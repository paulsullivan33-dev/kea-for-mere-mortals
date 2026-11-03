# Recipes

Each recipe assumes the chapters before it:
a checked configuration, a running server,
and the control agent answering. Addresses
are written for a small example network,
`192.168.10.0/24` — substitute your own.

## 1. A home network, on purpose

The shape this guide's lab used, scaled to
a real house: one subnet, one pool, a
reservation for the machine that must never
move, and the router's own DHCP server
**switched off** — one address desk per
network (chapter 1's rule).

```json
"subnet4": [ {
    "id": 1,
    "subnet": "192.168.10.0/24",
    "interface": "eth0",
    "pools": [ { "pool": "192.168.10.100 - 192.168.10.199" } ],
    "option-data": [
        { "name": "routers", "data": "192.168.10.1" },
        { "name": "domain-name-servers", "data": "192.168.10.2" }
    ],
    "reservations": [
        { "hw-address": "aa:bb:cc:dd:ee:ff",
          "ip-address": "192.168.10.2",
          "hostname": "resolver" }
    ]
} ]
```

Check with `kea-dhcp4 -T`, restart, then
verify with `statistic-get-all` that the
subnet's total is 100 — the size of the
pool you meant to write. Keep static
addresses (gateway `.1`, resolver `.2`)
below the pool, so the pool means
"unplanned addresses" only.

## 2. Migrate from ISC DHCP

ISC DHCP is end-of-life, and ISC wrote the
bridge: **`keama`**, the Kea Migration
Assistant (package `isc-dhcp-keama`). It
reads a `dhcpd.conf` and writes the
equivalent Kea JSON:

```bash
keama -i dhcpd.conf -o kea-dhcp4.conf
```

Treat its output as a first draft, not a
faithful translation: run `kea-dhcp4 -T` on
it, diff the pools and reservations against
the old file by eye, and know that the
exotic corners of dhcpd.conf (classes,
failover peers, arbitrary conditionals) are
where a translator earns its warnings.
Then run the two servers **not at once** —
stop the old one in the same minute you
start the new one; clients renew into the
new server as their timers ring (chapter 6).

## 3. A second pair of eyes: watch the counters

Point whatever watches your machines at the
control agent and poll `statistic-get-all`
(or `stat-lease4-get` per subnet) every few
minutes. The numbers that earn a graph:
`subnet[N].assigned-addresses` against
`total-addresses` (a pool creeping toward
full is next month's outage, visible
today) and `pkt4-discover-received`
flatlining at zero on a network that is
awake (the server has a problem the clients
haven't reported yet). The neighbours in
this series' watching-your-systems guides
will happily do the polling.

## 4. Move leases between backends

Outgrowing memfile? The path is
`kea-admin`'s, and it works while you plan
the changeover:

1. `kea-admin db-init mysql` (with the
   database name and credentials) to build
   the schema.
2. Stop Kea; `kea-admin lease-dump mysql`
   — or, from memfile, the CSV you already
   have *is* the dump (chapter 10).
3. `kea-admin lease-upload mysql -i leases.csv`
   to load the leases into the database.
4. Point `lease-database` at the new
   backend, `-T` the configuration, start,
   and confirm with `lease4-get-all` that
   the leases you moved are the leases the
   running server reports.

Described from kea-admin's documented
interface — the lab ran memfile only, and
its memfile-shaped answers are in t08.

## 5. Standby pair, in one paragraph

Two Kea servers, one lease database story,
the `libdhcp_ha` hook loaded on both, one
configured `hot-standby`: the standby
watches the primary's heartbeat and takes
over its subnets if it goes quiet. This is
documented-only in this guide (one machine,
one lab) and it is the feature to read
ISC's high-availability chapter for before
you need it on a Friday night — set it up
on a calm Tuesday instead.
