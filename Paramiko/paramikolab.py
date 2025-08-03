import paramiko
import os
import time

def ssh_command(ip, user, key_file, command):
    # โหลด private key
    pkey = paramiko.RSAKey.from_private_key_file(key_file)

    # ตั้งค่า client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Connecting to {ip}...")
    client.connect(hostname=ip, username=user, pkey=pkey)

    # ใช้ shell channel สำหรับ Cisco IOS
    shell = client.invoke_shell()
    shell.send(command + "\n")

    # รอรับผลลัพธ์
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode()

    print(f"\n--- Output from {ip} ---\n{output}\n")
    client.close()

# ==== เรียกใช้งาน ====

devices = [
    "172.31.40.1",
    "172.31.40.2",
    "172.31.40.3",
    "172.31.40.4",
    "172.31.40.5"
]

# ใช้ path แบบ relative หรือ absolute ก็ได้
private_key_path = os.path.join("key", ".ssh", "id_rsa")

for device in devices:
    ssh_command(device, "admin", private_key_path, "show version")
