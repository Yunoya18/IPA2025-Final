from netmiko import ConnectHandler
from pprint import pprint
import re

def setup(ip):
    device_ip = ip
    username = "admin"
    password = "cisco"

    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }
    return device_params

def gigabit_status(ip="10.0.15.61"):
    ans = ""
    device_params = setup(ip)
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        interfaces = []
        result = ssh.send_command("sh ip int bri", use_textfsm=True)
        for status in result:
            if status["interface"].startswith("GigabitEthernet"):
                interfaces.append(f"{status['interface']} {status['status']}")
                if status["status"] == "up":
                    up += 1
                elif status["status"] == "down":
                    down += 1
                elif status["status"] == "administratively down":
                    admin_down += 1
        ans = ", ".join(interfaces) + f" -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans

def get_motd(ip):
    device_params = setup(ip)
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command("show run | section ^banner motd")
    txt = re.search(r'banner motd\s+\^(.)\s+(.*?)\s+\^\1', result, re.DOTALL)
    if txt:
        return txt.group(2).strip()
    else:
        return "No MOTD configured"
