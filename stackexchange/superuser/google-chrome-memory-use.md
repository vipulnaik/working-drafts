# Google Chrome memory use

Question url: https://superuser.com/questions/1817473/what-accounts-for-the-discrepancy-between-the-memory-use-shown-when-hovering-on

Question title: What accounts for the discrepancy between the memory use shown when hovering on the Chrome tab, and the heap size?

Full markdown of question text below (comments and answers *not* mirrored here):

Chrome tabs now show active memory used by the tab when you hover on the tab title; see [here](https://medium.com/@addyosmani/chrome-now-shows-each-active-tabs-memory-usage-4f74876538e6) for the details.

Chrome also allows us to get more details on the memory use in the Memory panel of Devtools, where a (constantly updated) JS heap size is provided. I can also take a heap snapshot from right there in the Memory panel, and I can see the size of the heap snapshot.

I found that the JS heap size and the heap snapshot size are within the same ballpark of each other, but the active memory use by the tab is (usually) _significantly_ higher.

For instance, on https://example.com/, in one particular load, I got a tab memory use of 23.8 MB:

[![example.com tab memory use][1]][1]

For comparison, the JS heap size is 1.1 MB (see bottom):

[![JS heap size on example.com][2]][2]

The snapshot size is also 1.1 MB (see left column)

[![JS heap snapshot for example.com][3]][3]

For context, example.com is an extremely small page, about 1 KB in size, and it renders on a single screen with no scrolling needed (see first screenshot above).

I've also noticed that tab memory use can adjust down a little bit under memory pressure (e.g., if I open a lot of tabs) or backgrounding (e.g., I tab away from the tab for some tme) but I have rarely seen it come down all the way to match the heap size or heap snapshot size.

So, what causes the greater active tab memory use, how can we get better insight into what aspects of the page structure and content are contributing to it, and could the active tab memory use that is *over and above* the heap size cause out-of-memory issues?

  [1]: https://i.stack.imgur.com/vXqlp.jpg
  [2]: https://i.stack.imgur.com/gXg5k.png
  [3]: https://i.stack.imgur.com/HuCHX.png
