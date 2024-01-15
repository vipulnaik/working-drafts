# Google Chrome: search all sources bug report

## Bug report meta

I used `Help > Report an Issue` in Google Chrome to report this
bug. The text I paste below is a copy of what I put in the text box
for the bug. I also attached a screenshot for illustrative purposes.

I submitted the bug report on 2023-04-29 around 1 PM.

## Bug report text

I’m using Chrome on a Mac. For my regular Chrome (Chrome 112), in
Chrome Developer Tools, when I try to search across all sources using
Cmd+Option+F, I do not actually see the search bar in which to
type. When I run Chrome in incognito, hitting Cmd+Option+F to search
across all sources shows a search bar, and I can use it to
successfully search across all sources.

I’ve noticed this bug a few months ago but did not report it, hoping
that subsequent iterations of Chrome would fix it. I don’t remember
exactly when the bug started. I’ve attached a screenshot of Developer
Tools for my regular Chrome after I click Cmd+Option+F; you can see
the drawer for Search has opened but there’s no Search bar.

I also checked on a different Mac (Intel Mac) and I see the same bug
there as well.

I see the error even after I deactivate all my Chrome extensions.

I’ve tried several page urls, including brand new tabs with no page
loaded, and always run into the same issue.

## My eventual bug resolution (2024-01-14)

On 2024-01-14, I decided to dig into the bug using devtools of
devtools, having had success doing so to help diagnose a [Lighthouse
issue](https://github.com/GoogleChrome/lighthouse/issues/15073). Based
on the diagnosis, I discovered that this is related to an advanced
search config where it's failing to use the default value and instead
returning an empty object `{}` because the condition
[here](https://github.com/ChromeDevTools/devtools-frontend/blob/d8d864d72bbb825235ae18119e2e1420d14182fc/front_end/core/common/Settings.ts#L392-L394)
is satisfied. The empty object fails to work properly downstream, as
it lacks the expected keys, and in particular, when the `#parse`
function executes the line
[here](https://github.com/ChromeDevTools/devtools-frontend/blob/d8d864d72bbb825235ae18119e2e1420d14182fc/front_end/models/workspace/SearchConfig.ts#L76),
the arguments to the `#parse` function are all undefined, so that line
errs out.

I didn't trace all the code, but I decided to look for the keys in
`Application > Local Storage` for `devtools://devtools` in my devtools
of devtools, as I remembered having done some cleanup here. There, I
found a key called `sourcesSearchConfig` that was set to `{}`. This
seemed to me to be the likely root cause of the problem, so I deleted
that key and restarted Chrome. After the restart of Chrome, searching
all sources worked as desired!
