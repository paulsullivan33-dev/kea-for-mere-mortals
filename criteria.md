# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab served the loopback network 127.0.0.0/8 with invented
   hardware addresses, hostnames and a `lab.example` domain.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: a server that cannot see the network it serves
   and cannot detect a rogue rival, no built-in dashboard,
   a memfile backend that is the small end of the range,
   hook libraries that are not all open source, a protocol
   with no real authentication to retrofit trust onto, and
   an IPv6 twin that differs in kind rather than in detail.
8. **The ethics rule is in the text, early.** A DHCP server is
   believed by every device that asks it, so the README and
   chapter 1 draw the line before any procedure depends on
   it: run a DHCP server only on a network you administer (a
   second server on somebody else's network is a fault when
   accidental and an attack — a rogue DHCP server — when not),
   and treat the lease database as what it is, a record of
   which devices were present and when, kept because it is
   needed and protected like any other log.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran. Kea **2.4.1** was
installed from Ubuntu's own packages (kea-dhcp4-server,
kea-ctrl-agent, kea-admin, kea-dhcp-ddns-server, all
2.4.1-3ubuntu0.2) and run unmodified. All transcripts live in
`kea-lab/transcripts/`; the lab's configuration files and API
payloads are in `kea-lab/config/`; its two Python tools are
`kea-lab/probe_network.py` and `kea-lab/dhcp_discover.py`.

**The sandbox's network limits decide this guide's shape, and
they were measured, not assumed (t02).** Raw sockets are
refused (`Operation not permitted`). UDP sockets can be created
and bound, but *sending* any UDP packet is refused for every
process; TCP on loopback works normally. DHCP is UDP, so the
client exchange could not be carried by this machine — and
Kea, by design, will not open a raw socket on the loopback
interface at all (t09). Everything that does not depend on a
UDP packet flying was run for real.

Run for real, with transcripts as evidence:

- Installation and versions: every daemon's `-v` (2.4.1), the
  extended build report naming the compiled-in database
  backends, the package list, and the layout of `/etc/kea`,
  the hook libraries, and the control sockets (t00, t01) —
  including the negative evidence that Ubuntu ships **no
  `keactrl`**, which upstream documentation relies on.
- Configuration: the lab's full configuration (loopback
  subnet 127.0.0.0/8, a 51-address pool, options, one
  reservation, memfile leases, lease/stat hooks) checked with
  `kea-dhcp4 -t` and `-T`, and the control agent's file with
  `kea-ctrl-agent -t`; a deliberately broken file (pool outside
  its subnet) refused with the reason and file position named;
  and the lab's own first error — `output-options` where Kea
  requires `output_options` — kept as evidence (t03).
- The server running: `kea-dhcp4` started by hand (no systemd
  exists here, so the state directories were created first),
  bound to 127.0.0.1:67/UDP, control socket open in `/run/kea`,
  lease file created, `DHCP4_STARTED` in its log (t04).
- The DISCOVER packet built byte by byte and decoded — a real
  250-byte packet for the reserved lab client — and its send
  refused by the sandbox; ISC's `perfdhcp`, tried once, was
  refused in the same sandbox and found port 67 already held
  by the running server (t05). The server's packet counters
  afterwards were all zero: no exchange slipped past the lab.
- The control channel in full: the control agent on
  127.0.0.1:18081 answering `version-get`, `status-get`,
  `list-commands` (fifty commands, hook-given ones included),
  `config-get`, `statistic-get-all` (including
  `subnet[1].total-addresses = 51`, the pool's real size), an
  unknown command refused with result 2, and a plain GET
  answered HTTP 400 (t06).
- The lease database worked end to end: `lease4-get` on an
  empty database (result 3), `lease4-add` of a lease,
  retrieval by address and by hardware address,
  `lease4-get-all`, `stat-lease4-get` (51 total, 1 assigned),
  a refused add outside the subnet (result 4), the lease's
  row in the on-disk memfile CSV, and its deletion followed
  by a clean "not found" (t07, t09). One observation is
  reported exactly as seen: the add asked for a 3600-second
  lifetime and the stored lease carries the configuration's
  7200.
- `kea-admin` against the memfile: `db-version` NOT
  IMPLEMENTED, `lease-dump` not supported, `stats-recount`
  reporting that memfile keeps no statistics — the tool's
  real weight is on the SQL backends, and the guide says so
  (t08).
- Shutdown by API command, the agent's subsequent "server is
  likely to be offline" answer, and a full teardown: no Kea
  process remains, and neither port 67 nor the agent's port
  is bound (t09).

Documented only — described from the project's documentation
and the protocol (RFC 2131), not run, and the text does not
claim otherwise:

- **The client lease exchange itself** (DISCOVER / OFFER /
  REQUEST / ACK over the wire, renewals at T1/T2, DECLINE and
  RELEASE), for the sandbox reasons measured in t02 and t09.
  Chapter 6 teaches it as protocol, flagged at its head.
- The fulfilment of the lab's reservation (an OFFER of the
  reserved address) — the reservation is verified as parsed
  configuration and as present in the running server's
  `config-get`, but the `reservation-*` API commands come
  from a hook library not in the open-source packages.
- MySQL and PostgreSQL lease and hosts backends, `kea-admin`
  against them, and migrating leases between backends
  (recipe 4 follows the documented commands).
- High-availability pairs (the `libdhcp_ha` hook is installed
  but was not configured or run), DHCPv6 service, the DDNS
  daemon's DNS updates (installed, version-checked, not
  exercised), control-agent authentication and TLS, and
  `config-set`/`config-test` over the wire (the file-based
  `-t`/`-T` equivalents were run instead).
- The neighbour tools of chapter 12 — characterised, not run.
- `keama`, the ISC DHCP migration assistant (recipe 2):
  named and its workflow described from its documentation;
  the lab had no dhcpd.conf to translate.

Fixtures are this guide's own and deliberately generic: the
loopback network, invented hardware addresses in the
locally-administered 02:00:00 range, hostnames like
`lab-laptop` and `reserved-gadget`, and the domain
`lab.example`. Nothing here is modelled on a real network.
