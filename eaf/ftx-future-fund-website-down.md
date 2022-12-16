# FTX Future Fund's website is down, ftx.tghp.co.uk still seems to work

The FTX Future Fund official website
[ftxfuturefund.org](https://ftxfuturefund.org/) no longer works, with
all pages giving a nginx 404 not found error. Looking at its [Wayback
Machine
snapshots](http://web.archive.org/web/20220000000000*/https://ftxfuturefund.org),
the last working snapshot appears to be from [December 12,
2022](http://web.archive.org/web/20221212115231/https://ftxfuturefund.org/)
(about 4 days ago).

The content of the site still seems to be available at
[ftx.tghp.co.uk](https://ftx.tghp.co.uk/). This is a subdomain of
[tghp.co.uk](https://www.tghp.co.uk/), the website of website design
company The Glasshouse Project. A reasonable inference is that The
Glasshouse Project designed FTX Future Fund's website and hosted a
copy of it as a subdomain.

This leads me to a bunch of questions:

1. Who owns the domain registration for ftxfuturefund.org? Are there
   efforts by anybody to secure this and make sure the domain
   registration does not expire? Running `whois ftxfuturefund.org`
   shows that ownership information is hidden, but does say that the
   registration is currently set to expire on 2023-02-23T00:44:17Z.
2. Where is ftxfuturefund.org currently hosted and is it possible for
   whoever is managing the hosting to fix the issue that's causing the
   nginx 404 not found error? Running `dig ftxfuturefund.org` shows
   that the IP address for ftxfuturefund.org points to CloudFlare,
   that's probably not the final host, so the hosting situation is
   unclear.
3. Is the version at ftx.tghp.co.uk the most current version? Or was
   it just an initial version of the site that The Glasshouse Project
   made for FTX Future Fund before handing it off to the latter?
4. Does The Glasshouse Project plan to keep its version around for the
   long term? Is it worth reaching out to them to encourage them to
   keep it around longer? Presumably, FTX Future Fund is no longer a
   client of theirs, so they don't have a strong incentive to keep the
   site up, but the marginal cost may be negligible.
5. Partly depending on the answers to the previous questions, should
   the links pointing to ftxfuturefund.org from other places be left
   as is, updated to use ftx.tghp.co.uk, or updated to use the most
   recent functioning Wayback Machine snapshot?

I'd love if somebody with insight on any of these questions could
share it in the comments.
