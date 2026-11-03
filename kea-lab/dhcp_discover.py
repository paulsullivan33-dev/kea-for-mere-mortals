#!/usr/bin/env python3
"""Build a real DHCPDISCOVER packet, byte by byte, then try to send it.

The packet is genuine: BOOTP header, magic cookie, message-type
option. The client hardware address is invented for the lab and
matches the reservation in the lab config (02:00:00:00:00:01).
"""
import socket
import struct

HWADDR = bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
XID = 0x3903F326

packet = struct.pack("!BBBB", 1, 1, 6, 0)          # op=BOOTREQUEST, htype=Ethernet, hlen=6, hops=0
packet += struct.pack("!I", XID)                    # transaction id
packet += struct.pack("!HH", 0, 0x8000)             # secs, flags (broadcast)
packet += socket.inet_aton("0.0.0.0")               # ciaddr
packet += socket.inet_aton("0.0.0.0")               # yiaddr
packet += socket.inet_aton("0.0.0.0")               # siaddr
packet += socket.inet_aton("0.0.0.0")               # giaddr
packet += HWADDR + b"\x00" * 10                     # chaddr (16 bytes)
packet += b"\x00" * 64                              # sname
packet += b"\x00" * 128                             # file
packet += b"\x63\x82\x53\x63"                       # magic cookie
packet += b"\x35\x01\x01"                           # option 53: DHCPDISCOVER
packet += b"\x37\x04\x01\x03\x06\x0f"               # option 55: parameter request list
packet += b"\xff"                                   # end

print(f"built DHCPDISCOVER: {len(packet)} bytes")
print(f"  op=1 (request)  xid=0x{XID:08x}  flags=0x8000 (broadcast)")
print(f"  chaddr = {':'.join(f'{b:02x}' for b in HWADDR)}  (the reserved client)")
print(f"  magic cookie 63 82 53 63, option 53 = 1 (DISCOVER)")
print()
print("sending to 127.0.0.1:67 from a UDP socket bound to port 68 ...")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    client.bind(("127.0.0.1", 68))
    print("  bind to 127.0.0.1:68: OK")
    client.sendto(packet, ("127.0.0.1", 67))
    print("  sendto: OK (unexpected)")
except OSError as e:
    print(f"  sendto: REFUSED -- {e}")
    print()
    print("Result: the packet is real but undeliverable. The sandbox refuses")
    print("every UDP send (see t02), so no DISCOVER can reach the server and")
    print("no OFFER could come back. The lease dance itself is therefore")
    print("documented-only in this guide; the lease database is exercised")
    print("directly through the control channel instead (t07, t08).")
client.close()
