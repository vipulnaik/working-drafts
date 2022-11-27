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

## Recommendations for others (transferable learnings)

These are some of the key learnings that I expect to transfer to other
contexts, and that are sufficiently non-obvious and that may not come
to your attention until it is too late:

* Establish monitoring of the backups so that you can be confident
  that they're happening as expected, and get notified if they
  aren't. If using a managed service, make sure you are subscribed to
  notifications for the status page of the service so that you get
  notified if there are any issues with backups.

* Establish a well-defined process to restore from backups, and
  fire-drill it so that you know it works.

The rest of the stuff is also pretty important, so I do recommend
reading the whole post.

## Considerations when evaluating backup strategies

Backup strategies need to be evaluated along a variety of
dimensions. Some of these are listed below. Different considerations
come to the forefront for different kinds of backups, as we see in
later parts of the post.

### Considerations for the process of making backups

* **Integrity of the backup process and backup output**: As a
    failsafe, backups should be done properly; in particular, the
    backup process should not fail, and even more importantly, should
    not fail silently.

    This is particularly important, because most of the time, we don't
    need backups, so we may not notice that backups are failing,
    unless we set up active monitoring around the existence of
    backups.

* **Time taken for backup**: We want backups that can be executed
    relatively quickly (e.g., over a period of minutes, rather than
    hours or days).

* **Impact of making the backup on other processes**: Particularly for
    backups of production servers, we want the backup to operate in a
    way that has minimal impact on the rest of the server.

* **Cost of making the backup**: All else equal, we want making
    backups to be cheap! In general, the cost of making the backup
    depends on the size of the backup as well as the frequency.

### Considerations for backup storage

* **Security of backups**: We don't want the backup to leak to the
    public, and we also want to make sure that the backup is hard to
    destroy even if the machine is compromised somehow.

* **Independence of backups in terms of geography and provider**: We
    ideally want backups that are as independent as possible from the
    thing being backed up, to minimize the risk of both going down
    together.

* **Cost of storing the backup**: All else equal, we want backup
    storage to be cheap! In general, the cost of storing the backup
    depends on the size, frequency, and retention policy of the
    backup.

### Considerations for restoration process

* **Well-defined process to restore from backups**: We very rarely
    need to restore from backups, but when we do, time is of the
    essence, and we lack a lot of contextual information (for
    instance, if restoring from backup because the server got hacked
    or had a hardware failure). Formulating a well-defined process to
    restore from backups, and fire-drilling this process so that it
    can be applied quickly in stressful situations, is important.

* **Time taken for restoration**: All else equal, we prefer backups
    that we can restore *from* relatively quickly.

* **Cost of restoration**: All else equal, we prefer backups that are
    cheap to restore from.

## Full disk backups

### What these are

The crudest kind of backup is that of the full disk. My VPS provider,
Linode, offers managed backups for 25% of the cost of the server (see
[here](https://www.linode.com/content/linode-managed-backups-easily-configure-and-manage-backups-from-your-server/)
for more). The backups are done daily, and at any time I can access
three recent backups, the most recent being the one in the last ~24
hours, and two others within the past two weeks.

The full disk backup includes basically the whole filesystem. In
particular, it includes the operating system, all the packages, all
the configurations, all the websites, everything.

### What I use full disk backups for

I use full disk backups as a final layer of redundancy: I try to
design things in a way that I never have to use them. I basically only
use them when doing a fire drill to make sure I can restore from them.

Full disk backups are also a fallback solution for recovering
something that was on disk at the time of the backup but is no longer
on disk, perhaps due to accidental deletion or a bad upgrade. In most
cases, I don't want to rely on a full disk backup for this purpose
(due to the time and cost), but it's good to have it available as a
fallback solution, if all else fails.

### Evaluating full disk backups

I now evaluate full disk backups based on considerations described
earlier in the post.

#### Consideration for the process of making backups: integrity of the backup process and backup output (good)

Full disk backups are managed by my VPS as part of its
`Backups` service; information on this is reported on the [Linode
status page](https://status.linode.com/). I have subscribed to
notifications on this page via both email and Slack.

I also have the ability to log in at any time and check what full disk
backups are available to restore from, but I don't do this regularly.

#### Consideration for the process of making backups: time taken for backup (good)

I'm not sure how long the backup takes, but it appears to be done
asynchronously.

#### Consideration for the process of making backups: impact of making the backup on other processes (good)

As far as I can make out, the backup doesn't affect the performance of
production servers.

I do have the ability to configure when in the day the backup process
will run so if impact on other processes ever becomes an issue, I can
try to configure the timing to minimize that impact.

#### Consideration for the process of making backups: cost of making the backup (meh)

Making the backups is not broken down as a cost item; the total cost
of full disk backups is 25% of the machine cost, and it's offered as a
package deal. There aren't any knobs to tweak to optimize cost here.

#### Consideration for backup storage: security of backups (good)

Access to the backups is gated by access to my account, so they're as
secure as my account. This is good (to the extent I believe my account
is secure). In particular, it's stricter than access to the server
itself; if the server were to get hacked, the already-taken backups
would not be compromised.

#### Consideration for backup storage: independence of backups in terms of geography and provider (bad)

The managed backups are hosted by the same provider and in the same
region as the stuff being backed up, so in that sense they are not
very independent (Linode's
[guide](https://www.linode.com/content/linode-managed-backups-easily-configure-and-manage-backups-from-your-server/)
confirms this).

#### Consideration for backup storage: cost of storing the backup (meh)

Storing the backups is not broken down as a cost item; the total cost
of full disk backups is 25% of the machine cost, and it's offered as a
package deal. There aren't any knobs to tweak to optimize cost
here. With that said, the cost here is comparable to or less than the
cost of just the storage portion if I were backing up the full disk to
S3.

#### Consideration for restoration process: well-defined process to restore from backups (good)

Linode offers a clear process to restore from the backup either to the
same machine or to a new machine; I've tried their option of restoring
to a new machine. However, this is not the *full* restoration process
for a production server because there are additional steps (such as
updating DNS records) that I did not undertake. It is, however, the
*bulk* of the process (and the only part I'm comfortable testing) and
I have a reasonably clear sense of the remaining steps.

#### Consideration for restoration process: time taken for restoration (bad)

My last attempt to restore from backup (done for a fire drill) took 4
hours. Since then, I've reduced the amount of stuff on my disk, so I
expect the restoration from backup to take less time, but likely still
over 1 hour (probably closer to 2 hours). This is not great, but it's
not terrible to use as a last resort. However, it's not small enough
to use as a matter of course for time-sensitive recovery of individual
files that I carelessly delete or overwrite.

#### Consideration for restoration process: cost of restoration (meh)

The main cost associated with restoring from backup is the cost of
running the new server I'm restoring *to*, for the duration prior to
the restoration being complete. At a few hours, this comes to well
above 1 cent but under 1 dollar. The cost is small enough for a
genuine emergency, but not small enough to be negligible and to use as
a matter of course just to recover individual files that I carelessly
delete or overwrite. Overall, though, the cost scales with time, and
the downside based on cost is less than the downside based on time, so
it makes sense to just focus on the time angle.

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
  server's SQL backups folder; older backups are only in S3).

### Mechanics of backup script for logs

I also back up the access logs and error logs for the sites
regularly. This actually uses the same script as for code backups,
just with different parameters, with the source now the log file and
the target file slightly different.

### Evaluating cloud storage backups

I now evaluate cloud storage backups based on considerations described
earlier in the post. I also talk of tweaks I made to improve the way I
did cloud storage backups in order to score better on the various
considerations.

#### Consideration for the process of making backups: integrity of the backup process and backup output (probably good)

There were a bunch of considerations related to the integrity of the
backups; some of these actually occurred and others were identified by
me before they occurred. I *think* I'm in a good position here, but
since this is basically just my own set of scripts, I need to monitor
for a little longer to be confident that things are working well.

* **The backup process could fail silently, ending up not sending
    output to S3**: I fixed this two-fold, albeit one piece of the fix
    is still pending:

  * I had the backup script do extensive error-checking and report to
    a private Slack workspace I own, both in case of success and in
    case of error; in case of error, I would also get tagged. I
    eyeball the Slack channel occasionally.

  * I wrote a script that runs daily to check if recent backups exist
    in S3 and reports success to Slack (without tagging me); any
    missing backups are also reported and tag me. I investigate any
    tagged messages quickly, and also monitor the channel
    semi-regularly to make sure that the script that checks if recent
    backups exist has been running.

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

#### Consideration for the process of making backups: time taken for backups (probably good)

For some sites, the backups were large in size and took a lot of
time. The time taken was directly related to their size, so reducing
the size was a good strategy for reducing the time taken.

* In one case, the huge amount of space was due to the creation of
  several spam accounts even though the spam accounts couldn't
  actually post spam because they didn't have edit access; I had to
  manually clean up the spam accounts.

* In another case, a few tables were creating problems and I had to
  manually exclude them from the backup after confirming that they are
  derivative tables and can be reconstructed. Specifically, on
  MediaWiki sites, I confirmed that the [objectcache
  table](https://www.mediawiki.org/wiki/Manual:Objectcache_table) and
  [l10n_cache
  table](https://www.mediawiki.org/wiki/Manual:L10n_cache_table) can
  be excluded from backups.

* Similar to the above, for code backups, I switched from using `cp`
  to using `rsync` because it's easier in rsync to exclude a set of
  paths from the copy process. I was then able to exclude a variety of
  paths, including paths for autogenerated images, cache files, and
  logs.

In addition to reducing the time, I also decided to start monitoring
the time for backups. To do this, I set up Slack messaging for the
start and end of backups. At some point, I might also start adding
tagging for backups that take longer than a threshold amount of time.

#### Consideration for the process of making backups: impact of making the backup on other processes (probably good)

First off, reducing the size of backups (that I did in order to reduce
the time taken for backup) had a ripple effect on the impact of
backups: when the backup process had to do less work, it had less
impact on the server as well. However, there were a couple of other
ways I tried to mitigate the impact of the backup process:

* I switched to running all backup jobs with [`nice -n 20`](https://en.wikipedia.org/wiki/Nice_(Unix)) in order to
  play nicely with the rest of the server and to interfere as little
  as possible with production serving.

* In order to reduce the size of backups on disk on the server, I set
  up automatic deletion of older backups that I ran along with the
  backup script. My initial approach had been a `find <old enough
  backup files>` and `rm` them. This fix worked to address the disk
  space, but it ended up often taking a lot of time when there was a
  large search space.

  I later switched to a fix of directly deleting backup subfolders
  based on the expected dates in those subfolders. This worked much
  faster than `find` and has less performance implications.

#### Consideration for the process of making backups: cost of making the backup (probably good)

The cost of making the backup is essentially proportional to the size
of the backup, so the points of the preceding section also helped with
reducing the cost of making backups. With that said, the cost of
making the backup is relatively small compared to the cost of storing
the backups.

#### Consideration for backup storage: security of backups (probably good)

In order to upload the backup files to S3, I needed AWS credentials
with access to S3 to be stored on the server.

Having the S3 credentials on the server led to the risk of a hack on
the server leading to a compromise of the S3 data, or of some error in
the script causing the data in S3 to get overridden. This is a
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

#### Consideration for backup storage: independence of backups in terms of geography and provider (good)

The backups are store on Amazon S3. This is a different provider than
my VPS (Linode). Also, the AWS region where the backups are stored is
not geographically very close to the region where my Linode is
stored. Therefore, we have independence of both geography and provider.

#### Consideration for backup storage: cost of storing the backup (good)

The number of backup files grew linearly with time, and even assuming
that the backups were not growing in size from one day to the next (a
reasonable approximation, as most sites didn't have huge growth in
content), we still get a linear increase in S3 cost. This wasn't
acceptable.

In order to address this, I implemented a lifecycle policy in S3 for
the bucket with the primary backups that expired old code backups and
SQL backups after a few months. This made sure that costs largely
stabilized.

I also did some further optimization around costs: essentially, for
older backups that I don't expect to access frequently but that I
maintain *just in case*, I don't need them to be easily available. So,
in my lifecycle policy, I migrated backups that were somewhat old to
Glacier, S3's storage / cold storage. Glacier is cheaper than regular
S3 but also needs more time to access.

#### Consideration for restoration process: well-defined process to restore from backups (getting to good; work in progress)

I have a set of scripts to recreate all my sites on a new server based
on a mix of data from GitHub and S3. For those sites of mine that are
not fully restorable from GitHub (and this includes the MediaWiki and
Wordpress sites) I use the code and database backups in S3 as part of
my process for recreating the sites on a new server.

It shouldn't be too hard to modify the scripts to fully restore from
S3 even if I don't have access to GitHub at all, but I haven't done so
yet (it doesn't seem worth the effort to figure this out in advance,
since I expect that the chances of losing access to both my existing
server and GitHub at the same time are low).

#### Consideration for restoration process: time taken for restoration (getting to good)

As of now, the total time taken to restore all sites is comparable to
the time for a restore of a full disk backup, but this is largely
because there are still pieces I am working through automating (most
of these are pieces around testing; the actual downloading from S3 is
pretty streamlined).

However, the time taken to fix and restore a single site, or a few
sites, is way less than for a full disk backup. Full disk backups are
all-or-nothing: you need to fully restore to access any data. In
contrast, with S3 backups, it's possible to access just the data for a
particular site, or even more specifically, just a particular file.

I expect that the restoration process will get more streamlined over
time, as I'm using the same scripts to recreate all my sites on a new
server -- something that is going to be extremely useful for OS
upgrades.

#### Consideration for restoration process: cost of restoration (good)

Restoration is relatively cheap: the only cost is that of downloading
the backup from S3, which is relatively small. Moreover, because I can
selectively restore only the sites or even the files that I need to
restore, I only incur the costs associated with those specific sites
or files.

## Not quite a backup but serves some of the functions of a backup: git and GitHub

Some of my websites are fully on GitHub, and can be fully
reconstructed from the corresponding git repository. In this case, the
setup process for the website is mostly just a process of git cloning
followed by the execution of various steps as documented in the README
(and many of these have Makefiles, so it's just about executing
specific make commands).

Some other websites are *mostly* on GitHub, in the sense that for the
most part, they can be reconstructed from what's on GitHub. But there
are some pieces of information that are not on GitHub, and either (a)
cannot be reconstructed based on what's on GitHub, or (b) can be
reconstructed based on what's on GitHub, but the process is long and
tedious.

A combined example of both phenomena: the GitHub code for
[analytics.vipulnaik.com](https://analytics.vipulnaik.com/) includes
the logic to fetch analytics data, but a secret key is needed to
actually be able to fetch that data. Therefore, what's on GitHub isn't
sufficient to set up the repository; I also need to fetch the secret
key. However, fetching the secret key and then redownloading all the
data is time-consuming and expensive, so my setup script instead
downloads an existing database backup to jumpstart itself to the data
already downloaded on the previous server, after which the secret key
can be used to download additional data.

### What's good about git and GitHub?

* The great thing about the git protocol is that it facilitates both
  version control and ease of duplication across machines. This
  includes not just my servers, but also my laptop where I can keep a
  copy of the repositories and also work on changes locally.

* GitHub also stores a copy of the content on its own servers, which
  offers an additional layer of redundancy.

* GitHub makes it easy to give other selected people access to the
  repository, which facilitates collaboration.

* The GitHub UI has a bunch of other functionality for exploring the
  code and data.

### What's bad about git and GitHub?

* GitHub does not recommend the use of git for storing secret keys and
  credentials. For public repositories in particular, it doesn't make
  sense to store any credential information along with the repository,
  but GitHub discourages this even for private repositories. This
  isn't a bad thing about git per se, but it does indicate a
  limitation; when restoring from a git repository, additional logic
  is needed to populate the credentials.

* Git and GitHub aren't great with large files, and in particular, it
  therefore makes sense to exclude a bunch of large files from the git
  repository. This makes it unsuitable for some kinds of backups.

* For sites that use other software such as MediaWiki or Wordpress,
  it's hard to square both the code side and the database side of it
  with git.
