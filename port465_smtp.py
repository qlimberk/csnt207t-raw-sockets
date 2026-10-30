import base64
import os
import socket
import ssl

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


SENDER = os.environ["SMTP_USER"]
PASSWORD = os.environ["SMTP_PASS"]
RECIPIENT = os.environ.get("SMTP_TO", SENDER)  #sir's email


def read_response(reader):
    """Read one SMTP reply (multi-line replies look like '250-...')."""
    while True:
        line = reader.readline().decode().rstrip("\r\n")
        print("S: " + line)
        if len(line) >= 4 and line[3] == " ":
            return line


def send_command(sock, reader, command, hide=False):
    print("C: " + ("<hidden>" if hide else command))
    sock.sendall((command + "\r\n").encode())
    return read_response(reader)


def send_email():
    
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    sock = context.wrap_socket(raw_sock, server_hostname=SMTP_HOST)
    sock.connect((SMTP_HOST, SMTP_PORT))
    reader = sock.makefile("rb")
    print(f"[+] SSL socket connected to {SMTP_HOST}:{SMTP_PORT}")
    read_response(reader)  # 220 banner

    
    send_command(sock, reader, "EHLO localhost")

    
    send_command(sock, reader, "AUTH LOGIN")
    send_command(sock, reader, base64.b64encode(SENDER.encode()).decode())
    send_command(sock, reader, base64.b64encode(PASSWORD.encode()).decode(), hide=True)

    
    send_command(sock, reader, f"MAIL FROM:<{SENDER}>")
    send_command(sock, reader, f"RCPT TO:<{RECIPIENT}>")

   
    send_command(sock, reader, "DATA")
    message = (
        f"From: {SENDER}\r\n"
        f"To: {RECIPIENT}\r\n"
        "Subject: Computer Networks Assignment - Raw Socket Test\r\n"
        "\r\n"
        "Hello! This email was sent using a raw SSL socket on port 465.\r\n"
        ".\r\n"  
    )
    print("C: <message body>\n" + message)
    sock.sendall(message.encode())
    read_response(reader)

    # 6. Close
    send_command(sock, reader, "QUIT")
    sock.close()
    print("[+] Email sent and connection closed.")


if __name__ == "__main__":
    send_email()