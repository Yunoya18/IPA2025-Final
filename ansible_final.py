import subprocess

def showrun(ip):
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook',
               'backup_playbook.yaml',
               '-i', f'{ip}',
               '-e', f'ansible_user=admin',
               '-e', f'ansible_password=cisco',
               '-e', 'ansible_network_os=ios',
               '-e', 'ansible_connection=network_cli']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"
