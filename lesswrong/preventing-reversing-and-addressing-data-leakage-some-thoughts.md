# Preventing, reversing, and addressing data leakage: some thoughts

In the last few months, I've been thinking about the problem of
accidental leakage of data and how to prevent it, reverse it, and
address its aftermath. This post includes various thoughts, some of
them including tool-specific guidance, and some of it more general.

Examples of data leakage are as follows:

* Sending a password or sensitive credential to somebody you shouldn't
  send it to, or posting it in a forum with wide, even public, access.

* Sending factual information accidentally to somebody you didn't
  intend to share it with (or at least, didn't intend to share it with
  yet) or putting it in a forum with wide, even public, access.

The prevention steps are fairly similar for both cases, but the steps
for addressing are somewhat different. Specifically, for the case of
passwords or sensitive credentials, *changing* it is part of the best
practice response. For factual information, on the other hand, it is
often infeasible to change the facts since they're the facts!

This post is largely focused on leakage in the digital realm. Some
similar ideas apply in the physical realm as well.

This post also doesn't cover large-scale data leakage and best
practices around it (things such as password security, authentication
security of other kinds, encryption).

## Prevention strategies: general philosophy

### The accident triangle philosophy and the conjunctive nature of accidents

The [accident
triangle](https://en.wikipedia.org/wiki/Accident_triangle) idea is
that for every accident with major injury, there are several accidents
with minor injury and even more accidents with no injury. A similar
idea applies here: for every case of leaked sensitive data, there are
several cases where something went wrong, but sensitive data didn't
end up being leaked. Since sensitive data leakage is a
low-probability-but-high-cost occurrence, we don't get a lot of data
points for it.

One underlying insight here is that a major failure such as accidental
data leakage is often conjunctive: for instance, an accidental data
leakage through accidental copy/paste is a conjunction of several
things:

* Failure to clear clipboard after using it for sensitive data
* Accidentally pasting it instead of whatever you wanted to paste
  (this might be a failure to copy something else, or accidental
  pressing of the paste key)
* Failure to notice this before sending

The conjunction of all these is uncommon/unlikely. But we can think of
each of these as an accident-with-no-injury, and independently try to
reduce the likelihood of each of them. This will reduce the overall
probability of leakage due to accidental copy/paste to a negligible
amount.

### Avoid multitasking when handling sensitive data

In general, it's a bad idea to multitask between handling sensitive
data and doing things in a completely different domain. For instance,
it's a bad idea to be chatting with friends while changing a password,
or composing a public tweet while editing a private doc with sensitive
information. There's a possibility of getting mixed up.

Also, it's important to not do anything with sensitive data while on a
conference call, especially if screensharing. It's probably also
better to not work with sensitive data while in a shared physical
space with people who shouldn't have access to the data, due to the
risks of people seeing the data by peeking at your screen.

### Develop clipboard hygiene

#### The failure scenario

Your computer's clipboard is the thing that gets pasted when you paste
(using Ctrl+V on Windows or Cmd+V on Mac or Ctrl+Y in emacs; Linux
shells vary in terms of which of these shortcuts they support). You
put stuff in the clipboard by executing a cut (Ctrl+X on Windows,
Cmd+X on Mac, Ctrl+W on emacs) or a copy (Ctrl+C on Windows, Cmd+C on
Mac, Meta+W on emacs).

An interesting property of clipboards is that pasting doesn't clear
the clipboard; the item remains in the clipboard until it is
overridden by something else being cut or copied. This means that a
scenario like this is not uncommon:

* I need to copy sensitive information from one place to another, so I
  use the clipboard for copying and pasting.

* The item remains in the clipboard.

* Later, when I'm editing a shared Google Doc or messaging a friend, I
  want to share a link, but I forget to execute the *copy* step for
  sharing the link, so I end up accidentally sharing the sensitive
  information that was in my clipboard from before.

#### Clipboard-clearing

* Clear the clipboard after pasting any sensitive information! One
  simple way to do this is to open a notepad/notes app or terminal,
  type a letter, then select it and copy it. Paste it to confirm that
  the clipboard has been updated.

* For some non-system-wide clipboards, multiple clipboard entries can
  coexist (this is the case with emacs, for instance). In such cases,
  the easiest thing I've found is to just quit and restart emacs,
  though I'm sure there are other solutions.

* On modern Macs, locking screen and then unlocking automatically
  clears the system-wide keyboard, so you can use this method too --
  though it's generally more disruptive than just putting something
  else in the clipboard.

#### Making clipboard-clearing second nature

* After pasting data from one context to another (e.g., from your
  browser to your word processor, or your IDE to your terminal), ask
  the question: *should I clear this from clipboard?* And if the
  answer is yes, then clear it immediately.

* If you remember pasting sensitive data recently, but can't remember
  if you cleared it out, check what's in your clipboard (by pasting in
  a notepad or notes app or somewhere else that's safe). If you still
  see the sensitive data, that's a failure. If you see something more
  recent from the clipboard, that's good.

* Before starting on composing something for sharing with others, such
  as a Slack message, tweet, or email, or beginning to edit a shared
  Google Doc, check what's in your clipboard. If it has sensitive
  data, that's a failure.

#### Cutting down on dangerous clipboard use in the first place

In general, it's best not to have sensitive data in the clipboard in
the first place. Consider some alternatives:

* Rather than pasting sensitive data directly, paste a link to the
  sensitive data, where the link is only accessible to people who have
  authenticated themselves.

* If you're pasting sensitive data such as a password or card number
  for regular entry of that password, consider other options such as
  using the browser autofill or a password manager.

* (A bit extreme and often not worth it) If you do have to paste
  sensitive data such as a password or credential, consider ways of
  reducing the risk of leakage as follows:

  * Paste it in two or more chunks, so that your clipboard doesn't
    have the whole entry at any time.

  * Paste all but the last letter, and type the last letter manually.

#### Cutting down on accidental pasting

The paste shortcut key (Ctrl+V in Windows, Cmd+V in Mac) is close to
several other shortcut keys, including the shortcut key for copy and
for bolding. So there's a good chance of accidentally pasting when
you're trying to copy or bold.

If your clipboard is clear of sensitive information in the first
place, accidental pasting causes limited damage. But based on the
accident triangle philosophy, it's best practice to try to cut down on
accidental pasting as much as possible, especially when switching
contexts or using a collaboratively edited doc such as a Google Doc,
or while sharing screen (accidental pasting while within the flow of
editing a document locally and privately is not that big a deal).

The main way to cut down on accidental pasting is a mix of (a)
improving precision of one's keyboard use in general, and (b) going a
little slower whenever using the keys to cut, copy, paste, or bold,
e.g., looking at the keyboard rather than touch-typing even if you
normally touch-type.

### Pause and check before hitting Enter or send

Always pause and check what you're sending before you hit Enter or
send, whether you're using email or a messaging tool. In general, I
recommend a gap of at least 2-3 seconds between typing your message
and sending it, as it gives you enough time to react to anything weird
you see in what you're sending.

I generally check the following:

* Is the *content* of the message what I want it to be?
* Do the *links* go where they should? (In particular, because links
  may not be shown as they're replaced by anchor text, this may be
  important to check).
* Are the *recipients* the intended ones?

This is an important practice even outside the issue of sensitive data
leakage; sending a message to a wrong recipient delays the right
recipient receiving it, while also confusing the wrong recipient.

### Double-check when sharing documents or putting them in shared folders

Sharing documents in Google Drive or a similar online service for
document collaboration is a bit like sending, and the same cautions
apply here as they do with sending emails. (Maybe a bit less because
you have the ability to edit the document after sending, but you still
don't want to share sensitive data).

A silent way of sharing documents is to move them into a shared
folder. This generally doesn't proactively notify recipients (but you
should double-check this for the specific service you are using) but
it still makes the documents accessible to them, and they'll see the
documents if they happen to view the folder after you put the document
in the folder. Be careful when putting documents in shared folders --
if in doubt, check who has access to the folder, and that it matches
the people you want to have access to the document. NOTE: Google does
warn you about this when moving a document to a shared folder; in
general, it's a good idea to read and ponder such warnings.

### Be careful about screensharing

These suggestions apply when screensharing on a conference call (such
as Zoom, Google Meet, or Slack Huddle), and also when sharing your
screen physically such as in a physical conference room.

* Before screensharing on a conference call, check that you don't have
  sensitive information in any of the screens that you intend or
  expect to share. In fact, it may be better to check this when
  joining the conference call even if you don't need to immediately
  screenshare, so that you're ready to screenshare whenever.

* Check that you don't have sensitive data in your clipboard before
  sharing screen (in fact, it's good to check before joining the
  conference call, and to not put sensitive stuff into the clipboard
  during the call).

* As much as possible, try to share only a specific tab or specific
  window or specific set of windows. This reduces the risk of
  sensitive information in other windows getting leaked. Confirm using
  the software's visual cues that you're sharing the screen(s) you
  think you're sharing (for instance, Zoom uses a green outline to
  indicate the windows that you are sharing).

### Pay attention to warnings and color coding

Many services warn you when they suspect you're sending something
suspicious. For instance, Gmail warns you if the email you're trying
to send includes links to Google Drive content that the recipients
don't have access to. Pay attention to these warnings, as they could
help prevent accidental sends to the wrong parties.

Gmail also uses color coding and banners in various ways to indicate
cases where it suspects that you're sending a message to the wrong
recipients. Pay attention to these colors and banners! For instance,
if you're using Google for Workspaces, your work Gmail will color-code
the recipients who are outside your organization, so you can eyeball
and see that these people aren't in your organization. Similarly,
Google Drive issues a warning when you try to share a document with
somebody outside your workspace.

In Slack, if you're using Slack Connect to communicate with people
from a different workspace, Slack will show a message right above your
message-drafting area reminding you that the other person is from a
different organization. Pay attention to this.

## Immediate reversal strategies

### Undo send for emails and messages

* Gmail offers an "Undo send" functionality that is available for a
  few seconds right after you send an email, if you don't navigate
  away from the screen. You can configure the send cancellation period
  for which this "Undo send" is visible by going to `Settings >
  General`. Other mail providers may offer similar functionality.

  Note that if you undo send, the message doesn't actually get sent,
  so recipients don't get it. If you *don't* undo send, the message
  get sent after the send cancellation period. Once the message
  actually gets sent, there is no reversing it.

* Slack allows you to edit or delete messages you've sent any time
  after you send them; the exact functionality available may depend on
  your workspace settings. Note that even if you edit or delete the
  message, the original message would still have been visible to
  people for the duration from when you sent it to the time you edited
  or deleted it, and you have no programmatic way to know if they read
  it or not.

* Facebook's Messenger allows you to "Unsend for everyone" any
  message; however, the message would have been visible to them prior
  to unsending. You do get visual cues indicating whether the message
  was read by them before you unsent it. Even if you unsend, the fact
  that you sent the message will be included in the message history
  (in lieu of the message itself).

### Undo bad edits to shared documents

When you make an edit to a Google Doc or Google Sheets that you want
to reverse, you should reverse it immediately *without navigating away
from the tab where you're editing*. The reason for this is that Google
commits a version of the document every time you switch focus away
from it, and there is no way to delete old versions from the version
history of the document (the only real way is to start afresh with a
new document). If nobody else is viewing the document at the time you
make your undesired edit, *and* you reverse the edit immediately
without switching tabs, it won't get into the history and will not be
visible to others. You should confirm this later by reviewing the
history of the document in its most expanded form.

### Remove sensitive information from histories

* If you accidentally visited a sensitive url, you should be able to
  remove it from your browsing history.

* If you pasted something accidentally into the address bar of your
  browser and hit Enter, causing you to Google it, you should be able
  to remove it from your Google search history.

* If you entered sensitive information in your terminal and hit Enter,
  it may get into your shell history (though it might enter your shell
  history only after you actually exit that terminal tab). You should
  be able to delete it from your shell history file (such as
  `.bash_history` or `.zsh_history`). These files are generally only
  accessible to you, so removing isn't super-urgent but it's probably
  good to remove so that you don't end up showing it in a screenshare
  later when searching your history. Similar remarks apply to
  histories for various REPLs, such as MySQL or Python.

* If you entered sensitive information into your browser console, it
  gets into your console command history. In Chrome, you can access
  and edit your console command history by opening devtools of
  devtools, then manipulating the Local Storage associated with
  `devtools://devtools` (either by using `Application > Local Storage`
  or using JavaScript in the console using `window.localStorage`). See
  [here](https://stackoverflow.com/questions/33299810/where-is-chromes-debugger-console-command-history-stored)
  for more related information.

### Undo bad edits to posts or comments on online fora

This applies for many online fora; the one I have the most experience
with is GitHub.

* Most fora offer the option of fully deleting the post or comment,
  which removes it from public view. The service may keep a log for a
  short period.

* Some fora allow you to edit the post or comment and *don't* show
  older revisions. In such cases, you can edit out the sensitive
  information and be done.

* Some fora allow you to edit the post or comment but they do show
  older revisions. In such cases, you should check whether
  functionality to delete specific older revisions exists. For
  instance, GitHub offers the ability to delete specific revisions
  (except the latest one) for comments on issues and pull requests.

It's generally good to investigate what is and isn't allowed by a
forum in advance, so that when you do get in the position of having
entered sensitive data, you can quickly choose the optimal approach.

### Reverse local changes within git repositories

If you made a sensitive change to a git repository that is shared with
others (e.g., on GitHub) local changes you make could be reversed if
they have not yet been pushed to the remote origin. Here's some
guidance:

* If you detect the sensitive data before you commit it locally, you can just
  undo the change, and then proceed normally.

* If you detect the sensitive data after you commit it locally but
  before pushing to the remote origin, you can undo the sensitive data
  and then amend your commit. Your local git will still have a commit
  associated with the sensitive data, but it will no longer be
  associated with the branch. Therefore, it won't get pushed to the
  remote unless you directly push that specific commit. You can later
  try to remove it through garbage collection or (after you've pushed
  what you *wanted* to push) by deleting and refetching the git
  repository from the remote origin.

* If you already pushed the change remotely, record the commit hash
  for the commit with sensitive data. Then immediately amend the
  commit to remove the sensitive data and do a force push (`git push
  --force-with-lease`). The commit with sensitive data will still
  exist on the remote origin, but it's now a dangling commit not
  associated with any branch (you can confirm this by visiting the
  page on GitHub and seeing a banner near the top saying so).

  In the case of GitHub, they don't automatically garbage-collect
  dangling commits, so you need to reach out to their support by
  clicking "Clear cached views"
  [here](https://support.github.com/request/remove-data?tags=docs-generic). The
  support can take 1-2 business days to address your request. After
  that, the danging commit should not be accessible through GitHub.

  If any collaborator ran a `git fetch` or `git pull` between the time
  you originally pushed and the time you force-pushed, they'll also
  have that commit on their local git. However, collaborators who ran
  `git fetch` or `git pull` only after your force-push won't get that dangling commit
  even if it's still on GitHub.

## Addressing leakage of password or credentials

### Change credentials where feasible

You should assume that any password or credential is compromised if
you think others might have seen it (for instance, you included it in
a Slack message and then deleted the message, but aren't sure if
people read the message before you deleted it). Therefore, you should
change it as soon as feasible. if you are using the same or a highly
similar password or credential elsewhere, you should change that too.

This is made easier if:

* You don't use the same or a very similar password/credential in
  multiple places (as it means you have fewer places to change)

* Your password/credential is not closely tied to personal information
  about you

* You maintain an organized list of your services/accounts for which
  you have passwords/credentials, allowing you to audit quickly

## Addressing leakage of factual information

### Check if others accessed the information

This is most relevant to factual information that, unlike credentials,
cannot simply be changed.

In case of factual information that others were not supposed to have,
you may be able to check if they were able to access the information
without explicitly asking them. Some cases:

* For documents accidentally shared with them in Google Drive, you can
  go to `Tools > Activity dashboard > Viewers` to see who all has
  viewed the document. After you've fixed the permissions, you should
  be able to check this. If the people you accidentally shared with
  did *not* access the document, you can be confident that it didn't
  leak to them.

* Facebook Messenger has visual cues to show if somebody read a
  message. If you delete the message prior to them having read it, you
  can be reasonably confident they didn't access it.

### Figure out what kind of secret data it was from the person it leaked to

#### The benign case of not-very-actionable information they don't and shouldn't know but they know about

An example here is that you accidentally share information about your
company's quarterly revenue with a work colleague who is not supposed
to have access to the data. Then you detect and delet the
data. There's nothing particularly surprising about the data you
accidentally shared, it's just that as a matter of policy, your
colleague shouldn't have access to that data. Your colleague is also
aware that such data exists, and that you have access to the data --
the only thing they didn't know is the specifics.

#### The trickier case of information that is genuinely surprising and actionable to them

Let's say you are a senior executive at a company and have been tasked
with figuring out what half of the people in your division to fire. If
you accidentally share musings/thoughts related to this with one of
the people under you (who might end up being in the line of fire, even
if it's unclear right now), this is a case of information that is
actionable to them. This is a tricky situation to be in, and here you
have to exercise a judgment call regarding whether to take them into
confidence explicitly versus go with the risk that they might have
seen the information.

In this case, the other person may feel stress and fear about the
situation. Depending on how they model you, and what they expect from
you, they may also feel disappointed in you for not sharing the
information with them earlier. Finally, if you only leaked to a subset
of the affected people, you may create asymmetries between them (e.g.,
now some of the people who may be fired know they may be fired, and
others don't) and the possibility of further leaks.

### Explicitly discuss if you're sure they saw it

If you're sure the other person saw it, it seems best to explicitly discuss.

In the case of "not-very-actionable information they don't and
shouldn't know but they know about" it may be as simple as saying
"Hey, I accidentally leaked this info to you; you may have seen it;
please ignore and delete it. Sorry!"

In the "trickier case of information that is genuinely surprising and
actionable to them", you'll need more of a strategy. The exact strategy
you choose partly depends on the reasons you kept the information
secret in the first place.

* In some cases, it makes sense to talk to the people who've seen the
  information and ask them to keep it in confidence for now.

* In other cases, it may make sense to openly share with a wider pool
  (if you're concerned about asymmetries between the subset of people
  who know). This can tamp down on speculation and the possibility of
  ongoing leaks.

### Make a judgment call about explicit sharing if you aren't sure if they saw it or not

If you were able to re-hide factual information that you temporarily
leaked, and aren't sure if people saw it during the interim, you have
to make a judgment call: do you operate under the assumption that they
probably didn't see it (and it's as good as if you had never leaked
it), or do you act on the assumption that they might have seen it? The
specifics here will vary based on the situation.

In the "benign case of not-very-actionable information they don't and
shouldn't know but they know about" it doesn't matter too much; it may
be easiest to just not say anything, but if they bring it up you can
tell them you accidentally shared it and ask them to ignore or delete
it.

In the "trickier case of information that is genuinely surprising and
actionable to them", you have to choose between sharing with them and
asking them to keep confidence, sharing more widely with all affected
parties, and just keeping quiet until you have stronger evidence that
they know.

### What can you do in advance to make addressing leakage easier?

When hiding sensitive information over an extended period of time, you
should assume some probability of leakage. Here are a few thoughts on
how you can make it easier:

* Don't make enemies! In general, people are more likely to exacerbate
  a leakage (by leaking it further) if they don't like you. Don't give
  people reasons to hate you or want to get back at you.

* As much as possible, try to minimize the number of cases where
  you're hiding from people "information that is genuinely surprising
  and actionable to them"; as much as possible, data that you hide
  should be of the form of "not-very-actionable information they don't
  and shouldn't know but they know about" (for instance, detailed
  financial statements that are consistent with the high-level picture
  they have of finances, but are being kept secret). As long as most
  secrets aren't things that are very actionable to the people who
  they get leaked to, these people will just ignore them (unless they
  hate you, which brings me back to the "Don't make enemies!" point).

* If a secret needs to be maintained for an extended period of time,
  invest in some upfront organization around how to make sure that
  stuff related to that secret doesn't leak. For instance, maybe only
  do things related to that secret during specific times of the day
  when you are *not* interacting with other people.

* Formulate contingency plans for how to deal with a leakage. In
  particular, think through what path you'll take if the information
  has definitely or probably leaked, per the preceding subsections.
