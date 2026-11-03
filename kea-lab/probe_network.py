#!/usr/bin/env python3
"""Probe what the lab sandbox allows, before the guide claims anything.

Three questions:
  1. Can we open a raw socket (what Kea uses by default for DHCP)?
  2. Can we send and receive UDP on loopback (Kea's "udp" socket type)?
  3. What interfaces exist?
"""
import socket

print("== 1. raw socket ==")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    print("raw socket: OPENED (unexpected in this sandbox)")
    s.close()
except OSError as e:
    print(f"raw socket: REFUSED -- {e}")

print()
print("== 2. UDP on loopback ==")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 18767))
server.settimeout(3)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(3)
try:
    client.sendto(b"ping", ("127.0.0.1", 18767))
    data, addr = server.recvfrom(64)
    print(f"server received {data!r} from {addr}")
    server.sendto(b"pong", addr)
    data, addr = client.recvfrom(64)
    print(f"client received {data!r} from {addr}")
    print("UDP loopback: WORKS")
except OSError as e:
    print(f"UDP loopback: FAILED -- {e}")
server.close()
client.close()

print()
print("== 3. interfaces ==")
for idx, name in socket.if_nameindex():
    print(f"  {name}")
