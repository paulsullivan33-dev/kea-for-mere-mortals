# The Moving Parts

Kea is not one program. It is a small crew
of programs, a database, and two doors to
talk to them through. Knowing which part
holds what turns most confusion into a
named problem, so here is the map before
anything is installed.

## The servers

- **`kea-dhcp4`** — the IPv4 DHCP server.
  Listens on UDP port 67, hands out leases,
  writes them to the lease database. This
  guide's main character.
- **`kea-dhcp6`** — the IPv6 twin. Same
  design, different protocol details
  (DHCPv6 has no broadcast and identifies
  clients by DUID rather than hardware
  address). Installed alongside, covered
  here only where it differs.
- **`kea-dhcp-ddns`** — the Dynamic DNS
  daemon. When a lease is granted or
  released, the DHCP server sends it a note
  (a *Name Change Request*) and this daemon
  updates the DNS server's records, so
  `printer.example.net` can resolve to the
  address the printer just leased. They
  talk over UDP port 53001 on the local
  machine by default. The lab installed it
  and did not exercise it — DNS updates
  need a DNS server configured to accept
  them, which is its own project; see
  `criteria.md`.

## The lease database

Every lease lives in a **lease database**
with one of three backends:

- **memfile** — the default and the
  simplest: leases held in memory and
  written to a CSV file (traditionally
  `/var/lib/kea/kea-leases4.csv`). A helper
  process, **`kea-lfc`**, periodically
  tidies the file (the *lfc-interval*).
  The lab ran this backend, and chapter 10
  reads the CSV directly.
- **MySQL** or **PostgreSQL** — leases in a
  real database, the choice for large or
  high-availability setups, where two
  servers share one truth. Documented
  here, not run.

Host reservations (chapter 8) can live in
the configuration file or in a database of
their own, through the same backends.

## The configuration file

Each daemon reads one JSON file —
`/etc/kea/kea-dhcp4.conf` and siblings —
written in JSON with the courtesy that
`//` comments are allowed. The file names
the interfaces to serve, the subnets and
pools to hand out, the lease database, the
logging, and any **hook libraries**:
loadable modules that extend the server.
Two hooks matter in this guide and both
ship free with Kea — `libdhcp_lease_cmds`
(the lease commands of chapter 10) and
`libdhcp_stat_cmds` (lease statistics).
Others exist — high availability among
them — and a few, such as the host
commands and the configuration backend,
are distributed to ISC support subscribers
rather than in the open-source packages.
Chapter 12 returns to that line.

## The two control channels

A running server can be talked to, and
there are two doors:

1. **The control socket** — a Unix socket
   each daemon opens (for dhcp4,
   `/run/kea/kea4-ctrl-socket`). Local,
   permission-protected, speaking JSON
   commands one at a time. Tools like
   `kea-shell` talk here.
2. **The control agent** — **`kea-ctrl-agent`**,
   a small HTTP server (default port 8000)
   that accepts REST-style POSTs and
   forwards each command to the right
   daemon's socket. This is the door
   automation uses, and the one chapter 9
   exercises in full — the lab put it on
   port 18081 to keep the sandbox's
   assigned ports straight.

Behind both doors live the same **commands**:
`config-get`, `lease4-add`, `statistic-get-all`,
`shutdown`, dozens more. A command names a
service (`"dhcp4"`), carries optional
arguments, and gets back a `result` code —
0 for success, small integers for the
flavours of failure, each with a `text`
explanation. Once you have seen one command
work, you have the shape of all of them.

## The supporting cast

- **`kea-admin`** — the offline tool: it
  works on the lease database when the
  server is stopped (or on a copy):
  initialising databases, checking schema
  versions, dumping and uploading leases.
  Chapter 10 puts it to work and reports
  its honest limits against memfile.
- **`keactrl`** — upstream's start/stop
  script. Ubuntu's packages do not ship it
  (chapter 3 shows the evidence); on
  Ubuntu, systemd units or a direct launch
  do the job.
- **`perfdhcp`** — ISC's DHCP load tester,
  shipped in the kea-admin package: it can
  pretend to be thousands of clients. The
  lab tried it once, and the sandbox
  refused it the same way it refused
  everything else that sends UDP (t05).

Everything else in the guide is these
parts in combination. Next: installing
them.
