# Reservations

**Outcome: you can promise a known machine
the same address on every visit, understand
where that promise is stored, and know how
to check that the server is holding it.**

Dynamic pools are for strangers. Some
machines are not strangers: the printer,
the NAS, the little sensor whose address
other things point at. For them, DHCP
offers **reservations** — a standing
instruction that when *this* client asks,
it gets *that* address. The client still
runs the four-packet exchange of chapter 6;
the server simply answers from the promise
instead of from the pool.

## A reservation in the configuration file

Kea identifies an IPv4 client most simply
by its **hardware address** (the MAC
address of its network card), and a
reservation in the subnet says so:

```json
"reservations": [
    {
        "hw-address": "02:00:00:00:00:01",
        "ip-address": "127.0.1.50",
        "hostname": "reserved-gadget"
    }
]
```

That is the lab's reservation, verbatim
from `kea-lab/config/kea-dhcp4-lab.conf`:
the invented client `02:00:00:00:00:01` —
the very address the lab built into its
DISCOVER packet, t05 — is promised
`127.0.1.50`, an address deliberately
*outside* the pool (`127.0.1.100–150`), so
the pool stays "addresses no plan exists
for" and the reserved address can never be
handed to a stranger by accident. The
optional `hostname` lets the server register
the name with the DDNS daemon.

Two behaviours worth knowing:

- A reservation beats the pool. If the
  reserved address is inside a pool and
  another client is holding it when the
  owner arrives, Kea will not evict the
  squatter mid-lease; the owner gets a
  pool address this once, and the conflict
  shows in the statistics
  (`v4-reservation-conflicts`, visible in
  t06's counters at 0).
- Reservations can also carry their own
  `option-data` — a machine can be promised
  not just an address but a different
  gateway or DNS answer than its subnet's.

## Where reservations live

Small networks keep reservations in the
configuration file, where a text editor
and the chapter 4 checker guard them.
Larger ones put them in a **hosts
database** — the same MySQL or PostgreSQL
backends as leases — where they can be
edited without touching the server's
configuration at all. Kea looks up
reservations on every request (the lab's
startup log notes that multi-threaded Kea
performs the reservation lookup first),
and a mode setting decides whether a
reservation found *only* in the database,
or also in the file, wins — read
`reservations-global`, `reservations-in-subnet`
and `reservations-out-of-pool` in the
documentation before mixing the two.

The honest limit of this guide's lab: the
reservation is **verified as configuration**
— parsed by `-T`, present in the running
server's `config-get` answer (chapter 9),
and built into the lab's DISCOVER packet —
but the moment of its fulfilment, an OFFER
of `.50` answering that packet, belongs to
the exchange the sandbox would not carry
(criteria.md). The API's `reservation-*`
commands, which would let us ask the server
directly, come from the host-commands hook
library, which is not in the open-source
packages — see chapter 12.

## The check

After any change to reservations, the
operator's routine is chapter 4's: run
`kea-dhcp4 -T` on the file, restart, then
`config-get` through the API and confirm
the reservation you wrote is the one the
running server reports. Configuration
drift — the file edited, the server never
restarted — is the commonest DHCP fault
there is, and it is invisible until exactly
that check.
