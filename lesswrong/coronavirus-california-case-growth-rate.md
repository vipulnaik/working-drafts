In this post, I try to understand the case growth rate for coronavirus
cases in California, and try to address questions such as:

* How long will the case count continue to grow?
* At what level will the case count stabilize?
* To what extent will we be able to infer from the data whether level
  2 restrictions were sufficient, or level 3 restrictions were
  necessary, to stop or significantly slow down case growth? The
  "level 2" and "level 3" jargon are from my [previous
  post](https://www.lesswrong.com/posts/pBPiZQYBF9niRAMSq/coronavirus-the-four-levels-of-social-distancing-and-when).

Skip to [answers and lessons](#answers-and-lessons) for my (incomplete
and tentative) answers.

NOTE: My original post was based on data till 2020-03-27 (row 17 in
the
[spreadsheet](https://docs.google.com/spreadsheets/d/1L8xJs1YNn3iMHHohgtTLhcvUULEj-crwupB72QAJJLg/edit#gid=0)). On
2020-04-01 (April 1, 2020) I made edits to this post of two kinds:

* Language improvements, based on feedback in the comments, without
  any substantive changes to the model.
* Addenda at the end of some sections giving updates based on data
  seen since I originally published the post. I used data till
  2020-03-31 (row 21).

## A simple model from true currently-or-eventually-symptomatic cases to confirmed cases to deaths or recoveries

### The model

For simplicity, I will use the shorthand "true
currently-or-eventually-symptomatic cases" only for cases where a
person is already infected and will *eventually* become symptomatic
(so this will include both currently symptomatic cases and cases that
are presymptomatic, i.e., will become symptomatic later). I expect
that most asymptomatic cases (i.e., cases that *never* become
symptomatic) won't get diagnosed, and therefore won't count in the
number of confirmed cases either, so this seems a reasonable
approximation for the model I will present below. However, if
incorrect, this could cause estimates to be off by a factor of two or
more, depending on the fraction of cases that are asymptomatic.

The simplistic model identifies the following flow:

1. Get infected
2. Start showing symptoms
3. Get a test
4. Get test results
5. Recover or die

Technically, 5 can happen before 3 or 4; the logical dependencies are
1 -> 2 -> 5 and 1 -> 2 -> 3 -> 4. It's also possible (and probably
more likely) that 5 happens after 3 but before 4.

To keep this post focused, I will not discuss 5 here, though it's
obviously very important.

### Time lags in the model (1 -> 2 -> 3 -> 4)

The total time lag from 1 to 4 shows up as the lag between any trend
change in the number of true currently-or-eventually-symptomatic cases, and the
corresponding trend change in the number of confirmed cases. The more
accurately we can estimate and measure this total time lag, the more
accurately we can relate the timing of social distancing measures and
the timing of case growth flatlining. Herei s what I know:

* The 1 -> 2 lag is in the range of 2 to 14 days, according to
  [CDC](https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html).
  I'll use a median estimate of 1 week.
* The 2 -> 3 lag depends on the queue/backlog for tests. It looks like
  there is no single queue for tests, but rather, different kinds of
  cases are in different queues (those showing severe symptoms or
  those who need to do essential work may get a priority for being
  tested). For simplicity, I'll use a median estimate of 1 week. See
  [here](https://www.nytimes.com/article/test-for-coronavirus.html)
  for reasonably up-to-date information on the experience of getting
  tested.
* The 3 -> 4 lag seems to be between 5 and 10 days. Again, I'll use a
  median estimate of 1 week.

Using median estimates for each suggests that there is a lag of *3
weeks* between trend changes in true currently-or-eventually-symptomatic cases and
trend changes in confirmed cases. If this 3 weeks were precise, then
the trend in confirmed cases will be a 3-week time translation of the
trend in true cases. In practice, however, because each transition has
a variable time range, varying across individuals, the true time range
is more like 2 to 6 weeks. And rather than a crisp time translation,
we see a fuzzy smear -- even if true currently-or-eventually-symptomatic cases
flatline immediately after the escalation from level 2 to level 3
(flexible lockdown), the confirmed case count will show no such sharp
trend change, instead showing a leveling off over time.

## Looking at the California data

### Description of the data

*Original version written 2020-03-29, possibly edited for clarity but
 with no substantive model changes.*

The California Department of Public Health publishes [daily
releases](https://www.cdph.ca.gov/Programs/OPA/Pages/New-Release-2020.aspx)
on coronavirus case counts as of the previous date. The reports have
always included data on the number of confirmed positive cases and the
number of deaths. Starting with the release for March 18 (published
March 19), the release includes data on the total number of tests and
the total number of test results returned.

I put the data together in a
[spreadsheet](https://docs.google.com/spreadsheets/d/1L8xJs1YNn3iMHHohgtTLhcvUULEj-crwupB72QAJJLg/edit#gid=0)
where I added columns for the daily increments to each value, as well
as some percentages and comparisons of interest. *ETA 2020-04-01: I
have been updating the spreadsheet daily since writing this post;
please see up to row 17 for 2020-03-27 in the spreadsheet to
understand the part of it I had in front of me when writing the post.*
A few notes:

* There are two dates with sharp changes to the incremental number of
  confirmed positive cases (i.e., the "second derivative" of the
  confirmed positive case count is high; see column E for confirmed
  positive cases, column I for the first derivative and column O for
  the second derivative): the transition from March 18 to March 19,
  and the transition from March 25 to March 26. Outside of these days,
  the second derivative is low; the growth seems to be closer to
  piecewise linear or quadratic than exponential. The increase from
  March 18 to March 19 may be due to more testing capacity -- it's
  hard to say because we have test counts only starting March 18. The
  increase from March 25 to March 26 is off by a few days from an
  increase in the number of test results. However, if there is a lag
  between test results and confirmed cases showing up, that might
  explain the jump.

* The total number of tests jumped a lot from March 23 to March 24
  (see column D for the number of tests and column G for the first
  derivative). Looking at language in the CDPH report pages, this
  seems to be because tests from some state and local health labs that
  were previously not included have started getting included.

### Extrapolating the number and timeline of confirmed positive cases for people already tested

*Original version written 2020-03-29, possibly edited for clarity
 later but with no substantive model changes.*

Let's go back to our simple model:

1. Get infected
2. Start showing symptoms
3. Get a test
4. Get test results
5. Recover or die

It is quite hard to measure 1 and 2 from the data we have, but we can
shed light on 3 and 4 based on the data collected here.

First, as noted in the previous section, the data seems consistent
with a 3 -> 4 lag of 5 days or a little more. Specifically, the number
of test results on a given day is around 75% to 90% of the number of
tests about five days before that. This is consistent with test
results taking five days, but some results getting delayed. See column
M.
  
However, as the number of tests has increased quite a bit recently ,
the lag might increase a lot in the next few days if processing
capacity has not kept pace.

Second, we see that right now, the majority of tests don't yet have
results (i.e., there is a lot in the 3 -> 4 transition). Therefore,
even assuming that there are no more true currently-or-eventually-symptomatic cases
coming through 1 -> 2 -> 3 any more, there's still a lot in 3 -> 4 and
much of it may be confirmed positive.

Third, at least so far, the cumulative confirmed positive rate
(confirmed positive cases as a percentage of test results; see column
L) has been going up, albeit slowly. The incremental confirmed
positive rate (incremental confirmed positive cases as a percentage of
incremental test results; see column K) is more noisy, but is also
generally higher in recent days than it was in the beginning. The
increase in confirmed positive rate could be because (a) the selection
of who takes the test is getting more precise, as people better
understand the right symptoms, flu test screening is instituted, and
test criteria are improved, or (b) the false negative rate of tests is
reduced as tests become more accurate.

With all these, we can make the following loose predictions:

* We expect to see results for about 64,000 currently pending tests in
  the next 5 to 7 days, assuming test processing capacity keeps pace.

* If the confirmed positive rate of the remaining tests matches that
  of the tests so far, we will see about 16,514 confirmed positive
  cases from the people who have already been tested (cell N17).

* Here is an argument that the confirmed positive rate will be
  dramatically lower for the still-pending tests, even though it's
  been increasing so far: We have just recently hit the point where
  the people getting tested now are testing "too late" to have
  actually gotten the disease, because this is just about the right
  amount of lag after we went to level 2 or level 3.

* Here is an argument that the confirmed positive rate will be higher
  for the still-pending tests: Since the confirmed positive rate has
  been generally increasing, it may be better to extrapolate from the
  confirmed positive rate of the last 2 or 3 days.

Based on these considerations, I estimate that, just from the people
who have gotten tested so far, we should expect a total of 10,000 to
40,000 cases in California. This is inclusive of the already-diagnosed
4,643 cases. I also expect that, if testing capacity keeps pace with
the number of tests done, we will hit this number (somewhere between
10,0000 and 40,000) by around Friday, April 3, along with the number
of test results getting to equal or exceed the current total number of
tests (~89,000).

Further, I expect that (again assuming that test processing capacity
roughly keeps pace) we will see another sharp increase in the
incremental confirmed positive case count in the transition from March
28 to March 29 or March 29 to March 30. This will lag by about 5 days
the sharp increase from March 23 to March 24 in the total number of
tests. More specifically, I expect that the incremental number of
confirmed positive cases will go up from its current daily value of
~800 to a few thousand.

*Addendum 2020-04-01*: Based on data from a few more days of tests (up
 to row 21 for 2020-03-31 in the spreadsheet), here are my updated
 thoughts:

* I had not explicitly thought about this possibility, but it seems
  like the CDPH reports have become a bit more erratic over the
  days. This has complicated some analysis for the days after I
  published the original post. I had also not thought explicitly about
  the possibility of the test count needing to be adjusted downward,
  though I had been subconsciously suspicious of the huge jump in test
  count.

* Setting that aside, I still stand by my general prediction range of
  10,000 to 40,000 confirmed cases from the first ~90,000 tests. In
  fact, in light of the new data, I narrow the range to 15,000 to
  40,000. That's because the
  cumulative confirmed positive rate (columns K and L) has continued
  to go up.

* My caveat of "assuming that test processing capacity roughly keeps
  pace" was important because, judging from data till 2020-03-31, test
  processing capacity has not kept pace with the increase in the
  number of tests a week ago. This means that I expect that the
  results for the first ~90,000 tests won't be out by the end of this
  week. My guess is it will take another 1 or 2 weeks. This means that
  the count of confirmed positive cases will continue to rise for the
  next 1 or 2 weeks purely from clearing the backlog on test
  processing, even if no new tests happen.

### Thinking about the transitions till testing (1 -> 2 -> 3)

*Original version written 2020-03-29, possibly edited for clarity
 later but with no substantive model changes.*

The data here doesn't give a clear idea of how the transitions from 1
to 2, or from 2 to 3 are proceeding. Nonetheless, it may offer some
clues. So first, let's backtrack and think: let's say California going
to level 2 or level 3 did in fact effectively stop coronavirus in its
tracks. What should we see?

First, keep in mind that there's a time lag 1 -> 2 and a time lag 2 ->
3. When describing the model, we estimated these time lags as 1 week
each, so that's a total of 2 weeks. This means that, about 2 weeks
after coronavirus is stopped in its tracks, we should see a
corresponding change in the trend of the number of true
currently-or-eventually-symptomatic cases that are getting tests.

One complication is that, because there is huge variation between
people and between regions in the 1 -> 2 time lag and in the 2 -> 3
time lag, we won't see a sharp trend change after 2 weeks. Rather,
we'll see the trend change happening a little more gradually.

Another complication: even if the rate at which true
currently-or-eventually-symptomatic cases are getting to the testing
stage drops, the number of other cases (e.g., people with a
cold, flu, or allergy) that's getting the test may increase. In that
case, we may not see a decrease in the number of tests being done. So,
more accurately, we should see at least one of these:

* A drop in the incremental number of tests each day. This will happen
  if the growth of true currently-or-eventually-symptomatic cases
  slows down, but any increase in tests from other cases does not
  increase to compensate.

* A drop in the confirmed positive rate on tests (but this metric is
  available at a further 3 -> 4 lag of about a week). This will happen
  if the growth of true currently-or-eventually-symptomatic cases
  slows down, and proportionally more people who don't have
  coronavirus are getting the tests.

Unfortunately, we aren't seeing the second yet. As for the first, the
transition data from March 26 to March 27 suggests that yes, we are
seeng a drop in the incremental number of tests (the increment went
down from 10,600 to 1,200). But that's just one day of data. If we see
a similar drop persist, that might mean that we are finally seeing the
lagged effects of escalating to level 2 or level 3. A week after that
we should see a drop in the growth rate of confirmed positive cases.

*Addendum 2020-04-01*: In the above para, I noted a sharp drop in the
 incremental number of tests a day. The reduced number has been
 sustained over the days since then, but it's hard to get a clear idea
 because CDPH is also making adjustments to address double-counting of
 tests. Nonetheless, tentative evidence is consistent with (but
 doesn't strongly support) the idea that the growth of true
 eventually-asymptomatic cases slowed down a few weeks ago.

### Is the data good enough to know whether level 2 is sufficient, or whether we need level 3?

My rough estimate is that California achieved level 2 starting around
March 11 to March 13, and escalated to level 3 around March 17 to
March 19. The gap is about one week. This is a really small gap, and
is dwarfed by the range of variation in the time lag. If case counts
level off in the next one or two weeks, we won't have good enough data
to say whether level 2 was sufficient, or the escalation to level 3
was necessary.

Of course, while aggregate data may not say much, it is still possible
that more detailed analysis of individual cases will answer the
question. Specifically, we would need to identify the number of
individual cases where we expect that they got the infection in the
time period when California was level 2. However, because of the long
period between getting exposed and showing symptoms, we may have a
large number of cases where we are pretty uncertain.

## Answers and lessons

### Answers

I summarize the predictions from this post here.

* The super-optimistic scenario is that almost all people who had the
  disease are already tested, and confirmed positive rates for the
  pending tests will be lower than those for the tests so far.

* In this super-optimistic scenario, I expect something like 10,000
  confirmed cases and, assuming test processing capacity keeps pace, I
  expect the number to be hit by around April 3. For comparison, there
  are currently 4,643 cases.

* My estimate range for the number of confirmed positive cases from
  people already tested is 10,000 to 40,000. With the optimistic (but
  not super-optimistic) assumption that almost all people who had the
  disease are already tested, I expect us to hit this number by around
  April 3, after which the growth rate of confirmed positive cases
  will slow down to a trickle.

* Given the huge time lags and variation in time lags, it will be
  hard, even after case growth stops, to know whether level 2 was
  sufficient or level 3 was neceessary to arrest case growth.

### Lessons

* Cutting down time lags (as well as variation in time lags) is
  crucial to being able to reason clearly about cause and effect
  between social distancing measures and infection growth rates.

* In particular, cutting down the time spent waiting to get a test
  (the 2 -> 3 transition), and cutting down the time taken to process
  test results (the 3 -> 4 transition), is absolutely critical.

* Better heuristics for people to identify themselves as needing to
  get tested, even before they start feeling sick, would be great (it
  would speed up the 1 -> 2 transition). For instance, if loss of
  smell is an early indicator, even before a person otherwise feels
  sick, that could help people get 1 -> 2 faster.

* Getting more detailed data on each case, to gauge the expected true
  start date of infection, is very important to be able to determine
  the true growth rate of an infection. I hope some people are doing
  this, because the publicly available aggregate statistics are not of
  much use for that.

* I personally found it more helpful to model confirmed case trends as
  linear, quadratic, or piecewise linear/quadratic than
  exponential. This is because at least at present, the bottlenecks
  are around testing capacity, which is growing linearly or
  quadratically, not exponentially.
