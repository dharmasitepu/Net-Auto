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

for ip in list_ip:
    ssh_client.connect(
        hostname=ip,
        username=user, 
        password=passw
    )

    print(f"Success  login {ip}")
    conn= ssh_client.invoke_shell()

    conn.send("conf t\n")
    conn.send("int lo4\n")
    conn.send(f"ip add 10.5.1.1 255.255.255.255\n")
    time.sleep(1)
    conn.send("do write\n")
    time.sleep(3)

    output = conn.recv(65635).decode()
    print(output)

    ssh_client.close()

