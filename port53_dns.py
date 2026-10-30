import socket
import struct

DNS_SERVER = "8.8.8.8"
DOMAIN = "example.com"


def build_query(domain):
    
    header = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0)

    
    qname = b""
    for label in domain.split("."):
        qname += bytes([len(label)]) + label.encode()
    qname += b"\x00"

    
    question = qname + struct.pack(">HH", 1, 1)
    return header + question


def skip_name(data, pos):
    """Move past a domain name (handles compression pointers)."""
    while True:
        length = data[pos]
        if length == 0:
            return pos + 1
        if length & 0xC0 == 0xC0:  
            return pos + 2
        pos += 1 + length


def dns_lookup():
    query = build_query(DOMAIN)

    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    
    sock.sendto(query, (DNS_SERVER, 53))
    print(f"[+] Sent {len(query)} bytes to {DNS_SERVER}:53")
    print("[+] Query (hex): " + query.hex())

    
    response, addr = sock.recvfrom(512)
    sock.close()
    print(f"[+] Received {len(response)} bytes from {addr[0]}:{addr[1]}")
    print("[+] Response (hex): " + response.hex())

    
    resp_id, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", response[:12])
    print(f"[+] ID={hex(resp_id)} Flags={hex(flags)} Questions={qd} Answers={an}")

    
    pos = skip_name(response, 12) + 4
    for _ in range(an):
        pos = skip_name(response, pos)
        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH", response[pos:pos + 10])
        pos += 10
        if rtype == 1 and rdlen == 4: 
            ip = ".".join(str(b) for b in response[pos:pos + 4])
            print(f"[+] {DOMAIN} -> {ip} (TTL {ttl}s)")
        pos += rdlen


if __name__ == "__main__":
    dns_lookup()