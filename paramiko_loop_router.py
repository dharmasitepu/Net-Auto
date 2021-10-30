import paramiko
import time
import getpass

user = input("Username: ") or "cisco"
passw = getpass.getpass() or "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for x in range(1, 6):
    ssh_client.connect(
    hostname=f"10.10.10{x}",
    username=user,
    password=passw
    )

    print(f"Success login to 10.10.10{x}")
    conn= ssh_client.invoke_shell()

    conn.send("conf t\n")
    conn.send("int lo0\n")
    conn.send(f"ip add 10.1.1.{x} 255.255.255.255\n")
    time.sleep(1)
    conn.send("do write\n")
    time.sleep(3)
    

    output = conn.recv(65635).decode()
    print(output)

    ssh_client.close()