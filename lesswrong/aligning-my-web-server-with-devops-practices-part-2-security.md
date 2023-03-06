# Aligning my web server with devops practices: part 2 (security)

This is a continuation of my [previous
post](https://www.lesswrong.com/posts/Efj8NCCv3TqDL5mbC/aligning-my-web-server-with-devops-practices-part-1-backups). See
the introduction at the top of the previous post to get more
information on what this series of posts is about.

This post focuses on devops practices I adopted to secure my web server.

## General philosophy of security

### Security against leakage versus security against manipulation

Some aspects of security are about preventing information from leaking
out. Other forms of security are about preventing others from being
able to *modify* the behavior of the server or impersonate the server
to modify the expected behavior for others (e.g., serving their own
website in place of mine).

For a web server, the latter kind of security is more relevant, but
the former also matters since in at least some cases, the source code
of a public website is not public (and may contain information that
shouldn't be public).

### Security even conditional to partial compromise

I conceptualize security as being about layers of defense against
attackers, both intentional attackers and accidental intruders. To my
mind, security is about being able to make strong statements of the
form "Even if A is broken/misconfigured/compromised, B will still not
be compromised" where A and B are "near" each other in some sense. So,
security isn't just about having a strong outer defense, but also
about inner decoupling to the extent possible.

## Firewall / security group

This is relevant both for security against leakage and for security
against manipulation.

Here, in the language of "Even if A is
broken/misconfigured/compromised, B will still not be compromised", we
have:

* A = misconfigured or vulnerable service running on the web server
* B = outsiders can take advantage of the misconfiguration

### The concept of firewall / security group: an outer layer of defense

A firewall is an outer layer of defense on a server that gates
incoming and/or outgoing traffic based on conditions. The conditions
are generally specified in terms of the *port* on the server that is
being communicated with, and the *IP range* of outside machines that
are allowed or not allowed to communicate.

Amazon Web Services (AWS) uses the term "security group" for the same
idea, so if you mainly use AWS you should be on the lookout for
security groups.

#### Ports for firewall

A port is a virtual endpoint on a server, assigned a numeric label, at
which it sends and receives messages from or to other servers. The
numeric labels of ports range from 0 to 65,535. A few specific numeric
values of ports have particular significance: for instance, 22 is used
for SSH, 80 for plain HTTP, and 443 for HTTPS. The bulk of the numbers
are not assigned any meaning, though there are conventions governing
typical usage pattern (for instance, 9000 is often used for local
applications such as PHP, 3306 is often used for MySQL or similar
applications). Here's
[Wikipedia](https://en.wikipedia.org/wiki/Port_(computer_networking))
on ports, and here's
[CloudFlare](https://www.cloudflare.com/learning/network-layer/what-is-a-computer-port/).

### IP ranges for firewall

A port-based firewall rule specifies, for a given port, what IP
addresses are allowed and not allowed to access that port. There's a
language to express this concisely (called [CIDR
blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)).

### What firewall policy makes sense?

#### First approximation: only allow ports 80 (HTTP) and 443 (HTTPS)

The main way I expect people to use my server is for *web serving*. So
outsiders shoud only need to access the ports needed to access
webpages, which is 80 for HTTP and 443 for HTTPS. So to a first
approximation, I want to allow access for everybody to ports 80 and
443, and allow access for nobody to other ports.

This is the case even though there are other services running on other
ports! For instance, MySQL may be running on port 3306. But
*outsiders* don't need to directly connect to MySQL! And they should
not. The MySQL port is only intended for internal serving. The
firewall is only for traffic coming from outside, not local traffic
within the server, so it shouldn't disrupt the server's ability to run
other services locally on other ports.
 
#### Adjustment for SSH

I want to be able to SSH into my web server. SSH is over port 22, so I
want to leave port 22 open. But ideally, only for IP addresses I
expect to be using (SSH is also gated by secret credentials, not just
IP address, but having IP address as an additional mechanism helps
filter out password hacking attempts). So, I add a firewall rule
allowing access to port 22 from a hand-crafted list of IP addresses
that are locations I use regularly. I may need to edit this list
occasionally.

#### Adjustment for ping

I like to be able to ping my server. Ping actually doesn't go through
a numbered port, but instead uses a more primitive protocol called
ICMP. I have a firewall rule that basically allows for free ping
access.

#### Blocking everything else

Any traffic that doesn't match any of the criteria above gets blocked.

#### Blocking spam traffic

Although this isn't directly a security issue, I also use the firewall
on occasion to block very clear IP-based patterns of spam traffic on
HTTP and HTTPS ports (that are otherwise open to everybody).

### Summary of firewall policy currently in use

* It allows access for all IP addresses (except a few IP addresses
  known for spam traffic) to ports 80 (the HTTP port) and 443 (the
  HTTPS port). My servers run nginx that listens to these ports.

* It allows access to port 22 (SSH) *only* from a few IP addresses
  that I use (such as my home and office IP address). This means that
  if a hacker figured out my SSH username and password, that person
  still couldn't get on the machine.

* It allows ping access from arbitrary locations.

If you're used to Amazon Web Services (AWS) you would have seen the
same idea encapsulated in AWS's concept of [security
groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html).

### Does a firewall really matter? Yes!

There are bots constantly running, checking for combinations of server
and port that are open to traffic from the Internet. Many of these
bots are malicious: once they find a server with an open port, they'll
check if what's running behind the port is some known software (such
as Redis, or PHP, or MySQL) and whether it is possible to send it
instructions, or hack into it, to achieve the bot's own goals. This
process is called "port scanning"; see
[here](https://security.stackexchange.com/questions/120711/why-do-hackers-scan-for-open-ports)
for instance.

Some bots just want compute to run their own crypto mining (this is
harmless except to the extent that it competes with your server's
resources), some bots will try to access files on your server to see
if they can read secret credentials that can open up access to other
stuff, and some bots will try to take over the site and serve their
own spam.

Now, in principle, when starting a service on a port, you can
explicitly restrict it to listen *only* to localhost on that port, and
therefore to *not* respond to outsiders who send messages on that
port. For instance, you can start MySQL on port 3306 to only listen to
localhost connections on port 3306, or start PHP-FPM on port 9000 to
only listen to localhost connections on port 9000. That way, even
without a firewall, there are no unintended open ports for outsiders
to use.

But making sure of this requires care with *every* service, and it's
possible to slip up at some point (or to not have the ability to
configure some software). A firewall, as an *outer* layer of defense,
prevents any such misconfiguration from having a negative impact.

#### In the real world: a dev server of mine got reliably taking over by a crypto miner

When playing around with configurations for a dev server, I
accidentally started PHP-FPM on port 9000 open to the world (rather
than just to localhost, as I intended). Nothing went wrong
immediately, but within a few hours to a few days, nearly all the CPU
on the server was being used by the Kinsing malware for some crypto
mining purposes. Fortunately, this was a dev server, not identified
with me, and the bot did nothing else to the server, so the impact on
me was limited. But this was a cautionary tale and I immediately
worked on setting up the firewall -- something I should have done to begin with!

#### Also in the real world: MySQL installations open to the world

I've heard of a couple of cases where MySQL installations that had a
weak or empty root password set by default were predictably hacked
into.

### My recommendation for others: use a firewall even if you're not sure

Using a firewall to lock down most ports dramatically reduces the risk
surface area to a few specific ports that are being served by the
software you are focused on (in this case, nginx). You don't have to
worry as much about accidentally exposing other ports to strangers.

## Unique credentials

I make sure that each server I setup (whether the production server or
a new test server) has its own unique:

* AWS credentials
* GitHub credentials

This is so even though the set of permissions for AWS or for GitHub is
identical across the servers. Having separate credentials means that
if one server gets compromised, its credential can be rotated without
affecting other servers.

## Separate users for web processes, and limited permissions for these users

### Separate users for web processes

I run the Nginx and PHP processes using users that are separate from
each other and also separate from my main user. The users running the
Nginx and PHP processes have only the very limited access to files
needed for the web; in particular, they don't have write access to
most files, and they have read access to only the files needed for
front-facing stuff. This is to limit what a hacker can do even if the
hacker is somehow able to execute arbitrary PHP commands.

The reason to separate the Nginx and PHP users from each other is
partly security, but also partly more ease of diagnosis of what's
going on (any activity reported to a user can be traced to the
respective process).

### File permissions

All the automatic scripts that I've written to set up new sites
include steps to make sure that the files readable by others are just
the ones that are needed for the web processes.

In addition, I've set `umask` settings so that any files I create
through the command line on the server will get the default of not
being readable, writable, or executable by the users running the Nginx
or PHP processes. Note that this means that if I manually fetch git
changes on the command line, the files may end up getting overly
restrictive permissions and I would need to manually fix the
permissions for the site to continue working.

### Database permissions

The web user has access to the configuration file containing the MySQL
username and password that can be used to access the databases needed
to serve various sites. However, unless specifically needed for the
site, this user only has read permissions for the
database. Operationally, this translates to privileges to select, lock
tables, and show view. The user does not have the permission to insert
or delete. Morever, the username/password is different for each site,
so any bug affecting a specific site is limited to the database for
that site.

For some sites, the end user's actions can lead to data updates in
MySQL, and in these case, we do need to give at least some level of
write access.
