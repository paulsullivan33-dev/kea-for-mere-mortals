# Kea for Mere Mortals

Every device that joins a network needs an
address before it can do anything else, and
on most networks the address is not typed in
by hand. It is handed out, on request, by a
**DHCP server** — the quiet service that
tells a new laptop "you are 192.168.1.42,
your gateway is over there, your DNS server
is this one, and you may keep the address
until Thursday." **Kea** is the DHCP server
written by the **Internet Systems Consortium
(ISC)** — the same people behind BIND — as
the modern successor to their original DHCP
server, which reached the end of its life in
2022. Kea is built for the job being large,
automated and watched: configuration in
JSON, leases in a choice of databases, and
every daemon controllable over a socket or
a REST API while it runs.

This guide explains how DHCP works, how Kea
is put together, how to install it and read
its configuration file, and how to run it
and prove it is doing what the configuration
says. It runs the real thing in its lab —
**Kea 2.4.1** from Ubuntu's packages — and
then makes one honest admission up front,
because the lab itself ran into it and the
guide does not hide it: **the lab machine
sits in a sandbox that refuses to send any
UDP packet at all**, and DHCP is a UDP
protocol. The server was installed,
configured, checked, started and listened
on its port; leases were added, read,
counted and deleted in its real lease
database through its real API; and a genuine
DHCPDISCOVER packet was built byte by byte.
What could not happen is the packet flying
the last few inches — so the client exchange
itself is taught from the protocol and the
server's own counters, and labelled
documented-only wherever it appears.
`criteria.md` keeps the full ledger.

One line belongs here, early, because a
DHCP server is a position of trust. Kea
answers *every* device that asks on the
network it serves, and its lease file is a
log of which machines were present, and
when. Run it only on networks you are
responsible for: a second, unauthorised
DHCP server on somebody else's network is
not a prank, it is how networks break (and
a known attack). Chapter 1 returns to this
before any procedure depends on it.

## What this guide covers

- [**What Kea is**](what-kea-is.md) —
  the mental model: the address desk of
  the network, leases instead of gifts,
  and why the person running it holds a
  position of trust
- [**The moving parts**](the-moving-parts.md) —
  the three daemons, the configuration
  file, the lease database, the hook
  libraries, and the two control channels
- [**Installing Kea**](installing-kea.md) —
  the Ubuntu packages, what lands where,
  and the version checks that prove it
  runs (including the command Ubuntu
  does not ship)
- [**The configuration file**](the-configuration-file.md) —
  Kea's JSON, section by section, and the
  two test modes that check a file before
  a server ever trusts it
- [**Starting the server**](starting-the-server.md) —
  interfaces, raw sockets versus UDP
  sockets, the state directories, and
  what a healthy startup looks like in
  the log
- [**How a lease happens**](how-a-lease-happens.md) —
  the four-packet exchange (discover,
  offer, request, acknowledge), the
  timers inside a lease, and the ways a
  lease ends
- [**Subnets, pools and options**](subnets-pools-and-options.md) —
  dividing address space, choosing what
  to hand out, and the extra answers
  (gateway, DNS, domain) that ride along
- [**Reservations**](reservations.md) —
  promising a known machine the same
  address every time, in the config file
  or in a database
- [**The control channel and the REST API**](the-control-channel.md) —
  talking to a running server: its Unix
  socket, the control agent's HTTP API,
  and the commands that answer
- [**Working with leases**](working-with-leases.md) —
  the lease database as a thing you can
  inspect: lease commands, statistics,
  the memfile CSV, and kea-admin
- [**Recipes**](recipes.md) — a home
  network setup, migrating from ISC DHCP,
  a second pair of eyes with statistics,
  and moving leases between backends
- [**The neighbours**](the-neighbours.md) —
  the old ISC DHCP, dnsmasq, your router,
  and Windows Server DHCP: what each does
  that Kea doesn't, and vice versa
- [**Limits**](limits.md) — no built-in
  pretty dashboard, hooks that are not
  all free, a server that cannot judge
  the network it cannot see, and the
  rest, stated plainly
- [**Troubleshooting**](troubleshooting.md) —
  the config keyword with the underscore,
  the socket the loopback refuses, the
  agent answering for a dead server, and
  the traps this guide's lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running Kea in high-availability pairs and
with MySQL or PostgreSQL backends is
described from the documentation and
labelled: the lab ran the memfile backend
on one machine. DHCPv6 gets the same
honesty — Kea ships a twin server for it,
`kea-dhcp6`, and this guide covers the IPv4
server in depth and says where the v6 one
differs. The client side of DHCP (the
software on your laptop that asks) is
explained only as far as the exchange
needs. And nothing here teaches pointing
Kea at a network you do not administer —
that is the line from chapter 1, not a
missing chapter.

## How to use this guide

Read chapter 1 for the model and chapter 2
for the map of parts. Chapter 3 installs;
chapter 4 is the one to read slowly, because
every later surprise is a configuration
surprise wearing a disguise. Chapters 5 and
6 get a server running and explain the
exchange it exists to serve. Chapters 9 and
10 are the operator's half: the API and the
lease database. The lab's transcripts live
in `kea-lab/transcripts/`, its configuration
files and API payloads in `kea-lab/config/`,
and its two small Python tools beside them,
so every claim can be re-checked, not just
read.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Home Networking for Mere Mortals](https://paulsullivan33-dev.github.io/home-networking-for-mere-mortals/)
- [Networking for Mere Mortals](https://paulsullivan33-dev.github.io/networking-for-mere-mortals/)
- [Unbound for Mere Mortals](https://paulsullivan33-dev.github.io/unbound-for-mere-mortals/)
- [netboot.xyz for Mere Mortals](https://paulsullivan33-dev.github.io/netboot-xyz-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/kea-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/kea-for-mere-mortals/blob/main/LICENSE-CODE).
