# Optimized battery charging

Question url: https://apple.stackexchange.com/questions/468067/how-can-i-revert-to-the-old-optimized-battery-charging-regime-on-sonoma

Question title: How can I revert to the old optimized battery charging regime on Sonoma?

Full markdown of question text below (comments and answers *not* mirrored here):

I keep my M1 Macbook laptop plugged in most of the time, and have had it set to optimized battery charging for a long time. I've noticed two versions of the optimized battery charging regime.

**Regime 1: 7-10 day cycle between 81% and 76% without active use of battery**

In this regime, the battery charge level cycles between 81% and 76%, starting at 81% and then gradually dropping to 76% over a period of about 7 to 10 days, without the battery actively being used to power the computer (all the computer's needs are met through the power drawn by being plugged in). This rate of power drop is comparable to what I have seen when the computer is turned off and not plugged in, so it just seems to reflect the natural rate at which batteries leak charge.

When the charge level drops to about 76%, the battery charges back up to 81%, and the cycle starts again.

Characteristics of this regime:

* Maximum state of charge seen regularly: 81%
* Minimum state of charge seen regularly: 76%
* Average state of charge seen regularly: 78.5%
* Calendar time for one charge-discharge cycle: 140 to 200 days

**Regime 2: daily cycle between 100% and 80% through active battery use**

In this regime, the battery charge starts at 100%, stays there for a while, then starts actively being used (even while the computer is plugged in) till it falls to 80% over a period of about 2-3 hours. Then it stays at 80% for a while, and then it starts actively being charged back up to 100% (that takes about an hour). This cycle happens about once a day, though it may be a little less frequent.

Characteristics of this regime:

* Maximum state of charge seen regularly: 100%
* Minimum state of charge seen regularly: 80%
* Average state of charge seen regularly: around 90% (the exact value depends on how long it stays at 80% versus 100%)
* Calendar time for one charge-discharge cycle: 5 days

**The situation on Ventura, prior to upgrading to Sonoma**

Prior to upgrading to Sonoma, I observed the following:

* If I kept my computer plugged in continuously, then it would stay in regime 1.
* If I unplugged and replugged my computer at least once a day, even for a few minutes (for instance, when moving it from one location to another), it would stay in regime 2 (basically every time it would unplug, it would try to charge back to 100% when next replugged, and then at least once a day it would bring the charge back down to 80%).

For the period from the end of February 2023 till I upgraded to Sonoma in the end of October 2023, I kept my computer in regime 1 by keeping it plugged in continuously (I might have unplugged in briefly once or twice when cleaning my table, but the duration of unplugging was short enough that it didn't trigger regime 2). The number of charge-discharge cycles as reported in the Power section of the System Report went up from 46 to 47 over the period -- an increase of just 1, which is as expected based on the estimated above. My OS over this whole time period was Ventura.

**The situation after upgrading to Sonoma**

After upgrading from Ventura to Sonoma (which I did over two months ago), even though I've kept my computer plugged in continuously, it has stayed in regime 2. Over this period, the number of charge-discharge cycles went up from 47 to 66, an increase of 19 over a period of about 67 days. This is even faster than the "one charge-discharge cycle every 5 days" would suggest, though still within range so I think that description of the regime is approximately accurate.

**Is regime 1 better, and if so, how can I get back to regime 1 or something comparably good?**

As of now, my battery reports being at 100% capacity and in good health.

My understanding is that regime 1 is strictly better in terms of maintaining a state of charge that is closer to 50% and also in terms of having fewer charge-discharge cycles. (If this reasoning is wrong, I'd like to know that too). So, if possible, I would like for the battery to return to regime 1, or something similar. My question is: how can this be done?

I use my laptop an average of 8-9 hours a day (estimate based on the screen time app) so actually unplugging it would use the battery much more than even regime 2 does (though it might help with keeping the average state of charge a bit lower, my understanding is that the extent to which it'll hurt charge-discharge cycles would be a bigger consideration). So I'd really like to keep it plugged in and rely on optimized battery charging, and I'm looking for ways to get back into regime 1.
