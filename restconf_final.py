import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.61"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"}
basicauth = ("admin", "cisco")

def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070200",
            "description": "My RESTCONF loopback",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.2.0.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        api_url + "/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070200",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )
    if resp.status_code == 204:
        return "Cannot create: Interface loopback 66070200"
    elif (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070200 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070200"

def delete():
    resp = requests.delete(
        api_url + "/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070200",
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070200 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070200"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070200",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }

    resp = requests.put(
        api_url + "/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070200",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070200 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070200"


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070200",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.put(
        api_url + "/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070200", 
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070200 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070200"


def status():
    api_url_status = api_url + "/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070200"

    resp = requests.get(
        api_url_status,
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070200 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070200 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070200"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
