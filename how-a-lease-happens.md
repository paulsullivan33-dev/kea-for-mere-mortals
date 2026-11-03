# How a Lease Happens

**Outcome: you can narrate the four-packet
exchange that turns a stranger into a
leaseholder, say what the timers inside a
lease make a client do, and list the ways
a lease ends.**

> **Honesty note.** In this guide's lab the
> exchange below could not be run: the
> sandbox refuses all UDP sending (t02),
> and Kea will not open a raw socket on
> loopback (t09). The lab built a genuine
> DISCOVER packet and decoded it byte by
> byte (t05); the rest of this chapter is
> taught from the protocol (RFC 2131) and
> Kea's documentation, and does not pretend
> otherwise. The lease database the
> exchange *produces* is exercised for real
> in chapter 10.

## The four packets

A client that needs an address has none —
so the first packet is a broadcast, a shout
to everyone on the network:

1. **DISCOVER** — "I am hardware address
   `02:00:00:00:00:01`, I have nothing, is
   anyone handing out addresses?" Clients
   send it from port 68 to port 67, with
   the **broadcast flag** set when they
   cannot yet receive a unicast answer.
2. **OFFER** — a server that heard it picks
   a free address from a pool in the right
   subnet (or the reservation for that
   hardware address, chapter 8) and offers:
   "you could be 127.0.1.100, for two
   hours, with these extras." An offer is
   not yet a lease — with two servers on a
   network a client may collect two offers.
3. **REQUEST** — the client broadcasts its
   choice: "I accept 127.0.1.100 from that
   server." Broadcasting it tells the other
   server, politely, that its offer was not
   taken and the address can go back in
   the pool.
4. **ACK** — the chosen server records the
   lease in its database and acknowledges.
   Only now does the client configure its
   interface and start using the address.

Four packets, and every part of Kea's
configuration exists to serve one of them:
pools exist for step 2, reservations
override step 2, option data rides steps 2
and 4, and the lease database is written
at step 4.

## Inside the DISCOVER

The lab built one, byte by byte
(`kea-lab/dhcp_discover.py`, t05). A DHCP
packet is the old BOOTP frame plus options:
a one-byte operation code (1 = request from
a client), a transaction ID the client
chooses so it can match replies to its
question, the client's hardware address in
the `chaddr` field, then the four-byte
"magic cookie" `63 82 53 63` that marks the
options as DHCP's, and finally the options
themselves — option 53 first, the message
type: `1` for DISCOVER, `3` for REQUEST,
and so on. The lab's packet asked, in its
parameter-request list (option 55), for
subnet mask, routers and DNS servers — the
extras the client wants on the slip.

## The timers inside a lease

An ACK carries more than an address. It
carries the lease's lifetime and two
appointments, and chapter 4's configuration
set all three: a **valid lifetime** of
7200 s, a **renew timer (T1)** of 3600 s,
and a **rebind timer (T2)** of 6300 s —
T1 at half the lifetime and T2 at
seven-eighths, the traditional fractions.

- At **T1**, the client asks the server
  that leased it, directly, to renew.
  Normally the ACK comes back and the
  clock restarts. You will never notice
  this happening; that is the point.
- If nobody answered by **T2**, the client
  stops being polite and broadcasts a
  request to *any* server that can vouch
  for the address.
- At the **end of the lifetime**, unanswered,
  the lease is dead: the client must stop
  using the address and start again at
  DISCOVER. The server, for its part, marks
  the lease expired and eventually
  **reclaims** it — Kea's word for putting
  the address back in the pool, a process
  you can watch in its statistics.

## The other ways a lease ends

- **RELEASE** — a client shutting down
  gracefully may hand the address back
  early. Many don't bother; expiry does
  the job instead.
- **DECLINE** — a client that discovers its
  offered address is already in use (it
  checks, by ARP) declines it. Kea puts a
  declined address on probation — the
  `decline-probation-period`, a day by
  default — rather than offering a possibly
  poisoned address to the next stranger.
- **NAK** — if a client asks to renew an
  address the server knows is wrong for it
  (it moved networks, say), the server
  refuses with a NAK and the client starts
  over.

With the exchange in mind, the rest of the
guide is about everything the server does
around it: choosing addresses (chapter 7),
promising them (chapter 8), and being
asked afterwards what it did (chapters 9
and 10).
