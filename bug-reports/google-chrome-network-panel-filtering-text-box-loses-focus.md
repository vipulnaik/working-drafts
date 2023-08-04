# Google Chrome: netwok panel filtering text box loses focus

## Bug report meta

I used `Help > Report an Issue` in Google Chrome to report this
bug. The text I paste below is a copy of what I put in the text box
for the bug. I also approved of the automatic screenshot attached by
Chrome, and have saved a copy of it to this repository.

I submitted the bug report on 2023-08-03 around 5:40 PM PDT.

I checked all the boxes:

* We may email you for more information or updates
* Include this screenshot and titles of open tabs
* Send system information

## Bug report text

The network panel filtering text box in Chrome 115 keeps losing focus,
forcing me to keep clicking back into it.

I open the network panel and load any webpage (e.g.,
https://www.google.com/ then I select the filtering text box and type
in a few letters such as `go`. I then click on one of the entries
shown in the table below that contains `google`. Then I click back to
the text area. However, now each time I type or remove a character,
e.g., if I try typing out the remaining characters of `google` one by
one, the text box loses focus and focus returns to the matching
network panel entry after each character. So, I need to keep clicking
into the text box for each character. The loss of focus also occurs
when deleting or pasting characters. Basically it happens at every
action.

*However*, if the set of characters typed in does not have any
 matching entry in the network panel, then focus is retained in the
 text box for further edits.

If I somehow deselect the network panel table entries by
double-clicking on the waterfall area above them, then I can again
type freely in the text box.
