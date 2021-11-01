from datetime import datetime
import paramiko
import time
import getpass


user = input("Username: ") or "cisco"
passw = getpass.getpass() or "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

list_ip = [
    "10.10.10.1", "10.10.10.2", "10.10.10.3",
    "10.10.10.4", "10.10.10.5" 
]

file_log = open("paramiko_log.txt", "a")

for ip in list_ip:
    ip_split = ip.split(".")[-1]

    try:
        ssh_client.connect(
            hostname=ip,
            username=user, 
            password=passw
        )
        print("-------------------------------------------")
        print(f"Success  login {ip}")
        conn= ssh_client.invoke_shell()

        conn.send("show ip int br | ex unas\n")
        time.sleep(2)

        output = conn.recv(65635).decode()
        print(output)

        ssh_client.close()
    except paramiko.ssh_exception.AuthenticationException as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"{message} [{ip}]")
        file_log.write(f"[{datetime.now()}]-{message} [{ip}]\n")
        print(f"Skip Login to {ip}")
        print("-------------------------------------------")
    except paramiko.ssh_exception.NoValidConnectionsError as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"{message} [{ip}]")
        file_log.write(f"[{datetime.now()}]-{message} [{ip}]\n")
        print(f"Router {ip} Not Running")
        print("-------------------------------------------")
    except Exception as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"Other Eror // {message} [{ip}] //")
        file_log.write(f"[{datetime.now()}]-Other Eror // {message} [{ip}] //\n")
        print(f"Skip Login to {ip}")
        print("-------------------------------------------")
file_log.close()