# The Configuration File

**Outcome: you can read a Kea configuration
top to bottom, write a small one of your
own, and prove it valid with Kea's own
checker before any server runs it.**

Kea is configured, one JSON file per
daemon. JSON with a kindness: `//` and
`/* */` comments are allowed, and the
shipped `/etc/kea/kea-dhcp4.conf` uses them
as documentation. Here is the lab's working
configuration, the one the rest of the
guide runs (kept at
`kea-lab/config/kea-dhcp4-lab.conf`):

```json
{
"Dhcp4": {
    "interfaces-config": {
        "interfaces": [ "lo" ],
        "dhcp-socket-type": "udp"
    },
    "control-socket": {
        "socket-type": "unix",
        "socket-name": "/run/kea/kea4-ctrl-socket"
    },
    "lease-database": {
        "type": "memfile",
        "persist": true,
        "name": "/var/lib/kea/kea-leases4.csv",
        "lfc-interval": 3600
    },
    "valid-lifetime": 7200,
    "renew-timer": 3600,
    "rebind-timer": 6300,
    "hooks-libraries": [
        { "library": "/usr/lib/x86_64-linux-gnu/kea/hooks/libdhcp_lease_cmds.so" },
        { "library": "/usr/lib/x86_64-linux-gnu/kea/hooks/libdhcp_stat_cmds.so" }
    ],
    "subnet4": [
        {
            "id": 1,
            "subnet": "127.0.0.0/8",
            "interface": "lo",
            "pools": [ { "pool": "127.0.1.100 - 127.0.1.150" } ],
            "option-data": [
                { "name": "routers", "data": "127.0.0.1" },
                { "name": "domain-name-servers", "data": "127.0.0.1" },
                { "name": "domain-name", "data": "lab.example" }
            ],
            "reservations": [
                {
                    "hw-address": "02:00:00:00:00:01",
                    "ip-address": "127.0.1.50",
                    "hostname": "reserved-gadget"
                }
            ]
        }
    ],
    "loggers": [
        {
            "name": "kea-dhcp4",
            "output_options": [ { "output": "/var/log/kea/kea-dhcp4.log" } ],
            "severity": "INFO"
        }
    ]
}
}
```

## Reading it in order

- The whole file is one object named for
  the daemon: `Dhcp4` (the control agent's
  file is `Control-agent`).
- **`interfaces-config`** says which network
  interfaces to serve on, and how to open
  sockets. The default socket type is
  `raw` — what a real network needs —
  and the lab's `udp` choice is explained
  in chapter 5.
- **`control-socket`** is where commands
  arrive (chapter 9). No socket configured,
  no remote control.
- **`lease-database`** picks the backend.
  `memfile` with `persist: true` means
  leases survive a restart, in the CSV
  file named.
- **The timers** are the lease terms:
  `valid-lifetime` 7200 s (two hours),
  with `renew-timer` (T1) at half of it
  and `rebind-timer` (T2) at seven-eighths
  — chapter 6 explains what clients do
  when those alarms ring.
- **`hooks-libraries`** loads extensions by
  full path. Nothing in Kea answers lease
  commands until `libdhcp_lease_cmds` is
  listed here — the configuration *is* the
  feature switch.
- **`subnet4`** is the heart: an array of
  networks served, each with a numeric
  `id`, a `subnet` in CIDR form, `pools`
  to hand out, `option-data` extras, and
  any `reservations`. Chapter 7 gives this
  section its own chapter.
- **`loggers`** decides where the words go.
  Note the name of the inner key:
  **`output_options`, with underscores** —
  one of the very few places Kea does not
  use hyphens. The lab's first draft used
  `output-options` and the checker below
  rejected it, at a named position in the
  file. Remember it; chapter 13 does too.

## Checking before trusting

Kea will test a configuration without
serving it, in two depths:

```bash
$ kea-dhcp4 -t kea-dhcp4-lab.conf     # syntax and sense
(exit 0, with the subnets and socket choices echoed in the log)
$ kea-dhcp4 -T kea-dhcp4-lab.conf     # also loads hooks, opens the lease DB
```

Run both, every time, before a restart.
They catch different things, and `-T` is
the honest rehearsal: it loads the hook
libraries and opens the lease database,
then puts everything away again.

And they fail usefully. The lab's
deliberately broken file put a pool of
`10.9.9.100 - 10.9.9.150` inside subnet
`127.0.0.0/8`:

```text
DHCP4_PARSER_FAIL ... a pool of type V4, with the following
address range: 10.9.9.100-10.9.9.150 does not match the prefix
of a subnet: 127.0.0.0/8 to which it is being added
```

Exit code 1, the problem named in plain
words, the position in the file given.
That error is the configuration chapter in
one line: Kea refuses to run nonsense, and
tells you exactly which nonsense. The full
runs are t03. Next, the server starts.
