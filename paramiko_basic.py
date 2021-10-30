import paramiko
import time
import getpass

ip_address = input("IP Address: ")
username = input("Username: ")
password = getpass.getpass()

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(
    hostname=ip_address, 
    username=username, 
    password=password
    )
print(f"Success  login to {ip_address}")
conn= ssh_client.invoke_shell()

conn.send("conf t\n")
conn.send("int lo0\n")
conn.send("ip add 1.1.1.1 255.255.255.255\n")
time.sleep(1)

output = conn.recv(65635).decode()
print(output)

ssh_client.close()

