# The Control Channel and the REST API

**Outcome: you can interrogate a running
Kea server — its version, its status, its
live configuration, its statistics — and
even stop it, all by command, without
touching its configuration file or its
leases.**

This chapter is where Kea most differs from
the DHCP servers that came before it, and
it is the chapter the lab could exercise in
full: the control channel is a Unix socket
and plain TCP, neither of which the sandbox
restricts.

## The shape of every command

A command is a small JSON document:

```json
{ "command": "version-get", "service": [ "dhcp4" ] }
```

- `command` — the verb;
- `service` — which daemon(s) it is for
  (the control agent uses this to route);
- `arguments` — the command's inputs,
  when it has any.

The answer is a JSON list with one entry
per service, each carrying a `result` code
(0 = success; 1 = a general error; 2 = the
command is not supported; 3 = a thing you
asked for was not found — remember 3, it is
chapter 10's "Lease not found"), a
human-readable `text`, and often an
`arguments` object with the payload you
actually wanted.

## The control agent

Each daemon opens its own Unix socket —
`/run/kea/kea4-ctrl-socket` for dhcp4 in
the lab's config. Speaking to Unix sockets
directly is a local administrator's job
(`kea-shell` wraps it). For everything else
there is the **control agent**: one small
HTTP server whose own configuration file
names the port and the sockets it forwards
to. The lab's (`kea-lab/config/kea-ctrl-agent-lab.conf`)
puts it on `127.0.0.1:18081` and wires only
dhcp4:

```json
{
"Control-agent": {
    "http-host": "127.0.0.1",
    "http-port": 18081,
    "control-sockets": {
        "dhcp4": { "socket-type": "unix",
                   "socket-name": "/run/kea/kea4-ctrl-socket" }
    },
    ...
}
}
```

It is checked like any Kea config —
`kea-ctrl-agent -t` — and started like any
Kea daemon. It answers only POSTs of
command documents; a plain GET earns an
HTTP 400 (t06). Options the lab did not
enable, and a real deployment should know
exist: **basic authentication** and **TLS**
on the agent, so the HTTP door is not an
open one. An unauthenticated control agent
is a remote control for your network's
address desk — bind it to loopback or a
management network, and give it a password.

## The commands the lab ran

All of them are in t06, using payload files
kept in `kea-lab/config/cmd-*.json`:

- **`version-get`** — the running server's
  version and build report. The first check
  when a server behaves strangely: is the
  running binary the one you think?
- **`status-get`** — pid, uptime, thread
  and queue state, and whether its sockets
  report `ready`.
- **`list-commands`** — every command the
  server, *with its loaded hooks*, supports.
  The lab's answer ran to fifty verbs; the
  `lease4-*` family is in it because the
  lease-commands hook is in the config.
  Diff this list before and after a hook
  change and you will never wonder whether
  a hook loaded.
- **`config-get`** — the entire running
  configuration, defaults filled in. This
  is the ground truth of chapters 7 and 8:
  the server may have been reloaded since
  the file changed; the file is an opinion,
  `config-get` is the fact.
- **`statistic-get-all`** — every counter:
  packets by type (all zero in the lab —
  the counters are the lab's negative
  evidence that no exchange slipped past
  it), and per-subnet totals, including
  `subnet[1].total-addresses = 51`, the
  pool's true size.
- **`config-test`** and **`config-set`** —
  the careful way to change a running
  server: test a candidate configuration
  over the wire, then apply it without a
  restart. The lab verified its file with
  `-t`/`-T` instead (chapter 4) and left
  the over-the-wire pair described here —
  on a production server, prefer them:
  no restart, no blind moment.
- **`shutdown`** — the server stops itself,
  by command (t09). Send `version-get`
  afterwards and the agent answers for it:
  "unable to forward command to the dhcp4
  service… The server is likely to be
  offline" — the agent outlives the server
  and says so, which is exactly what you
  want a status page to do.

## The one-sentence summary

If you take one habit from this chapter:
**when Kea surprises you, ask it** — its
version, its config, its counters — before
you restart it. The answer is one POST
away, and it is the truth about the server
that is actually running.
