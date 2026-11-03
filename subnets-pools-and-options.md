# Subnets, Pools and Options

**Outcome: you can divide a network into
subnets Kea serves, set the pools it hands
out from, and attach the extra answers —
gateway, DNS, domain — that clients expect
to ride along with an address.**

## A subnet is a promise about a wire

Kea serves **subnets**: the networks
attached to its interfaces. When a request
arrives, Kea first decides which subnet it
belongs to — by the interface it arrived
on, or by the **relay agent** address
(`giaddr`) if a relay forwarded it — and
only that subnet's pools and options apply.
Each subnet in `subnet4` has:

- an **`id`** — a number you choose, used
  everywhere the subnet is referenced: in
  leases, in statistics, in API calls;
- the **`subnet`** itself, in CIDR form;
- optionally the **`interface`** it is
  reached through, as in the lab's config;
- **`pools`**, **`option-data`**, and
  **`reservations`** (chapter 8).

A server can carry many subnets; a small
network needs exactly one. The checker
(chapter 4) enforces the obvious: a pool
must live inside its subnet — the lab's
deliberate error, a `10.9.9.x` pool inside
`127.0.0.0/8`, was refused with the mismatch
named (t03).

## Pools: what may be handed out

A **pool** is a range of addresses within
the subnet that the server may give to
strangers:

```json
"pools": [ { "pool": "127.0.1.100 - 127.0.1.150" } ]
```

The lab's pool is 51 addresses. When the
server ran, its statistics knew the size
exactly — chapter 9's `statistic-get-all`
reported `subnet[1].total-addresses = 51`
and `assigned-addresses = 0` before any
lease existed (t06). Keep pools away from
addresses with fixed jobs: the gateway,
servers with static addresses, and any
reservations you plan to make *outside*
the pool — a reservation inside a pool
works, but outside is tidier, because the
pool then means "addresses no plan exists
for." Multiple pools per subnet are allowed
and simply merge into one supply.

How Kea picks within a pool is the
**allocator**: the default, `iterative`,
walks the range in order, remembering
where it stopped; `random` scatters;
`flq` (free-lease queue) recycles the
longest-free addresses first. The iterative
default suits nearly everyone.

## Options: the extras on the slip

An address alone is a device that can talk
only to its own street. **Options** are the
standardised extras a client asks for (its
DISCOVER lists the ones it wants, t05) and
the server supplies, written in the
configuration as `option-data`:

```json
"option-data": [
    { "name": "routers", "data": "127.0.0.1" },
    { "name": "domain-name-servers", "data": "127.0.0.1" },
    { "name": "domain-name", "data": "lab.example" }
]
```

Names are Kea's readable forms of the
numbered DHCP options (routers is option
3, domain-name-servers option 6). Options
can be set per subnet, as here, or globally
for every subnet, and a subnet's value
overrides the global one. The handful every
network sets:

- **routers** — the default gateway;
- **domain-name-servers** — where to ask
  for names (the Unbound guide's server,
  perhaps);
- **domain-name** — the suffix clients
  append to short names;
- **ntp-servers**, **broadcast-address**,
  and subnet-specific ones like a boot
  server for network booting (the
  netboot.xyz guide lives on one).

The lab's options are loopback-plausible
and invented — on a home network you would
write the gateway and resolver addresses
of that network. Options are answers a
client trusts as completely as the address
itself, which is chapter 1's trust line
again, one field at a time.

## Checking your arithmetic

The operator's check for this chapter is
the statistics command of chapter 9: after
a restart, `statistic-get-all` reports each
subnet's total and assigned addresses.
If the total is not the size of the pools
you wrote, the configuration the server is
running is not the one you think it is —
and now you know before a client does.
