# What Kea Is

A device that has just joined a network
knows nothing: not its own address, not
where the gateway is, not which DNS server
to ask for names. It could wait for a human
to type all of that in — the old way, and
still the right way for a few fixed servers
— or it can shout a question into the room:
*is anyone handing out addresses?* The
protocol for that shout is **DHCP**, the
Dynamic Host Configuration Protocol, and
the program that answers is a **DHCP
server**. Its answer is called a **lease**:
not a gift of an address, but a loan, with
the terms attached — how long you may keep
it, when to come back and renew it, and
the extras (gateway, DNS servers, domain
name) written on the same slip.

**Kea is ISC's DHCP server.** The Internet
Systems Consortium maintained the original
ISC DHCP for over two decades; when they
retired it (end of life, 2022) Kea was
already its designated successor, written
from scratch rather than patched forward.
The differences are the design: where ISC
DHCP kept its leases in a custom file and
was reconfigured by editing and restarting,
Kea keeps leases in a database you can
inspect (a CSV file, or MySQL, or
PostgreSQL), reads a configuration written
in JSON, and — the change you feel most as
an operator — **can be questioned and
commanded while it runs**, through a
control socket on the machine or a REST API
over HTTP. It also splits the job into
separate programs: one server for IPv4, a
twin for IPv6, a small daemon that keeps
DNS records in step with leases, and a
control agent that speaks HTTP on their
behalf. Chapter 2 draws the map.

## Why it matters that addresses are leased

A lease is a promise with an expiry date,
and that single idea runs the whole system.
Because addresses come back, a network of
200 addresses can serve 2,000 devices that
are never all present at once. Because a
lease is recorded, the server can answer
questions later: which address did that
machine have on Tuesday? Because renewal
is the client's job (chapter 6), a server
can stop and restart without the network
noticing — clients simply renew against
whoever answers next. And because the terms
ride along with the address, one change on
the server — a new DNS address, say —
reaches every device as its lease renews,
with nobody walking desk to desk.

## The trust line, up front

A DHCP server is believed by every device
that asks it. Whatever it answers — that is
your address, that is your gateway, that is
your DNS server — a client accepts. In the
wrong hands those same answers are a way to
steer a whole network's traffic through one
machine. Two consequences follow, and this
guide treats both as part of operating the
tool, not as fine print:

- **Run a DHCP server only on a network
  you administer.** A second server on a
  network that already has one races the
  real one, and clients take whichever
  answer arrives first. On your own
  network that is a fault you caused; on
  somebody else's it is a classic attack
  with a name (a *rogue DHCP server*).
- **A lease database is a record of
  presence.** It lists hardware addresses,
  hostnames, and the times devices came
  and went. That is genuinely useful — it
  is also a diary of the house. Keep it
  because you need it, protect it like
  any other log, and do not be surprised
  by what it can tell you.

The lab behind this guide practised on the
one network nobody can object to: the
loopback interface, 127.0.0.0/8, a network
with exactly one machine on it.

## A first taste

On a machine where Kea is installed and
running (chapters 3–5), the whole system
can be asked how it is in one HTTP call to
its control agent:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"command": "status-get", "service": ["dhcp4"]}' \
  http://127.0.0.1:8000/
```

```json
[ { "arguments": { "pid": 85714, "uptime": 51,
    "sockets": { "status": "ready" }, "...": "..." },
  "result": 0 } ]
```

`result: 0` is Kea's "yes"; the arguments
are the running server reporting on itself.
Chapter 9 lives inside that call. The point
to take from chapter 1 is the shape of the
tool: a service that hands out numbered,
expiring promises — and an operator who can
ask it, at any moment, exactly what it has
promised so far.

## What it is not

Kea is not a DNS server (it can *update*
one, through its DDNS daemon, but it does
not answer name lookups — the Unbound guide
in this series covers that side). It is not
a router or a firewall: it tells clients
where the gateway is, it is not the gateway.
It is not an inventory system, though its
lease file reads like one. And it is not
the small DHCP server inside your home
router, switched on by a checkbox — chapter
11 compares them fairly, because for many
homes the router's server is honestly
enough. Kea earns its place when the
network outgrows the checkbox: when you
want reservations in a file you can back
up, leases you can query, statistics you
can graph, and a second server standing
ready to take over.
