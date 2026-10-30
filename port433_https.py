import socket
import ssl
import webbrowser


def decode_chunked(body):
    """Remove HTTP chunked-encoding framing (hex size lines) from the body."""
    result = b""
    while body:
        size_line, body = body.split(b"\r\n", 1)
        size = int(size_line.split(b";")[0], 16)
        if size == 0:
            break
        result += body[:size]
        body = body[size + 2:]  
    return result


def fetch_page_via_port_443(host="www.wikipedia.org"):
   
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    context = ssl.create_default_context()
    sock = context.wrap_socket(raw_sock, server_hostname=host)

    
    sock.connect((host, 443))
    print(f"[+] Connected to {host}:443 using {sock.version()}")

    
    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    sock.sendall(request.encode())

    
    response = b""
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response += data
    sock.close()

    
    header_part, html_body = response.split(b"\r\n\r\n", 1)
    print("[+] Received Response Headers:\n" + header_part.decode())

    
    if b"transfer-encoding: chunked" in header_part.lower():
        html_body = decode_chunked(html_body)
        print("[+] Chunked encoding detected and decoded.")

    
    with open("output.html", "wb") as f:
        f.write(html_body)

    webbrowser.open("output.html")
    print("[+] Saved payload to output.html and launched browser.")


if __name__ == "__main__":
    fetch_page_via_port_443()