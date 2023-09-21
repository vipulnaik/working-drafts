Original question: https://money.stackexchange.com/questions/158164/where-do-i-report-iso-income-with-a-subsequent-disqualifying-disposition-and-wh

Full markdown of question below (comments and answers *not* mirrored here):

Here's what happened in 2022 in the United States. I have changed numbers a little bit for simplicity and privacy.

I had an incentive stock option (ISO) grant that I exercised using a net exercise with withholding to cover exercise cost and taxes. The grant was for 10,000 shares. 8,000 shares were withheld-to-cover so I ended up receiving 2,000 shares. The 8,000 shares that were withheld-to-cover underwent an immediate disqualifying disposition, and my employer withheld taxes on the "sale" of these 8,000 shares including federal income tax, social security tax, and medicare tax. The amount was added to my W-2 wage income (boxes 1, 3, and 5 of my W-2) and the withholdings were also included in my W-2. And although I do not have visibility on this, I presume that the "employer portion" of social security and medicare taxes, to the extent applicable, was also paid on this income (NOTE: Social security taxes are complicated by the social security wage base / taxes cap which ended up capping things, but for Medicare at least the above should all apply).

Later, within the same calendar year, I sold the remaining 2,000 shares. Since I sold the shares in less than a calendar year, these shares underwent a disqualifying disposition. However, the system used for the sale does not inform my employer of this so the subsequent disqualifying disposition was not communicated back to my employer, and so the portion of the proceeds that should have been disqualified (namely the gain *up to* the point of exercise; the gain from exercise to sale still shows as capital gains for Form 8949 / Form 1040 Schedule D) was not added into my W-2, and no withholding was done.

**Where do I report the additional compensation income from the subsequent disqualifying disposition?**

NOTE: I'm talking here *only* about the gain *up to* the point of exercise; the gain from exercise to sale still shows as capital gains for Form 8949 / Form 1040 Schedule D and that part is pretty straightforward and I'm comfortable with that.

I'm getting conflicting/confusing information from different sources.

I tried looking at the [Form 1040 instructions](https://www.irs.gov/instructions/i1040gi) and saw this:

> Line 8k

> Stock options. Enter on line 8k any income from the exercise of stock options not otherwise reported on Form 1040 or 1040-SR, line 1h.

However, I didn't get lot of clarity on what exactly is covered by "stock options" here and whether it includes ISO disqualifying dispositions. I also checked what line 1h covers and the list of cases under it doesn't seem to include anything related to ISO disqualifying dispositions.

I tried getting this information from a few online sources, and they suggest just silently adding it to my W-2 wage income:

https://www.thebalancemoney.com/incentive-stock-options-3192970#toc-reporting-requirements says:

> Calculate compensation income. Include this amount as wages on line 1 of Form 1040 in addition to the amounts from Form W-2 if the compensation income has not already been included on the W-2.

https://fairmark.com/compensation-stock-options/employee-stock-purchase-plans/disqualifying-disposition-reporting/#step-3-report-your-compensation-income says something similar:

> If the compensation income from your disqualifying disposition was included in the wages reported on Form W-2, simply report the number from your W-2 on your tax return the way you normally do. If it was *not* included on your W-2, add the ESPP compensation to the wages on your Form W-2 and report the total as wages on your tax return.

> Some people worry that they need to attach an explanation if the number for wages on Form 1040 doesn’t match the number on the attached Form W-2. That isn’t necessary here because the number you’re reporting is *greater than* the number on Form W-2.

**What taxes are due on this income?**

This is closely connected to the previous question, because where I put the income on the Form 1040 will determine what taxes are due (to a first approximation). Here are the potential taxes:

* **Federal income tax**: This income should all contribute to AGI and therefore to taxable income. I think this part is straightforward and will apply regardless of where in Form 1040 I put the income.
* **Social security tax, Medicare tax, and 0.9% additional Medicare tax**: Whether this income is subject to the social security tax (subject to social security wage base limitation), Medicare tax, and additional Medicare tax (if the total earned income is high enough) would depend on where I enter it in the form. I also tried checking online whether this income is taxable for social security purposes. https://www.thebalancemoney.com/incentive-stock-options-3192970 seems to suggest that it's not eligible for these taxes, but I know that the portion of the ISO that was *immediately* disqualified *was* subject to those taxes. And if it is conceptually just like wage income then it *should* be subject to all these taxes.
* **Employer portion of Social Security tax and Medicare tax**: This is the part that I am most uncertain about. Since my employer didn't report this income on the W-2, and if it is indeed eligible for Social Security and Medicare taxes (similar to the *immediately* disqualified disposition) then it should also be subject to the *employer* portion of these taxes. If my employer didn't pay those, perhaps I should? However, I couldn't find any form to do this directly -- the two forms that seemed closest were Form 4137 (unreported tip income) and Form 8919 (uncollected Social Security and Medicare tax on wages) but neither of them seems to fit fully.

**How is the tax treatment different than if I did not split compensation income out?**

I was trying to understand what the significance for tax purposes is of splitting out the gain into compensation income and capital gains income. Since I sold within the same calendar year anyway, I would anyway fall within short-term capital gains. Which means that I'm not eligible for the lower long-term capital gains tax rate. Barring some edge cases, this is my understanding of the additional taxes (beyond the income tax, which should be the same in both cases):

* **If I am below the Social Security wage base**: In this case, reporting as compensation income is clearly worse for me taxes-wise, because I have to pay the 7.65% (6.2% Social Security and 1.45% Medicare), plus 7.65% employer share if I am on the hook for that as well. So 7.65% or 15.3% depending on whether I should pay the employer share.
* **If I am above the Social Security wage base but below the threshold for Net Investment Income Tax / Additional Medicare Tax ($200,000 for single filers)**: In this case, reporting as compensation income is still worse because I have to pay 1.45% or 2.9% depending on whether I am on the hook for the employer share.
* **If I am above the threshold for Net Investment Income Tax / Additional Medicare Tax**: In this case, reporting as compensation income is *better* if I only have to pay the employee share. That's because I have to pay only 1.45% + 0.9% additional Medicare tax = 2.35%, versus paying 3.8% net investment income tax. On the other hand, if I am on the hook for the employer share as well, then it's 2.9% + 0.9% = 3.8% vs. 3.8%, a wash.

I'm ignoring a bunch of in-between cases (e.g., earned income below $200,000, but earned + investment income above, or earned income straddling $200,000) in order to paint the general picture.

Let's put these additional tax rates in a table.

| Income range | Social Security and Medicare tax due? | Employer portion of tax due? | Compensation income case | Capital gains income case |
| -- | -- | -- | -- | -- |
| < Social Security Wage Base | No | No | 0% | 0% |
| < Social Security Wage Base | Yes | No | 7.65% | 0% |
| < Social Security Wage Base | Yes | Yes | 15.3% | 0% |
| Between Social Security Wage Base and $200,000 | No | No | 0% | 0% |
| Between Social Security Wage Base and $200,000 | Yes | No | 1.45% | 0% |
| Between Social Security Wage Base and $200,000 | Yes | Yes | 2.9% | 0% |
| > $200,000 | No | No | 0% | 3.8% |
| > $200,000 | Yes | No | 2.35% | 3.8% |
| > $200,000 | Yes | Yes | 3.8% | 3.8% |

The thing that's weird to me is that at low incomes, treating it as compensation income is clearly *worse* for tax treatment, but at high incomes, the situation reverses, *unless* I am on the hook for the employer portion of the medicare tax as well (in which case it's exactly a wash). This makes me suspect that I am indeed on the hook for the employer portion of the tax, because it seems deeply counter-intuitive that declaring some income as compensation income (instead of short-term capital gains income) can *lower* my tax bill.