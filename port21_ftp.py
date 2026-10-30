import socket

HOST = "test.rebex.net"
USER = "demo"
PASSWORD = "password"
FILENAME = "readme.txt"


def read_response(reader):
    """Read one FTP reply (handles multi-line replies like '220-...')."""
    lines = []
    while True:
        line = reader.readline().decode().rstrip("\r\n")
        lines.append(line)
        print("S: " + line)
        if len(line) >= 4 and line[:3].isdigit() and line[3] == " ":
            break
    return lines[-1]


def send_command(sock, reader, command):
    print("C: " + command)
    sock.sendall((command + "\r\n").encode())
    return read_response(reader)


def ftp_download():
    ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrl.connect((HOST, 21))
    reader = ctrl.makefile("rb")
    print(f"[+] Control socket connected to {HOST}:21")
    read_response(reader)  # welcome banner

    
    send_command(ctrl, reader, f"USER {USER}")
    send_command(ctrl, reader, f"PASS {PASSWORD}")

    
    send_command(ctrl, reader, "TYPE I")
    pasv_reply = send_command(ctrl, reader, "PASV")

    
    if pasv_reply.startswith("229"):
        
        data_ip = HOST
        data_port = int(pasv_reply.split("|||")[1].split("|")[0])
    else:
        
        numbers = pasv_reply[pasv_reply.index("(") + 1:pasv_reply.index(")")].split(",")
        data_ip = ".".join(numbers[:4])
        data_port = int(numbers[4]) * 256 + int(numbers[5])
    print(f"[+] Data socket target: {data_ip}:{data_port}")

    
    data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data.connect((data_ip, data_port))
    send_command(ctrl, reader, f"RETR {FILENAME}")

    
    content = b""
    while True:
        chunk = data.recv(4096)
        if not chunk:
            break
        content += chunk
    data.close()
    read_response(reader)  

    
    with open(FILENAME, "wb") as f:
        f.write(content)
    print(f"[+] Saved {len(content)} bytes to {FILENAME}")

    send_command(ctrl, reader, "QUIT")
    ctrl.close()


if __name__ == "__main__":
    ftp_download()