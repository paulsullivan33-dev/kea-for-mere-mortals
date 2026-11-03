# Installing Kea

**Outcome: Kea 2.4.1 installed from Ubuntu's
packages, every daemon's version check
answering, and a clear picture of where the
files live — including the differences from
upstream's documentation that Ubuntu's
packaging makes.**

## The install

On Ubuntu 24.04, Kea is four packages (plus
`kea-common`, which arrives by itself):

```bash
sudo apt-get install -y \
  kea-dhcp4-server kea-ctrl-agent \
  kea-admin kea-dhcp-ddns-server
```

Add `kea-dhcp6-server` if you intend to
serve IPv6. ISC also publishes its own
packages with newer versions; the Ubuntu
ones are the plainer path and are what this
guide exercised. On a normal Ubuntu install
the packages also create systemd units that
would start the daemons for you; the lab
has no systemd, so it created the state
directories and started daemons by hand
(chapter 5) — on a real machine,
`systemctl enable --now kea-dhcp4-server`
does that part.

## The check

Kea's daemons take single-letter flags —
`-v` for version (a long `--version` is
refused, politely, with usage text):

```bash
$ kea-dhcp4 -v
2.4.1
$ kea-ctrl-agent -v
2.4.1
$ kea-admin -v
2.4.1
```

`kea-dhcp4 -V` prints the extended report —
what it was linked with, and which database
backends were compiled in (the lab's build:
MySQL, PostgreSQL, and Memfile 3.0). The
full transcript is t00.

## Where things live

| Thing | Place |
|---|---|
| Daemons | `/usr/sbin/kea-dhcp4`, `kea-dhcp6`, `kea-dhcp-ddns`, `kea-ctrl-agent` |
| Tools | `/usr/sbin/kea-admin`, `kea-shell`, `kea-lfc`, `perfdhcp` |
| Configuration | `/etc/kea/kea-dhcp4.conf`, `kea-ctrl-agent.conf`, `kea-dhcp-ddns.conf` |
| Hook libraries | `/usr/lib/x86_64-linux-gnu/kea/hooks/` |
| Runtime state (sockets, PID files) | `/run/kea/` |
| Lease files | `/var/lib/kea/` |
| Logs | `/var/log/kea/` (if the config sends them there) |

Three of those directories are worth a
second look. On a systemd install they are
created by the units themselves (the unit
files declare `RuntimeDirectory`,
`StateDirectory`, `LogsDirectory`), and the
daemons run as the unprivileged `_kea`
user. Without systemd — the lab's position —
they may not exist at all after install,
and the daemons will refuse to start until
you create them:

```bash
sudo mkdir -p /run/kea /var/lib/kea /var/log/kea
```

## Two Ubuntu differences to know now

1. **There is no `keactrl`.** Upstream's
   documentation leans on `keactrl start /
   status / stop`; Debian and Ubuntu do not
   package it. The lab checked
   (`keactrl: command not found`, t01).
   On Ubuntu: systemd units, or launching
   `kea-dhcp4 -c /etc/kea/kea-dhcp4.conf`
   directly.
2. **The shipped configuration is a
   starting point, not a server.** The
   package's `kea-dhcp4.conf` defines no
   subnet of yours; it will run and serve
   nothing until you write a configuration.
   That is the next chapter's job.

The install is proven when every `-v`
answers with the same version. Configuration
is where Kea becomes *your* server.
