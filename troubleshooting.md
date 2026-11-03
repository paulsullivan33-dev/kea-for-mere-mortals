# Troubleshooting

The traps, in roughly the order a new
operator meets them. Every entry here was
met by the lab (transcript named) or is a
direct consequence of something it ran.

## The server will not start at all

- **Missing directories.** Without systemd,
  `/run/kea`, `/var/lib/kea` and
  `/var/log/kea` may not exist; the daemon
  needs all three. Create them (chapter 3).
- **The configuration was never checked.**
  Run `kea-dhcp4 -t` and then `-T` on the
  exact file the daemon will read. Most
  "will not start" is a config error with
  the answer spelled out in the checker's
  output — including the position in the
  file.
- **Port 67 is taken.** Something else is
  already the DHCP server on that interface
  — the lab met this through perfdhcp,
  which failed to bind 127.0.0.1:67 because
  the real server held it (t05). `ss -lunp`
  names the holder. One address desk per
  network: stop the other one on purpose,
  never by accident.

## `output-options` — the underscore trap

The loggers section wants **`output_options`**
with underscores. Write it with hyphens
like everything else in the file and the
checker refuses it: *"got unexpected keyword
"output-options" in loggers map"*, exit 1
(t03). The lab wrote it wrong first, on
purpose in hindsight. It is nearly the only
underscore in the language; now you know.

## Running, but no client ever gets an address

Work the chain the way chapter 5 taught it:

1. **Is it listening?** `ss -lunp | grep :67`,
   and `DHCP4_STARTED` in the log. A server
   that started with raw sockets on the
   loopback interface is running but deaf:
   look for `DHCPSRV_OPEN_SOCKET_FAIL … must
   not open socket on the loopback interface
   lo` (t09). Raw sockets are for real
   interfaces; loopback serving needs
   `"dhcp-socket-type": "udp"` — and on a
   real network, use raw.
2. **Is it being asked?** `statistic-get-all`
   and read `pkt4-discover-received`. Zero
   with awake clients means the requests are
   not arriving — interface wrong, relay
   wrong, or another server answering
   first.
3. **Is the pool plausible?** `subnet[N].total-addresses`
   in the same answer. A pool outside its
   subnet fails at the checker (t03); a pool
   of zero size fails only your clients.
4. **Is the address already promised?** A
   reservation conflict does not refuse the
   reserved client — it gives it a pool
   address for now and counts
   `v4-reservation-conflicts`. If a machine
   "keeps changing address," this counter
   and chapter 8 are where to look.

## The API answers… strangely

- **`result: 3, "Lease not found."`** is not
  an error in your call; it is the answer
  "no such lease" (t07). Learn the codes:
  0 success, 1 general error, 2 unsupported
  command, 3 not found, 4 a refused request
  with the reason in `text`.
- **A command you expect is missing.**
  Commands come from hooks. No
  `libdhcp_lease_cmds` in `hooks-libraries`,
  no `lease4-*` commands — `list-commands`
  shows the truth about the running server
  (t06).
- **The agent says the server is offline.**
  After a `shutdown`, `version-get` returns
  "unable to forward command to the dhcp4
  service… The server is likely to be
  offline" (t09). The agent is a forwarder:
  when it cannot connect, the fault is
  downstream — check the daemon, not the
  agent.
- **A plain GET returns HTTP 400.** The
  agent speaks POSTed JSON only (t06).

## The lease you added is not the lease you asked for

The lab's `lease4-add` asked for a
3600-second lifetime and the stored lease
carried the configuration's 7200 (t07).
Read records back with `lease4-get` after
any change and trust the record, not the
request — the configuration's values win
in more places than that one.

## kea-admin says NOT IMPLEMENTED / not supported

Against a memfile database that is the
correct answer, not a fault: no schema to
version, no dump to make from a file that
is already a dump (t08). kea-admin's real
work is on the SQL backends.

## And the meta-trap

The commonest Kea fault needs no error
message at all: **the file was edited and
the server was never told.** `config-get`
(chapter 9) shows the configuration the
server is *running*. When behaviour and
file disagree, believe the server — then
restart it, or better, `config-test` and
`config-set` the new configuration in
through the API.
