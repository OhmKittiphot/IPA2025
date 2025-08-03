from netmiko import ConnectHandler
from paramiko import RSAKey
from pathlib import Path

# ==== โหลด SSH Private Key ด้วย Paramiko ====
key_path = Path("key/.ssh/id_rsa").resolve()
private_key = RSAKey.from_private_key_file(str(key_path))

# ==== รายชื่ออุปกรณ์ ====
devices = [
    {
        "name": "S1",
        "device_type": "cisco_ios",
        "ip": "172.31.40.3",
        "username": "admin",
        "use_keys": True,
        "allow_agent": False,
        "pkey": private_key
    },
    {
        "name": "R1",
        "device_type": "cisco_ios",
        "ip": "172.31.40.4",
        "username": "admin",
        "use_keys": True,
        "allow_agent": False,
        "pkey": private_key
    },
    {
        "name": "R2",
        "device_type": "cisco_ios",
        "ip": "172.31.40.5",
        "username": "admin",
        "use_keys": True,
        "allow_agent": False,
        "pkey": private_key
    }
]

# ==== Config สำหรับแต่ละอุปกรณ์ ====
s1_config = [
    "vlan 101",
    "name CONTROL-DATA",
    "ip access-list standard MGMT_ONLY",
    "permit 172.31.40.0 0.0.0.15",
    "line vty 0 4",
    "access-class MGMT_ONLY in"
]

r1_config = [
    "router ospf 1",
    "network 10.10.1.0 0.0.0.255 area 0",
    "network 10.10.2.0 0.0.0.255 area 0",
    "ip access-list standard MGMT_ONLY",
    "permit 172.31.40.0 0.0.0.15",
    "line vty 0 4",
    "access-class MGMT_ONLY in"
]

r2_config = [
    "router ospf 1",
    "network 10.10.3.0 0.0.0.255 area 0",
    "network 10.10.4.0 0.0.0.255 area 0",
    "default-information originate",

    "ip access-list standard NAT_ACL",
    "permit 10.0.0.0 0.255.255.255",

    "ip nat inside source list NAT_ACL interface GigabitEthernet0/3 overload",

    "interface GigabitEthernet0/1",
    "ip nat inside",
    "interface GigabitEthernet0/2",
    "ip nat inside",
    "interface GigabitEthernet0/3",
    "ip nat outside",

    "ip route 0.0.0.0 0.0.0.0 192.168.249.129",

    "ip access-list standard MGMT_ONLY",
    "permit 172.31.40.0 0.0.0.15",
    "line vty 0 4",
    "access-class MGMT_ONLY in"
]

# ==== ฟังก์ชันสำหรับเชื่อมต่อและ config ====
def configure_device(device, config_list):
    device_name = device.get("name", device.get("ip"))
    print(f"Connecting to {device_name} ({device['ip']})...")

    device_params = device.copy()
    device_params.pop("name", None)

    try:
        ssh = ConnectHandler(**device_params)
        ssh.enable()
        output = ssh.send_config_set(config_list)
        print(output)
        ssh.disconnect()
    except Exception as e:
        print(f"Failed to connect to {device_name}: {e}")

# ==== เรียกใช้การตั้งค่า ====
if __name__ == "__main__":
    configure_device(devices[0], s1_config)
    configure_device(devices[1], r1_config)
    configure_device(devices[2], r2_config)
