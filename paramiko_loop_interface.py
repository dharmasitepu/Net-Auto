import paramiko
import time
import getpass

ip_address = input("IP Address: ") or "10.10.10.1"
username = input("Username: ") or "cisco"
password = getpass.getpass() or "cisco"

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

for n in range(1,11):
    conn.send(f"int lo{n}\n")
    conn.send(f"ip add 10.1.1.{n} 255.255.255.255\n")
    time.sleep(1)

# for n in range(1,11):
#     conn.send(f"no int lo{n}\n")
#     time.sleep(1)

output = conn.recv(65635).decode()
print(output)

ssh_client.close()

