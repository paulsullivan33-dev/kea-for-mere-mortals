# Glossary

**ACK** — the fourth packet of the lease
exchange: the server's confirmation that
records the lease and lets the client use
the address.

**Allocator** — the rule Kea uses to pick
the next free address in a pool: iterative
(in order), random, or flq (longest-free
first).

**Broadcast flag** — a bit in a client's
request asking the server to broadcast its
reply, set by clients that cannot yet
receive a packet addressed to their new
address.

**chaddr** — the field in a DHCP packet
carrying the client's hardware address;
the identity reservations are written
against.

**Control agent** — `kea-ctrl-agent`: the
small HTTP server that forwards API
commands to the daemons' control sockets.

**Control socket** — the Unix socket each
running daemon accepts JSON commands on.

**Decline** — a client's refusal of an
offered address it found already in use;
Kea puts the address on probation rather
than reoffering it.

**DDNS daemon** — `kea-dhcp-ddns`: the
daemon that turns lease events into DNS
record updates.

**DHCP** — Dynamic Host Configuration
Protocol: the shout of "who hands out
addresses?" and the lease that answers it.

**DISCOVER** — the first packet: a client
with no address broadcasting for a server.

**DORA** — the four-packet exchange's
initials: Discover, Offer, Request,
Acknowledge.

**giaddr** — the gateway-IP-address field,
filled in by a relay agent; how a server
knows which subnet a forwarded request
belongs to.

**Hook library** — a loadable module that
extends a Kea daemon: lease commands,
statistics, high availability, and others.

**kea-admin** — the offline tool for lease
databases: init, upgrade, dump, upload.

**keactrl** — upstream's start/stop script
for the daemons; not shipped in Ubuntu's
packages.

**Lease** — an address loaned, not given:
an address, a lifetime, and the extras,
recorded in the lease database.

**Lease database** — where leases live:
the memfile CSV, or MySQL, or PostgreSQL.

**Magic cookie** — the four bytes
`63 82 53 63` marking a BOOTP packet's
options as DHCP options.

**Memfile** — Kea's simplest lease backend:
leases in memory, persisted to a CSV file,
tidied by `kea-lfc`.

**NAK** — the server's refusal of a
client's request for an address it should
not have; the client starts over.

**OFFER** — the second packet: a server's
proposed address and terms, not yet a
lease.

**Option data** — the extras that ride with
an address: routers, DNS servers, domain
name, and the rest of the numbered DHCP
options.

**perfdhcp** — ISC's DHCP load tester,
shipped with kea-admin.

**Pool** — a range of addresses within a
subnet that the server may hand to any
client that asks.

**Raw socket** — a socket that takes
packets straight off the interface, below
UDP; Kea's default, and the only way to
hear clients that have no address yet.

**Rebind (T2)** — the second timer in a
lease (seven-eighths of the lifetime):
broadcast a renewal request to any server.

**Relay agent** — a helper on a subnet with
no server, forwarding client broadcasts to
a server elsewhere and marking them with
`giaddr`.

**Renew (T1)** — the first timer in a lease
(half the lifetime): ask the leasing server
to extend it.

**REQUEST** — the third packet: the client
broadcasting which offer it accepts.

**Reservation** — a standing promise that a
known client (by hardware address) always
receives a particular address.

**Result code** — the API's answer summary:
0 success, 1 error, 2 unsupported command,
3 not found, 4 refused with reasons.

**Rogue DHCP server** — an unauthorised
server answering on a network: a fault when
accidental, an attack when not.

**Subnet** — one network Kea serves, with
its pools, options and reservations,
numbered by an `id` used everywhere it is
referenced.
