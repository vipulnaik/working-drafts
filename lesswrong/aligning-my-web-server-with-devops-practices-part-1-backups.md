# Aligning my web server with devops practices: part 1 (backups)

I have a web server (that serves a double-digit number of different
domains and subdomains, such as
[contractwork.vipulnaik.com](https://contractwork.vipulnaik.com/) and
[groupprops.subwiki.org](https://groupprops.subwiki.org/wiki/Main_Page). I
originally set it up in 2013, and more recently upgraded it a few
years ago. Back when I did the original setup, I had no knowledge or
experience of the principles of devops (I didn't even have any
experience with software engineering, though I had done some
programming for academic and personal purposes).

Over time, as part of my job as a data scientist and machine learning
engineer, I acquired deeper familiarity with software engineering and
devops. However, for the most part, I didn't have the time or energy
to apply this knowledge to my personal web server setup. As a result,
my web server continued to basically be a
[snowflake](https://www.sumologic.com/blog/snowflake-configurations-and-devops-automation/)
-- a special hodgepodge of stuff that would be hard to regenerate from
scratch -- and the thought of regenerating it from scratch was
terrifying. The time commitment to do so was big enough that I didn't
have enough time away from my job to do so.

In the past year, I've finally started work on desnowflaking my web
server and formulating a set of recipes that could be used to build it
from scratch, assembling all the websites and turning them on. This
work only happens in the spare time from my day job, and competes with
other personal projects, so progress is slow, but I've made a lot of
it.

This series of posts talks about various choices I made in setting up
various pieces of the system. Many of these pieces already existed
prior to my systematic efforts this year, but I had to add several
other pieces.

This particular post focuses on backups.

## Full disk backups

### What these are

The crudest kind of backup is that of the full disk. My VPS provider,
Linode, offers managed backups for 25% of the cost of the server. The
backups are done daily, and at any time I can access three recent
backups, the most recent being the one in the last ~24 hours, and two
others within the past two weeks.

It is possible to start up a new server from the full disk backup. I
did a test of this a few months ago; loading the disk from the backup
took about 4 hours. The time seems proportional to the amount of stuff
on disk. I've been cutting down on unecessary stuff on disk, so I
expect that it would take less time, but still over an hour.

The full disk backup includes basically the whole filesystem. In
particular, it includes the operating system, all the packages, all
the configurations, all the websites, everything.

### What's good about full disk backups?

* If there were some major catastrophe affecting my currently running
  production server, the full disk backup can be used to restore the
  server to a relatively recent state.

* If I accidentally lose some data (e.g., I delete a file or make some
  change to the database), even if it's not a catastrophic change, I
  can use the full disk backup as a relatively surefire way of
  getting the old state of the data as of (at most) a day. It's
  expensive in time (several hours to restore from the full disk
  backup) and also costs more (I have to pay the cost of the machine
  the backup is restored to for those few hours) but is still a good
  fallback option.

### What's bad about full disk backups?

* It takes too much time to restore from these, and also costs more
  (in terms of the cost of running the machine the backup is restored
  to for the several hours it takes to restore from backup).

* The granularity and range are decent (three backups over 2 weeks)
  but not great. It's definitely not enough to figure out exactly when
  a specific change might have occurred.

* Full disk backups aren't very useful if the goal is to restore to a
  newer or different operating system.

* Full disk backups are also managed by the same provider and hosted
  in the same geographical region as the server, so they don't offer a
  lot of redundancy in terms of provider-independence or derisking
  geographically.

### What I use them for

I use full disk backups as a final layer of redundancy: I try to
design things in a way that I never have to use them. I basically only
use them when doing a fire drill to make sure I can restore from them.

## Cloud storage backups

I back up relevant stuff (code files and SQL database dumps) to a
chosen location in Amazon Simple Storage Service (S3). I describe
briefly the mechanics of the scripts I use for these backups, then
talk about their advantages and disadvantages.

### Mechanics of backup script for code

The backup script for code works as follows:

* It takes in a bunch of arguments specifying what site to run it for,
  what folder to copy from, specific subfolders to exclude, etc.

* It copies stuff from the source folder into a local folder inside a
  code backups folder that includes the site and the current date in
  its file path. The copying is done using `rsync` and excludes any
  specified subfolders to exclude.

* The stuff in the local folder is now synced to a parallelly named
  folder in S3. This uses `aws s3 sync`.

* While we're at it, some older local backups are deleted based on
  their date (the goal is to have about two recent backups in the
  server's code backups folder; older backups are only in S3).

### Mechanics of backup script for SQL

The backup script for SQL works as follows:

* It takes in a bunch of arguments specifying what database to back
  up, what site it's for, and any specific instructions on tables to
  exclude from the backup process.

* It runs `mysqldump` on the database to back up, with exclusions of
  tables specified, and saves it in a SQL backup folder.

* It then compresses the SQL file obtained using `bzip2`.

* The bz2 file is now copied over to a parallel location in S3.

* While we're at it, some older local backups are deleted based on
  their date (the goal is to have about two recent backups in the
  server's code backups folder; older backups are only in S3).

### Mechanics of backup script for logs

I also back up the access logs and error logs for the sites
regularly. This actually uses the same script as for code backups,
just with different parameters, with the source now the log file and
the target file slightly different.

### Security: gotchas and tweaks

**Having the S3 credentials on the server led to the risk of a hack on
the server leading to a compromise of the S3 data, or of some error in
the script causing the data in S3 to get overridden**: This is a
serious risk, because S3 is intended as a layer of redundancy if
Linode fails. I took two steps to address this:

* I reduced the permissions (using AWS Identity and Access Management
  (IAM)) on the AWS keys on the server, so that they had access to
  only a specific bucket, and could only GET and PUT stuff, not DELETE
  stuff. This still didn't make things fully secure; it is still
  possible to effectively delete every file by manually writing a new
  version of the file. However, it did cut down significantly the risk
  of accidental data deletion.

* I created a separate bucket that isn't accessible at all with these
  AWS keys, and created a process that runs outside of the Linode that
  copies a few of the backups to this bucket. For instance, one backup
  every 3 or 6 months, depending on the frequency of content
  changing. These backups serve as an additional layer of protection.

### Gotchas and associated tweaks for integrity

There were a bunch of considerations related to the integrity of the
backups; some of these actually occurred and others were identified by
me before they occurred.

* **The backup process could fail silently, ending up not sending
    output to S3**: I fixed this two-fold, albeit one piece of the fix
    is still pending:

  * I had the backup script do extensive error-checking and report to
    a private Slack workspace I own, both in case of success and in
    case of error; in case of error, I would also get tagged. I
    eyeball the Slack channel occasionally.

  * I periodically manually review the backups folder for the presence
    of backup files for all sites as expected. I'm hoping to automate
    this piece relatively soon. This is useful for catching cases
    where the backup process fails to even get started (for instance,
    because it's not being invoked in the crontab, or the invocation
    is incorrect).

* **The SQL backup process could just miss some tables or err in some
    other weird way while still outputting stuff that seems
    legitimate**: This happened with one of my sites; `mysqldump`
    stopped whenever it got to specific tables, so all tables after
    those were omitted from the backups. I fixed this two-fold:

  * I added a verification for significant changes to the size of the
    SQL backup file. In case of detection of a significant size
    change, I'd get tagged in a Slack message.

  * I investigated what tables were choking the SQL backup for the
    site where I saw the choking, then manually excluded those tables
    from the backup after confirming that this would be okay.

* **There were potential filename clashes between backups being run
    from my production server and backups being done from dev servers
    I was setting up (to possibly replace the production server, or
    just to test the setup process)**: I updated the path generation
    logic to include an identifier for the machine in the path, so
    that two diferent machines should give non-colliding backup file
    paths.

### Gotchas and tweaks related to size, time, and cost

The backups would often take time, affect the production server, and
use up a lot of space both on the server disk and on S3, costing
money. I made various tweaks to address different aspects of this
issue:

* **Size at source: The backups were unwieldy in size and took a long
    time for some sites**: I investigated what tables were taking a
    lot of space. In one case, the huge amount of space was due to the
    creation of several spam accounts even though the spam accounts
    couldn't actually post spam because they didn't have edit access;
    I had to manually clean up the spam accounts. In another cases, a
    few tables were creating problems and I had to manually exclude
    them from the backup after confirming that they are derivative
    tables and can be reconstructed.

* **The backup process for some larger sites was using a lot of
  resources and making the server unresponsive for a brief period of
  time**:I switched the use of the backup process to use `nice -n 20`
  in order to play nicely with the rest of the server and to interfere
  as little as possible with production serving.

* **Size of backups on disk: The backups were taking a nontrivial
    portion of the disk space on the server**: Using up a lot of the
    disk on the server doesn't have any direct marginal cost in
    financial terms. But it is bad because it increases the risk of
    the server running out of disk space, increases the risk of MySQL
    slowing down, and increases the time taken to restore from a full
    disk backup.

  * My initial fix had been a `find <old enough backup files>` and
    `rm` them. This fix worked to address the disk space, but it ended
    up often taking a lot of time when there was a large search space.

  * I later switched to a fix of directly deleting backup subfolders
    based on the expected dates in those subfolders. This worked much
    faster and has less performance implications.


* **Size of backups on S3 and corresponding cost**: The number of
    backup files grew linearly with time, and even assuming that the
    backups were growing in size from one day to the next (as most
    sites didn't have huge growth in content), we still get a linear
    increase in S3 cost. This wasn't acceptable.

  * I implemented a lifecycle policy in S3 for the bucket with the
    primary backups that expired old code backups and SQL backups
    after a few months. This made sure that costs largely stabilized.

### What's good about S3 backups?

* S3 backups are quick to use to retrieve anything that I might have
  accidentally deleted on the server, assuming it would have been
  unlikely to change since the last backup.

* S3 backups are also useful as an input for a setup process of new
  machines (much better for the purpose than full disk backups).

* S3 also gives me more flexibility to move to another VPS or cloud
  provider if I want to.

* The S3 backup location is far from my VPS, so there isn't a heavy
  shared geographic risk.

### What's bad about S3 backups?

* The backup process can still be somewhat slow for large sites.

* There's still some possibility of affecting production server
  performance, though it's possible that, thanks to the improvements
  made, this is no longer an issue.
