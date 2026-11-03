# Limits

What Kea cannot do, or will not do for
free, or cannot do from where it stands —
collected in one place, as this series
requires.

- **It cannot see the network it serves.**
  Kea knows what it was asked and what it
  answered. It cannot tell you that an
  address conflict came from a device with
  a static address typed in by hand, or
  that a second, rogue DHCP server is
  racing it — it will simply lose some
  races and never know. A DHCP server is a
  witness to requests, not a guard.
- **The packet exchange is only as good as
  the network path.** Broadcasts do not
  cross routers by themselves; serving
  another subnet means relays, and Kea's
  view of a relayed request is only what
  the relay tells it. Misconfigured relays
  are invisible from the server's chair.
- **Not every hook is open source.** The
  lease commands, statistics and high
  availability used here ship with Kea.
  Others — the host commands (including
  `reservation-*` API commands) and the
  configuration backend among them — are
  distributed to ISC support subscribers.
  The features still exist; the price of
  admission is a support contract, and a
  design that depends on them should know
  it from the start.
- **There is no dashboard.** Kea's answers
  are JSON and log lines. Pretty graphs,
  alerting and history come from pointing
  something else at its API and counters —
  a strength for automation, a gap if you
  expected a console.
- **The memfile backend is the small end.**
  CSV leases are perfect for a lab and a
  home and questionable for a campus:
  statistics live in the server, the file
  is rewritten by helper processes, and
  sharing truth between two servers wants
  a real database.
- **DHCP was not built with security in
  it.** The protocol has no authentication
  worth the name: any device can ask, any
  device can lie about its hardware
  address, and a client will believe any
  server that answers first. Kea adds
  controls at its own doors (API
  authentication, TLS on the agent) but it
  cannot retrofit trust onto the exchange
  itself. Networks that need that answer
  it at another layer — switch port
  security, 802.1X — not in DHCP.
- **IPv6 is a twin, not a superset.**
  DHCPv6 differs in kind (no broadcast,
  DUIDs instead of MACs, prefix delegation
  as its own art). This guide's IPv4 fluency
  transfers as orientation, not as detail.
- **And this guide's own limit, repeated:**
  the lab could configure, start and
  interrogate the server completely, but
  could not run the client exchange (the
  sandbox sends no UDP). Kea's behaviour
  under a thousand real clients — the thing
  perfdhcp exists to measure — is entirely
  outside what the lab can claim.
