# Google Chrome: old version of page loading in reopened tab

## Report sent 2025-03-11

### Text in free text area in response to "Describe the issue in detail"

It has happened to me three times so far that Chrome opens an older version of a tab when I reopen the tab for either of these two reasons: (a) the tab became inactive since I hadn't visited it for a while, and then I visit it again, or (b) I close the tab and then do "Reopen closed tab".

In all three instances, the version of the tab that ended up loading was an older cached version than the version of the tab that had loaded in that tab. Instead, it was an older version from a previous run of Chrome (i.e., the version that ended up loading was one that would have been cached from a version of Chrome that I had already quit).

All the instances occurred with GitHub issues that I had edited multiple times, so the old version had an older version of the content of the issue.

Two of the instances occurred with Chrome 133 and one instance occurred with Chrome 134. So it's not a new bug introduced by Chrome 134 but it also doesn't appear to have been fixed in Chrome 134.

I was not able to reliably reproduce the issue; in fact, I could not deliberately reproduce it and it only happened when I was doing stuff in the wild.

### Additional options

URL: https://github.com/vipulnaik/daily-updates/issues/1875

Email: vipulnaik1@gmail.com

Attach file: (none, as Chrome auto-suggested a screenshot of the right inspect tab)

Boxes checked:

* We may email you for more information and updates
* Include this screenshot and titles of open tabs
* Send system information (I clicked the link and confirmed that this
  includes the Chrome version on the laptop and a few select Chrome
  settings)
