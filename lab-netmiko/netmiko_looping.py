import netmiko
import paramiko
import csv

data_file = open("netmiko_router.csv", "r")
data_router = csv.DictReader(data_file, delimiter=";")

for router in data_router:
    try:
        conn = netmiko.ConnectHandler(**router)
        conn.enable()
        print("-----------------------------------------")
        print(f"Router {router['host']}")

        output = conn.send_command("show run")
        file_output = open(f"backup_netmiko/{router['host']}.cfg", "w")
        file_output.write(output)
        file_output.close()
        print(f"backup Done {router['host']}!")

    except paramiko.ssh_exception.AuthenticationException:
        print(f"Username or password wrong {router['host']}")
    except paramiko.ssh_exception.NetmikoTimeoutException as message:
        print(message)
    except paramiko.ssh_exception.SSHException as message:
        print(message)
    except Exception as message:
        print(f"Other Eror {message}")