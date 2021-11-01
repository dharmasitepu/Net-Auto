from datetime import datetime
import paramiko
import getpass
import time
import csv


user = input("Username: ") or "cisco"
passw = getpass.getpass() or "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

list_router = open("data_router.csv", "r")
# data_router_list = list_router.readlines()
# data_router_list.remove(data_router_list[0])
data_router_dict = csv.DictReader(list_router, delimiter=";")
file_log = open("paramiko_log.txt", "a")


for router in data_router_dict:
    # router = router.split(";")
    try:
        # ssh_client.connect(
        #     hostname=router[0],
        #     username=router[1], 
        #     password=router[2],
        #     port=router[3] if router[3] else 22
        # )
        ssh_client.connect(
            hostname=router["ip"],
            username=router["username"], 
            password=router["password"],
            port=router["port"] if router["port"] else 22
        )
        print("-------------------------------------------")
        print(f"Success  login {router['ip']}")
        conn= ssh_client.invoke_shell()

        if router["enable"]: #.strip():
            conn.send("enable\n")
            conn.send(f"{router['enable']}\n")
            time.sleep(1)

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