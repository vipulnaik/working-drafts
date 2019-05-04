In August 2018, my work colleague Tomo Kazahaya and I came up with the
idea of using GitHub issues to keep track of daily work checklists. We
created a private GitHub repository called `daily-updates`. In
October, I copied over the idea to managing personal checklists; you
can see [my first issue created October
20](https://github.com/vipulnaik/daily-updates/issues/1).

Since then, I've been creating daily updates issues on my personal
repository on any days where I'm doing meaningful work on personal
projects or tasks beyond daily personal maintenance.

In this post, I'll talk briefly about the following:

* The benefits of a broadly visible written document for a personal checklist
* The benefits of daily granularity for a personal checklist
* The benefits of using GitHub issues to record daily updates
* Some protocol questions I don't have clear answers to

## The benefits of a broadly visible written document for a personal checklist

I'm using the term "broadly visible" instead of public, because in
some cases (such as companies) daily updates of employees refer to a
lot of confidential company information, and therefore can only be
visible within the company.

The emphasis on "broadly visible written document" is to contrast with
two other kinds of approaches:

* Personal checklists, that each person manages on their own, but are
  not visible to others: The advantage of a broadly visible document
  rather than a personal checklist is that people can check any time
  what the others are working on. This allows them to offer thoughts
  and feedback, and also gives a better organization-wide picture of
  what is going on.

* Daily stand-ups, where everybody describes what they plan to do
  during the day: Written documents are preferable to daily stand-ups
  because they can be continuously updated as needed, can be
  referenced any time, and work better for teams that don't all start
  work at the same time. Also, my historical experience has been that
  most people hate stand-ups; the Internet
  [seems](https://news.ycombinator.com/item?id=14271670)
  [to](https://blog.standuply.com/stand-up-meetings-are-soon-dead-e74118f788f4)
  [agree](http://blog.idonethis.com/daria-developer-hates-standup/).

## The benefits of daily granularity

Checklists can be made at different granularies: hourly, daily,
weekly, monthly. I have found that daily is a good unit for a certain
kind of checklist.

In my experience, a day is long enough and flexible enough to have a
reasonable set of things to fit in (without being too prescriptive
about what to do at what time) while still short enough to plan even
in chaotic environments.

For larger teamsn and/or more complex projects, planning needs to be
done on longer timescales, but a flat checklist of items may be too
simplistic for longer timescales, and tailored project management
tools (such as Jira) may be better suited to such planning. Such
planning can be complementary to the daily checklist.

Why have a daily checklist if we have broader project planning? A few
reasons:

* Daily checklists can include items that are not part of the broader
  plan, but more one-off pieces of work.

* Daily checklists offer a clearer sense of how the work breaks down
  in practice at a daily granularity. Project management tools can be
  quite complex, and while they may be better at overall task
  tracking, they may not be that good at getting a sense of "how much
  work of what kind can be done within a day?:

## The benefits of using GitHub issues to record daily updates

Using GitHub issues for daily updates is a bit of a hack, since that's
not the original purpose of GitHub issues. Nonetheless, the hack has
worked well. Here are some of the advantages of GitHub issues for
daily updates:

* GitHub has good checklist/checkbox support, which makes it easy to
  track progress.

* The concept of closing an issue helps create a sense of finality:
  once somebody has finished checking boxes and updating their daily
  updates issues, they can close the issue. Then others know that the
  issue represents the final state of what was done during the day.

* If much of the other work being done is also recorded in GitHub,
  GitHub's support for linking within GitHub can make it easy and fast
  to add links to the actual work. This could include links to GitHub
  issues, commits, or pull requests.

* It's easy to see daily checklists for many different people together.

## Some protocol questions I don't have clear answers to

Some of the questions I've wondered about, but don't have clear answers to.

### How should we handle stuff that came in after the original checklist was made?

My approach is to just add it to the list.

If it's particularly important to know what fraction of work is
pre-planned versus spontaneous, the stuff added later can be put in a
separate section for spontaneous tasks. I've tried this in the past,
back when getting that sense was important to me. However, I nowadays
organize my checklist by topic instead.

### Should boxes be checked if the whole task as intended wasn't completed, but part of it was?

My current strategy is to check the box and edit the description to
note that only part of the work was done.

### Should people be expected to keep the checklist updated throughout the day, or only once when closing the issue?

I think that as an organizational requirement, there should be only a
requirement to create the checklist (open the issue) early in the day,
and close it either at end of day or early in the next day. People who
want to update the checklist more frequently are welcome to, but there
is no requirement. For some organizations, there may be a requirement
for more real-time up-to-dateness.
