# The Neighbours

Kea is not the only program that can hand
out addresses. Each of these does something
Kea doesn't, and vice versa; the honest
question is which size of problem you have.

## The router in the cupboard

Almost every home router contains a small
DHCP server, on by default, configured by
checkbox and two fields. **Its virtues are
real**: it exists, it works, it needs no
maintenance, and for a house of phones and
laptops it is genuinely enough. What it
cannot give you is everything this guide
did after chapter 5: no inspectable lease
database, no API, no statistics worth the
name, reservations limited to whatever the
web page allows, and a configuration that
lives and dies with the router. The
Home Networking guide in this series is
the place to run a home network on purpose;
Kea is one of the tools for doing it.

## dnsmasq

The small multi-tool: DNS forwarder and
DHCP server in one tiny program, configured
in one flat file, beloved of home labs and
small offices. dnsmasq hands out addresses
perfectly well, does reservations by MAC in
one line, and pairs them with DNS names
automatically — a trick Kea needs its DDNS
daemon and a cooperating DNS server to
match. For one subnet and one admin it is
often the right answer. Kea pulls ahead
where dnsmasq stops: separate daemons and
real databases, high availability, an API,
statistics, and configuration that scales
past one file's comfort.

## ISC DHCP (dhcpd)

Kea's ancestor, end-of-life since 2022.
If you are running it, it still works —
and it is receiving no fixes. Its
configuration language is more expressive
than Kea's JSON (arbitrary conditionals,
classes, a failover protocol of its own),
which is both its charm and the reason
migration is a translation exercise
(recipe 2) rather than a file rename.
New installs should not start here.

## systemd-networkd and friends

Linux's built-in network manager has a
small DHCP server mode, aimed at the
"share this connection" and virtual-machine
host cases. It is tidy for a bridge that
needs to feed its guests and nothing more.
It is not trying to be a network's address
desk, and read that way it is fine.

## Windows Server DHCP

The incumbent in Microsoft shops: a
full-featured server with a graphical
console, Active Directory integration,
policies, and failover, licensed with the
server it runs on. In a Windows estate it
is the natural default and a capable one.
Kea's counter-offer is the Linux/Unix
world, the text-file configuration, and
the API — estates choose their own
gravity.

## The pattern

Notice the shape of the field: the
neighbours are either *smaller* (router,
dnsmasq, networkd — DHCP as a feature
inside something else) or *the platform's
own* (Windows). Kea is the one that is a
standalone, cross-platform, API-driven
DHCP service and nothing else — which is
exactly what you want when addresses have
become infrastructure, and complete
overkill when they haven't.
