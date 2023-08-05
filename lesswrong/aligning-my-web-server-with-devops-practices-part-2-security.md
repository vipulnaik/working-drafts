# Aligning my web server with devops practices: part 2 (security)

This is a continuation of my [previous
post](https://www.lesswrong.com/posts/Efj8NCCv3TqDL5mbC/aligning-my-web-server-with-devops-practices-part-1-backups). See
the introduction at the top of the previous post to get more
information on what this series of posts is about.

This post focuses on devops practices I adopted to secure my web server.

## Recommendations for others (transferable learnings)

* If you have a server exposed to the Internet, use a firewall (or
  security group in the case of AWS) to lock access to the server as
  much as possible, limiting the ports and IP address ranges that can
  be used to access it. This drastically reduces the risk surface
  area. Even if you do nothing else, do this.

* Separate, separate, separate. Even if things get compromised up to a
  point, that shouldn't compromise everything. Keep in mind the
  concept of [defense in
  depth](https://en.wikipedia.org/wiki/Defense_in_depth_(computing))
  as you think of things.

* Related to the above: Give only as much permission to each thing as
  it actually needs; this idea is called the [principle of least
  privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
  and you may also hear of it as "right-sizing permissions" in some
  contexts.

* Security isn't just about preventing or limiting attacks, it's also
  about being able to recover more quickly and get back to a clean
  slate. Backups with streamlined restore procedures, that I covered
  extensively in [part
  1](https://www.lesswrong.com/posts/Efj8NCCv3TqDL5mbC/aligning-my-web-server-with-devops-practices-part-1-backups), help a bunch with this.

* Make sure you have good security (strong password, two-factor
  authentication, etc.) on the online accounts that you use to manage
  your servers. A secure server managed through an insecure online
  account is like a locked safe that's wide open from above.

Some time after I started drafting this post, I discovered a great
podcast called [Darknet Diaries](https://darknetdiaries.com/) that
covers a lot of security-related themes. Many of the concepts I talk
about in this post show up organically in the episodes of this
podcast, and I recommend this podcast for people interested in
security.

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

### Security even conditional to partial compromise (related: defense in depth)

I conceptualize security as being about layers of defense against
attackers, both intentional attackers and accidental intruders. To my
mind, security is about being able to make strong statements of the
form "Even if A is broken/misconfigured/compromised, B will still not
be compromised" where A and B are "near" each other in some sense. So,
security isn't just about having a strong outer defense, but also
about inner decoupling to the extent possible.

I conceptualized this before I learned the formal jargon of [defense
in depth](https://en.wikipedia.org/wiki/Defense_in_depth_(computing)),
but upon learning of that jargon I see that my concept is closely
related. Specifically, defense in depth is the idea of having multiple
enclosures or layers of defense, so that even if outer layers are
breached, inner layers are still intact. My concept of "security
conditional to partial compromise" is a local version of this general
idea.

### Separation for ease of diagnosis and for seamless rotation

When a security issue occurs, it is best if the issue is
self-containing, easy to diagnose, and easy to remediate with minimal
disruption. A key aspect of this is *separation*; even functionally
similar things should be as separate as possible so that the
responsible party for an issue can be quickly identified, the issue
remains limited in scope, and it's easy to fix the one thing causing
issues without affecting other things. A few ways this manifests
itself:

* For different servers (even if they're running similar code), I
  always put different credentials for access to third-party
  services. That way, if one server gets compromised, the credentials
  on that server can be disabled without affecting the functionality
  of other servers.

* Within the same server, I use different username/password
  combinations for access to different websites. This is the case even
  though the same web user runs the code to access all these websites,
  so that user has access to all the username/password combinations in
  principle. However, the portion of code that gets compromised could
  still be more local and specific to a particular site, so it's good
  if the damage that such a compromise could achieve is limited.

## Identifying the layers of security

### The layers for web requests

Before getting into the details, here's an effort to step back and use
the general philosophy outlined above to figure out what the next few
sections should be.

* The outermost starting point seems to be the ports through which
  users can connect to the server, so control over ports (aka
  firewalls / security groups) is the outermost security layer to
  begin with.

* With the firewall set up, the only way to access the server is
  through the front door i.e., the web processes. So the next layer of
  defense is to limit the scope of the web process. This is two-fold:
  make sure the web process is running on a user different from the
  main user, and limit the file and database permissions that the web
  user can access.

* With the web process constrained, there is now a limited range of
  damage possible, but there is still some damage possible. We're now
  in the stage where code is being run, so the next step is:

  * Secure the code I've written as much as possible

  * Update software that I use directly for web serving (MediaWiki and WordPress)

### Zooming in early on the web requests

I started by saying that the outermost starting point is the ports
through which the user hits the web server. But even before that,
there is a process by which the name of the website resolves to the IP
address. This process has two layers:

* Domain registration that points each top-level domain to the
  nameservers for the hosting service (Linode)
* DNS records that point specific domains or subdomains to specific
  servers

Securing these basically means securing the online logins through
which these are controlled. In particular, I have strong passwords for
both cases and also have 2-factor authentication for both. The online
accounts are also important as they control access to the servers
themselves, and in particular may be powerful enough to destroy or
reset settings on the servers.

### Other stuff on the side

Servers often have a bunch of supporting functions that may not
directly be part of the web request flow, but are still
important. These includes:

* The operating system and software that are necessary to keep things
  running. Vulnerabilities in the operating system or the core
  software could compromise the server, even vulnerabilities that seem
  completely unrelated to the code or content of the websites you're
  serving. Some high-profile examples of major bugs:
  [Heartbleed](https://en.wikipedia.org/wiki/Heartbleed) and
  [Shellshock](https://en.wikipedia.org/wiki/Shellshock_(software_bug)).

  This makes it particularly important that the operating system and
  core software is updated regularly. The update process should
  ideally be automated; however, at minimum it should be highly
  streamlined and checked on periodically.

* In some cases, private credentials may be needed on the server to
  connect to external services. For instance, my web server needs to
  connect with Amazon S3 to copy backup files to S3. It also need to
  connect with GitHub to clone repositories and fetch updates. These
  aren't part of a web request flow; these happen either periodically
  or as needed by me. Nonetheless, having these credentials in an
  open, readable location, or having overly generous permissions for
  these credentials, can increase the damage from a security breach.

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

#### IP ranges for firewall

A port-based firewall rule specifies, for a given port, what IP
addresses are allowed and not allowed to access that port. There's a
language to express this concisely (called [CIDR
blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)). This
language supports both specifying an individual IP address and
specifying "all IP addresses" at once, as well as a bunch of stuff in
between.

Although not super-easy, [IP address
spoofing](https://en.wikipedia.org/wiki/IP_address_spoofing) is
possible, i.e., an attacker may be able to, in some cases, pretend to
be coming from an IP address that's different from the attacker's
actual IP address. Conversely, it's also possible that the IP address
of a legitimate entity changes. So, when thinking about IP ranges,
keep in mind:

* Use the IP address only as an additional/secondary form of
  verification and not as a primary method of authentication.

* Be prepared to have to log in and edit the firewall when IP ranges
  change.

### What firewall policy makes sense?

#### First approximation: only allow ports 80 (HTTP) and 443 (HTTPS)

The main way I expect people to use my server is for *web serving*. So
outsiders should only need to access the ports needed to access
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
the ports 80 (for HTTP) and 443 (for HTTPS).

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
worked on setting up the firewall -- something I should have done to
begin with!

#### Also in the real world: MySQL installations open to the world

I've heard of a couple of cases where MySQL installations that had a
weak or empty root password set by default *as well as having the port
open to the world* were predictably hacked into. In some cases this
was right around the time the server was being set up (so hadn't had
time to switch away from default credentials) whereas in others the
server had been left idle with default credentials.

I am not alone; see this excerpt from [Darknet Diaries podcast episode
#88 (Victor)](https://darknetdiaries.com/transcript/88/):

> JACK: Here’s the basic process; databases run on a certain port, so
> MySQL, for example, runs on port 3306, and so he could just scan the
> internet or use a website like Shodan to first look for any IPs that
> have port 3306 open.  Then once he finds that, he’ll try default
> usernames and passwords or maybe a handful of very weak passwords
> like the word ‘password’ to see if that’s it.  Yeah, from this
> alone, he was tripping over tons of open databases.  Some didn’t
> even have passwords at all.  Then they’d tell all the database
> owners that their stuff is insecure.  As their efforts grew, so did
> the number of people pitching in to help GDI.  [MUSIC] In the
> beginning, it was just Victor and his friends but almost fifty
> different volunteers have joined on [00:10:00] in the last five
> years.  In that time, the foundation has filed coordinated
> vulnerability disclosures on over a million security issues out
> there on the internet.

### My recommendation for others: use a firewall even if you're not sure

Using a firewall to lock down most ports dramatically reduces the risk
surface area to a few specific ports that are being served by the
software you are focused on (in my case, web-serving software
nginx). You don't have to worry as much about accidentally exposing
other ports to strangers.

Further, for ports that need to be accessible only to specific people
(in my case, the SSH port that only needs to be accessible to me),
using firewall rules to restrict the IP ranges that can access those
ports, further reduces the risk surface area.

## Separate users for web processes, and limited permissions for these users

In the language of "Even if A is
broken/misconfigured/compromised, B will still not be compromised", we
have:

* A = access to users running web processes (basically, the ability to execute arbitrary shell commands as such users)
* B = access to sensitive behind-the-scenes information, including credentials

The concept of limited permissions for web users is a special case of
the more general idea of the [principle of least
privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege).

### Users running web processes are vulnerable, so strong separation is desired

In the previous section, we talked about using firewalls to lock down
everything except the ports 80 and 443 that serve web traffic. A web
server does need to have those ports open, and the service running on
those ports, that serves the traffic, is a point of vulnerability. In
the case of my web server, I run nginx, proxying to other backends
(PHP-FPM in most cases). An error in the configuration of nginx, or of
PHP-FPM, or of the code running any of the websites, can potentially
create an opportunity for a clever end user to be able to execute
arbitrary commands as the users running these processes
(cf. [cross-site
scripting](https://en.wikipedia.org/wiki/Cross-site_scripting) or the
more general concept of [code
injection](https://en.wikipedia.org/wiki/Code_injection)).

So the next line of defense is to make sure these users, even if
compromised, have limited ability. Unfortunately, they *do* need some
level of access to be able to do a good job serving the websites. The
goal here is to make sure that they don't have any more access than
they need. In particular, they should not have the ability to modify
or write things they just need to read, and they also shouldn't need
to read things that aren't directly relevant for web serving (for
instance, a credential file or a Makefile). In the next few
subsections I go into a little more detail on what this means.

### Separate users for web processes

I run the Nginx and PHP processes using users that are separate from
each other and also separate from my main user.

I've already gone over why I don't run these as my main user. The
reason to separate the Nginx and PHP users from each other is partly
security, but also partly more ease of diagnosis of what's going on
(any activity reported to a user can be traced to the respective
process).

### File permissions

A well-known direction of attack used by real-world attackers as well
as penetration testers is a [directory traversal
attack](https://en.wikipedia.org/wiki/Directory_traversal_attack)
where the web process is tricked into accessing files and folders that
are outside of the web root folder. One layer of security to defend
against this kind of attack is to limit the permissions to files and
folders that the user running the web process has. So even if this
user gets compromised, the user can only do damage within a limited
sphere.

All the automatic scripts that I've written to set up new sites
include steps to make sure that the files readable by others are just
the ones that are needed for the web processes. And in almost no cases
do the users running the web processes have file *write* permissions;
all writes are done through scripts run directly by me, or scheduled
through cron to be run automatically -- but not invokable via the
web. The exception is when there is a need to save uploaded or
programmatically generated images; in such cases, the write
permissions of the user running the web process are limited to the
folder(s) containing images.

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
tables, show view, and create temporary tables. The user does not have
the permission to insert, update, or delete. Morever, the
username/password is different for each site, so any bug affecting a
specific site is limited to the database for that site.

For some sites, the end user's actions can lead to data updates in
MySQL, and in these case, we do need to give at least some level of
write access.

## Robust codebase for websites that is harder to attack

While as much as possible, it is good to limit the permissions for the
web processes, there are some cases where the web processes do need
write permissions (particularly on the database side) to execute
legitimate tasks. We want to prevent end users of websites from being
able to send the web process any instructions or commands outside of
the very specific things we want to constrain them to. For instance,
we don't want them to be able to run arbitrary SQL queries, or
arbitrary shell commands.

### Safe querying with prepared statements to reduce the risk of SQL injection attacks

One common form of attack is a [SQL
injection](https://en.wikipedia.org/wiki/SQL_injection); this
generally applies to SQL queries that include some variables inside
them that are populated based on inputs that can be influenced through
the web. For instance, a SQL query that is constructed based on url
parameters or based on data entered into a form. A SQL injection
attack may use some syntax tricks to smuggle in another query into the
url parameter or form data, where this other query allows for
manipulation of the data in ways different than desired.

Limiting database permissions as discussed in an earlier section, to
only allow read permissions unless otherwise needed, can limit the
damage here: if the user running the SQL commands only has read
permissions, the user can't do much damage even if it gets
SQL-injected. However, some kinds of sites require write permissions
to be available to the SQL user. So having a way to query that doesn't
allow for SQL injection would be nice.

Fortunately, MySQL has a concept of [prepared
statements](https://www.w3schools.com/php/php_mysql_prepared_statements.asp)
whereby it does the query interpolation itself. As much as possible,
I've tried to switch all my homegrown PHP sites to use prepared
statements. Regarding the off-the-shelf software I use that uses MySQL
database, I hope and expect that the developers of the software are
constantly vigilant about the issue and stick to prepared statements.

## Unique credentials for external services with limited permissions

The idea is that, for external services, such as Amazon Web Services
(AWS) and GitHub, that the servers need to connect with, each web
server (production or development) has its own unique
credentials. Moreover, to the extent possible, the credentials are
scoped to have only the power that the servers need. However, the
point about uniqueness applies even across different identically
powered servers: they should not share credentials.

In the language of "Even if A is
broken/misconfigured/compromised, B will still not be compromised", we
have:

* A = the server that has the credentials
* B = other stuff that depends on the credentials, assuming that the
  leakage of credentials is detected quickly

Specifically, as soon as the credential leakage for the server is
detected, that credential can be removed or changed, *without* needing
to make updates to other servers. Therefore, the change of credentials
can be executed seamlessly and with minimal disruption to other
servers.

Moreover, to the extent that access logs are available, having
different credentials on different servers allows us to get
information on *which* server's credential leaked. This might allow us
to more quickly get to the root of the problem.

## Management of updates for third-party software

I use third-party software such as MediaWiki and WordPress for serving
websites; I use other software on the server to support this work. The
codebase for these softwares is large, and often, vulnerabilities are
detected in the softwares (or in extensions or plugins to the
softwares). Staying up-to-date with security patches is important.

Also, a streamlined setup process makes it easier to update the
underlying OS and stack more frequently, allowing the server to
benefit from the improved security of newer versions.

Having out-of-date software is a liability even if it has no known
security holes, because the vendor may not be publishing patches for
future security holes once they are found. Out-of-date software may
also lack compatibility with up-to-date versions of *other* software
or even operating systems.

### Operating system updates

Vulnerabilities in the operating system can put the server at
risk. Two major OS vulnerabilities in recent years were
[Heartbleed](https://en.wikipedia.org/wiki/Heartbleed) and
[Shellshock](https://en.wikipedia.org/wiki/Shellshock_(software_bug)).

Fortunately, operating systems are generally quick to patch
discovered vulnerabilities; however, if hackers discover an exploit
before it's found by security researchers, then it is particularly
dangerous (such exploits are called
[zero-days](https://en.wikipedia.org/wiki/Zero-day_(computing))). We
can't do much about zero-days, beyond having good other layers of
defense such as those described in preceding sections: firewalls,
limited permissions, separate credentials. However, for bugs that have
already been discovered and patched, it's important to benefit from
the patches by keeping the operating system up-to-date.

#### Automation of security patches

Different operating systems have slightly different approaches to
security patches. See for instance [this
page](https://www.cyberciti.biz/faq/how-to-set-up-automatic-updates-for-ubuntu-linux-18-04/)
describing the options around automatic updates.

### Major version updates for operating system

One of the risks of automating all updates is that major version
updates could cause compatibility issues with existing web-serving
code, and we don't want to break web serving! My general philosophy
around major version updates is to start a fresh server and migrate
the content to that server. This is very much possible with a good set
of backup/restore procedures.

### WordPress updates: automation and monitoring

WordPress is an interesting case. The standard/default setup for
WordPress updates relies heavily on the *web* user. WordPress uses a
concept called wp-cron, where any pageview of a page on a WordPress
site can trigger the wp-cron, which in turn can trigger background
tasks to update the core software, themes, or plugins. However. I
wasn't comfortable with this for two reasons:

* As mentioned, I've already limited the web user's permissions,
  including file permissions, so the web user is often unable to take
  the steps needed to update the core software, plugins, and themes.

* I prefer to have the updates done at a specific time of day when I
  expect to be around, and to include additional validity checks.

I found that the [WordPress CLI](https://wp-cli.org/) does a good job
of addressing these concerns. It allows for command-line execution of
checks for updates.

To make use of this, I wrote a wrapper script about the WordPress
CLI. The script does something like this:

* It pings me on Slack before starting (without tagging).
* It then goes through the WordPress sites one by one.
  * It runs a WordPress CLI command to determine whether the core
    software needs updating. If not, it continues to the next step. If
    the core software does need updating, it sends a channel-tagged
    Slack message, then runs a url checker to make sure the site is
    working fine. If the url checker passes, it calls the WordPress
    CLI to udpate the core software, and after that, runs the url
    checker again. The failure of the url checker either before or
    after the update will result in a channel-tagged message to Slack.
  * It then does something similar for updates to plugins.
  * It then does something similar for updates to themes.

This runs once a day, at a time that I'm awake and usually near my
computer. I also take daily backups of my WordPress sites which allows
me to check the condition of the site before the update. The WordPress
CLI offers a bunch of functionality around managing updates, but it's
good to know that I have backups in case things don't work as
expected.

## Backups, with established recovery procedures, help with security

The previous section hinted multiple times at the importance of
backups and established recovery procedures. Let's now talk about
these explicitly.

Backups with established recovery procedures are helpful for security,
because they give us the option to discard any compromised resource
and recreate it from scratch using the backups. For instance, if a
server gets compromised today, I can restore from yesterday's backup.

Backups can also serve as checkpoints that help diagnose when exactly
a system became compromised.

With that said, backups can also be a source of security issues if the
backups themselves are not secured. See for instance, the [2022
LastPass
incident](https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/)
where hackers got a hold of their backups. Luckily for them, the
important data is fully encrypted to a zero knowledge standard, but
you may not be so lucky. The importance of backup security is something I include as a consideration when looking at various aspects of backups in my [backups post](https://www.lesswrong.com/posts/Efj8NCCv3TqDL5mbC/aligning-my-web-server-with-devops-practices-part-1-backups).

## Protection of online accounts for hosting and domain name registration

### Account security

It's important to have tight security (with redundancy) for the
hosting service of the web server, the service used for DNS records,
the domain name registration service, and any services used for
backups. If others are able to hack into the hosting service's web
portal, they may be able to make changes to the web server's
configuration. If others are able to hack into the domain name
registration service, they may be able to steal the domain.

Such tight security might include the following:

* Strong and unique passwords
* 2-factor authentication with fallback/recovery methods configured
* No password-sharing with others who might need access to the same
  online account -- in general it should be possible to create
  additional users for them that can log in with their own
  password. As much as possible, try to enforce the same practices
  (strong and unique passwords, 2-factor authentication) for them.
* Confirmation that email messages are sent to me for any critical
  account actions or updates, so that at least I know if somebody logs
  into my account without authorizationand start changing things.

### Paying bills on time and maintaining a financial cushion

Gaps in bill payment can lead to the loss of control over some
resources. In particular, failing to renew a domain registration can
be catastrophic if somebody else registers it in the meantime. While
online services are generally good about sending reminders, it is also
important to check these proactively.

Here are a few best practices I follow:

* I pay particular attention to all email messages from the services I
  use for web servers, DNS records, domain name registrations, and
  backups. I also check my spam email at least once a day, so if any
  email from them reaches spam I can catch it.

* Every month, I review the bills from these services, either based on
  what's emailed to me or by logging in.

* I've set up automatic payments for all the services. Also, where
  possible, I try to maintain a slight positive balance in the
  accounts for these services. The positive balance makes sure that
  even if there is a glitch with the automatic payments, I am
  protected for a while. In addition, I review and top up the balances
  for the services monthly, which means that in practice the automatic
  payment ends up never being needed.
