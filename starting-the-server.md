# Starting the Server

**Outcome: a Kea server running and
listening, a log that proves it, and a
straight answer about the two socket types
— including why this lab's server can
listen all day and never hand out a lease.**

## Starting it

On a systemd machine:

```bash
sudo systemctl enable --now kea-dhcp4-server
```

Without systemd — the lab's way, and the
way that shows you the moving parts — the
daemon is just a program reading a file:

```bash
sudo mkdir -p /run/kea /var/lib/kea /var/log/kea
kea-dhcp4 -c /etc/kea/kea-dhcp4.conf
```

(The lab ran with `-c` pointing at its own
copy in `kea-lab/config/`; the shape is the
same.) The lab's server came up and stayed
up. The evidence it leaves is threefold,
and chapter 13 will use all three as the
health check for any Kea install:

```text
$ pgrep -a kea-dhcp4
85714 kea-dhcp4 -c config/kea-dhcp4-lab.conf

$ ss -lunp | grep :67
UNCONN  127.0.0.1:67  users:(("kea-dhcp4",pid=85714))

$ grep DHCP4_STARTED /var/log/kea/kea-dhcp4.log
DHCP4_STARTED Kea DHCPv4 server version 2.4.1 started
```

`t04` keeps the full transcript, including
the control socket appearing in `/run/kea/`
and the lease file created with its header
row and no leases yet.

## The socket question, honestly

A DHCP server's natural habitat is a real
network interface, where clients broadcast
from having no address at all. To hear a
packet sent by a machine with no address,
Kea's default is a **raw socket** — it
takes packets straight off the wire, below
the normal UDP machinery. That is what
`"dhcp-socket-type"` defaults to, and on a
real server it is what you want.

The alternative, `"dhcp-socket-type": "udp"`,
opens ordinary UDP sockets bound to the
interface's addresses. It hears less (only
packets actually addressed to the server),
and for most production networks it is the
wrong tool — but it is the only socket type
Kea will open on the **loopback interface**.
With raw sockets the lab's start produced
this in the log (t09):

```text
DHCPSRV_OPEN_SOCKET_FAIL failed to open socket:
must not open socket on the loopback interface lo
```

That refusal is a Kea design rule, not a
sandbox quirk: raw sockets exist for
broadcast traffic, and loopback has none.

So the lab's server ran with UDP sockets,
bound to `127.0.0.1:67`, genuinely
listening. And there it met the sandbox's
own rule, which no configuration can talk
its way around: **in this environment,
sending a UDP packet is refused for every
process** — the lab probed it directly
(t02). No client inside the sandbox can
send a DISCOVER, and the server could not
send an OFFER if one arrived. The server
was real, the port was open, the exchange
was impossible. Everything after this
chapter therefore works Kea through its
control channel and lease database — which
are, not coincidentally, exactly the parts
an operator uses on a healthy network,
where the packet exchange is the clients'
business and not something you watch packet
by packet.

On your own hardware none of this applies:
same configuration, a real interface in
place of `lo`, raw sockets, and clients
will do the rest. Chapter 6 describes the
exchange those clients perform.
