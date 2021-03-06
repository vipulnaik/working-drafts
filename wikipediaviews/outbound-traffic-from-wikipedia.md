Below, we estimate traffic that Wikipedia generates for external sites.

I originally wanted to do this as a response to people who claim that
placing links on Wikipedia generates a lot of revenue for the
link-placers. At this point I don't think there is a point in
responding to the original discussion, but this seems to be of
independent interest.

Historical note:

* Prior to June 12, 2015, all non-logged-in traffic could be seen
  using Google Analytics as a referrer; the full referral path could
  be seen.
* With the switch to HTTPS on June 12, 2015, wikipedia.org referral
  traffic stopped getting reported.
* In February 2016, Wikipedia set a policy of "Origin" for the
  referrer, so the referrer domain could be seen but not the actual
  full referring URL.

See https://meta.wikimedia.org/wiki/Research:Wikimedia_referrer_policy
for more details on referrer policy.

Add to https://meta.wikimedia.org/wiki/Research:Timeline_of_Wikimedia_analytics

## issarice.com

https://www.google.com/search?q=issarice.com+site%3Awikipedia.org&ie=utf-8&oe=utf-8 overlists pages.

https://en.wikipedia.org/w/index.php?title=Special:Search&profile=all&search=issarice.com&fulltext=1 underlists pages (only lists two of four links).

Four links:

* User:Riceissa
* GiveWell (page deleted)
* Dustin Moskovitz (reference to Cari Tuna)
* User:Shaddim
* User talk:Riceissa

Traffic data en.wikipedia.org -> issarice.com: https://analytics.google.com/analytics/web/#report/trafficsources-referrals/a54798318w87799141p91155095/%3F_u.date00%3D20150208%26_u.date01%3D20170310%26explorer-table.plotKeys%3D%5B%5D%26_r.drilldown%3Danalytics.source%3Aen.wikipedia.org%26explorer-graphOptions.selected%3Danalytics.nthMonth%26explorer-segmentExplorer.segmentId%3Danalytics.landingPagePath/

Data: 69 sessions, 2.75 pages/session.

Upshot: CTR to issarice.com from these three user pages, in total, is about 1%. Maybe it's a bit higher, considering that some of the pages added the link later and we're considering lifetime pageviews. Or maybe lower, if some of the Wikipedia-sourced stuff is fake or referrer spam (or from pages we can't locate offhand).

Also for specific links:

https://en.wikipedia.org/w/index.php?title=Dustin_Moskovitz&diff=740677347&oldid=740675683 added link to https://issarice.com/cari-tuna from page on Dustin Moskovitz on September 22, 2016.

The page has had about 270K pageviews since then, see https://wikipediaviews.org/displayviewsformultiplemonths.php?page=Dustin+Moskovitz&months[0]=201702&months[1]=201701&months[2]=201612&months[3]=201611&months[4]=201610&language=en&drilldown=all and generated 4 visits to issarice.com.

So the CTR works out to 0.0015%.

The page on GiveWell had an addition of a link to https://issarice.com/givewell-staff-growth sometime between July and December 2016 (don't know exactly when, as page is deleted). Wikipedia page about GiveWell has had about 10K pageviews since then, and generated zero clicks. This is consistent with the low CTR.

Fraction of traffic to issarice.com explained by this? Total traffic over this period was on the order of 30,000 views (maybe a few thousand were spam) so about 0.5% of pageviews came from Wikipedia, and most of them from userspace.

## vipulnaik.com

https://en.wikipedia.org/w/index.php?search=vipulnaik.com&title=Special:Search&profile=all&fulltext=1&searchToken=e1iw2udyiqzkjb9beka8qag97

## effective-altruism.com (Effective Altruism Forum)

Seems like 770 sessions, 1.63 pages/session: https://analytics.google.com/analytics/web/#report/trafficsources-referrals/a53416835w86109361p89329676/%3F_u.date00%3D20140901%26_u.date01%3D20170310%26explorer-table.plotKeys%3D%5B%5D%26_r.drilldown%3Danalytics.source%3Aen.wikipedia.org%26explorer-graphOptions.selected%3Danalytics.nthMonth%26explorer-segmentExplorer.segmentId%3Danalytics.landingPagePath/

This is out of 877,474 total pageviews to the Effective Altruism Forum.

So maybe 0.2% of total traffic

## groupprops.subwiki.org (Group Properties Wiki)

Date range: September 1, 2014 to March 10, 2017

Data: https://analytics.google.com/analytics/web/#report/trafficsources-referrals/a4377715w8432957p8783374/%3F_u.date00%3D20140901%26_u.date01%3D20170310%26explorer-table.plotKeys%3D%5B%5D%26_r.drilldown%3Danalytics.source%3Aen.wikipedia.org%26explorer-segmentExplorer.segmentId%3Danalytics.landingPagePath/

5,679 sessions, 3.63 pageviews/session, second biggest website referral source

Total pageviews to groupprops.subwiki.org in that timeperiod was 2,352,232, so this was about 0.8% of total traffic.


