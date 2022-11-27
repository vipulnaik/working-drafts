# Aligning my web server with devops practices: part 2 (security)

This is a continuation of my previous post.

This post focuses on devops practices I adopted to secure my web server.

## Firewall (note: AWS uses the term "security group" for the equivalent concept)

My cloud provider, Linode, offers basic port-based firewall
functionality. I used this to minimize the number of entry points to
the server.

The firewall is set up as follows:

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

### What's good about a firewall?

A firewall is a layer of protection against misconfiguration of some
service I'm running within my server (such as PHP or MySQL) that has
an open port. I actually did make this mistake once in a dev server I
was setting up: I misconfigured the way the PHP port works, and left
port 9000 open to traffic. This was a dev server, so didn't serve live
sites yet, and was not in any clear way identified with me. But it did
get detected by a crypto malware bot, that ended up using all the CPU
on the server. A firewall would have prevented this even *with* my
misconfiguration.

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
