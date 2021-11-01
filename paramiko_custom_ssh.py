from datetime import datetime
import paramiko
import time
import getpass


user = input("Username: ") or "cisco"
passw = getpass.getpass() or "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

list_router = [
        {
            "ip": "10.10.10.1",
            "user": "cisco",
            "passw": "cisco"
        },
        {
            "ip": "10.10.10.2",
            "user": "cisco2",
            "passw": "cisco2"
        },
        {
            "ip": "10.10.10.3",
            "user": "cisco3",
            "passw": "cisco3"
        },
        {
            "ip": "10.10.10.4",
            "user": "cisco4",
            "passw": "cisco4"
        },
        {
            "ip": "10.10.10.5",
            "user": "cisco5",
            "passw": "cisco5",
            "port":"2211"
        }
         
]

file_log = open("paramiko_log.txt", "a")

for router in list_router:
    try:
        # if "port" in router:
        #     ssh_client.connect(
        #         hostname=router["ip"],
        #         username=router["user"], 
        #         password=router["passw"],
        #         port=router["port"]
        # )
        # else:
        #     ssh_client.connect(
        #         hostname=router["ip"],
        #         username=router["user"], 
        #         password=router["passw"]
        # )

        ssh_client.connect(
            hostname=router["ip"],
            username=router["user"], 
            password=router["passw"],
            port=router["port"] if "port" in router else 22
        )
        print("-------------------------------------------")
        print(f"Success  login {router['ip']}")
        conn= ssh_client.invoke_shell()

        conn.send("show run | include username\n")
        time.sleep(4)

        output = conn.recv(65635).decode()
        print(output)

        ssh_client.close()
    except paramiko.ssh_exception.AuthenticationException as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"{message} [{router['ip']}]")
        file_log.write(f"[{datetime.now()}]-{message} [{router['ip']}]\n")
        print(f"Skip Login to {router['ip']}")
        print("-------------------------------------------")
    except paramiko.ssh_exception.NoValidConnectionsError as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"{message} [{router['ip']}]")
        file_log.write(f"[{datetime.now()}]-{message} [{router['ip']}]\n")
        print(f"Router {router['ip']} Not Running")
        print("-------------------------------------------")
    except Exception as message:
        print("-------------------------------------------")
        print("-------------------------------------------")
        print(f"Other Eror // {message} [{router['ip']}] //")
        file_log.write(f"[{datetime.now()}]-Other Eror // {message} [{router['ip']}] //\n")
        print(f"Skip Login to {router['ip']}")
        print("-------------------------------------------")
file_log.close()