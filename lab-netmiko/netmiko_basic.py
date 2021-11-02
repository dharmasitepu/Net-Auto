from netmiko import ConnectHandler


r1 = {
    "device_type": "cisco_ios",
    "host": "10.10.10.2",
    "username": "cisco2",
    "password": "cisco2",
}

conn = ConnectHandler(**r1)

list_config = [
    "int lo8",
    "ip address 10.1.1.8 255.255.255.255",
]

output = conn.send_config_set(list_config)
print(output)

output = conn.send_command("show ip int brief")
print(f"interface for router {r1['host']}")
print(output)