# Working with Leases

**Outcome: you can read, add, count and
remove leases in a running server through
its API, find them again in the on-disk
memfile, and know what the offline tool
kea-admin can and cannot do.**

A lease is Kea's unit of memory. The
exchange of chapter 6 creates them; this
chapter is about everything you can do with
them afterwards — and it is all live in the
lab, because leases manipulated through the
control channel are the same records the
packet exchange would have written.

## The lease commands

They exist only because the configuration
loads `libdhcp_lease_cmds` (chapter 4); the
family includes `lease4-add`, `lease4-get`,
`lease4-get-all`, `lease4-get-by-hw-address`,
`lease4-get-page`, `lease4-update`,
`lease4-del`, `lease4-wipe` and more. The
lab's run is t07; the story in brief:

**Ask before there is anything:**

```text
$ POST lease4-get  {"ip-address": "127.0.1.120"}
[ { "result": 3, "text": "Lease not found." } ]
```

Result 3 — promised in chapter 9 — is the
API's clean "no."

**Add a lease directly**, as an operator
might to seed or repair one:

```json
{ "command": "lease4-add", "service": ["dhcp4"],
  "arguments": { "ip-address": "127.0.1.120",
                 "hw-address": "02:00:00:00:00:42",
                 "hostname": "lab-laptop",
                 "valid-lifetime": 3600,
                 "subnet-id": 1 } }
```

```text
[ { "result": 0, "text": "Lease for address 127.0.1.120, subnet-id 1 added." } ]
```

**Read it back**, by address or by hardware
address — both return the full record:
client's last transaction time (`cltt`),
hostname, state, subnet, and lifetime.
One detail the lab noted with its eyebrows
up: the command asked for a 3600-second
lifetime and the recorded lease carries
**7200** — the `valid-lifetime` from the
configuration. The stored record, not the
request, is the truth; check it, don't
assume it.

**Count them**, two ways. `stat-lease4-get`
(from the statistics hook) reports the
subnet's table — 51 total addresses, 1
assigned — and `statistic-get-all`
(chapter 9) agrees. **Try to cheat**: an
add for `10.9.9.9`, outside subnet 1, is
refused with result 4 and the reason in
words. **Delete**, and the get that found
it a minute earlier answers "Lease not
found" again (t09).

## The memfile: the database you can read

With the memfile backend the lease database
is a CSV file, and the lease added above
appears in it as a row (t07):

```csv
address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context,pool_id
127.0.1.120,02:00:00:00:00:42,,7200,1793676504,1,0,0,lab-laptop,0,,0
```

Everything the API said is here: address,
hardware address, lifetime, the expiry as a
Unix timestamp (last-transaction time plus
lifetime), subnet, hostname, state
(0 = default, i.e. an ordinary live lease).
Reading the file is a legitimate inspection
method; *editing* it while the server runs
is not — the server holds the truth in
memory and rewrites the file itself (the
`kea-lfc` helper tidies it periodically).
Change leases through the API, or with the
server stopped.

## kea-admin: the offline tool, sized honestly

`kea-admin` works on lease databases
directly: `db-init`, `db-version`,
`db-upgrade`, `lease-dump`, `lease-upload`,
`stats-recount`. The lab aimed it at the
memfile and got short, honest answers
(t08): `db-version` is *not implemented*
for memfile — a CSV has no schema version;
`lease-dump` is *not supported* for memfile
— the file is already the dump; and
`stats-recount` reports that memfile keeps
no statistics of its own.

That is the tool's shape: **kea-admin
earns its keep with the SQL backends** —
initialising a MySQL or PostgreSQL lease
database, upgrading its schema when Kea
upgrades, and dumping leases out of (or
uploading them into) a database in
memfile-ready CSV form, which is how you
migrate between backends (chapter 11's
recipes use exactly that). Against memfile
it mostly confirms there is nothing for it
to do, and there is a lesson in that:
reaching for the offline tool when the API
would answer is operating the hard way.
