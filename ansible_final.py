import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'backup_playbook.yaml', '-i', 'hosts']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"

def set_motd(ip, txt):
    command = [
        'ansible-playbook', 'motd_playbook.yaml',
        '-i', f'{ip},',
        '-e', (
            "ansible_user=admin "
            "ansible_password=cisco "
            "ansible_connection=network_cli "
            "ansible_network_os=ios "
            f"text={txt}"
        )
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=1' in result:
        return "Ok: success"
    else:
        return "Error: Ansible"
