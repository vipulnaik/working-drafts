Posted at https://www.lesswrong.com/posts/p5EWmxfnaJKwkHYRu/benefits-of-micro-tracking-for-personal-health-measurements

I'm interested in understanding the benefits of what I call
"micro-tracking" for their health: tracking information such as diet,
heart rate, exercise routine, etc. at a granularity finer than a day.

Starting last year, and likely expanding further into this year, I am
using a more "macro-tracking" approach.

For instance, for supplements, this macro-tracking simply involves
tracking the [start and end date of consumption of each supplement
bottle](https://github.com/vipulnaik/diet-exercise-health/blob/master/sql/supplements.sql). This
means roughly one new data entry per month. The corresponding
"micro-tracking" approach would be to record each time I take a
supplement, possibly with other information such as the time of day,
relation with meal, etc.

Similarly, for food, I do record all purchases of restaurant food in
my [activity
tracker](https://github.com/vipulnaik/diet-exercise-health/tree/master/notes/2021-activity-tracker.md)
(albeit not in a computable format). I am now thinking of adding
information on the specifics of all food purchases (from both grocery
stores and restaurants) in a computable format. This is a
macro-tracking approach. The corresponding micro-tracking approach
would mean recording each meal, including information such as time of
day, quantity of various foods in the meal, etc. (For the most part I
do not share food with others, and my food waste is near-zero, so
purchases = consumption; I can record exceptions separately).

Disadvantages I see of micro-tracking:

1. Time: It looks like micro-tracking adds a nontrivial daily overhead
   of tracking work. Time is very important to me. Even more so, time
   that I need to spend daily, when I might be pressed for time on
   other tasks, is even more important.
2. Difficulty with micro-quantification (for food): It's an extra
   hassle to quantify exactly how much food I am consuming. When
   consuming cooked food, I am usually helping myself from a large
   bowl of prepared food and may go from 70% to 65% of it or something
   like that. The food isn't perfectly mixed either, so some days I
   might end up having more of the tomatoes part and other days I
   might end up having more of the spinach part.
3. Aggregation effort: Once all the micro-quantities are entered, I
   need to aggregate them to extract meaningful data. If I enter data
   at a more aggregated level, this is somewhat easier.

Advantages I see of micro-tracking, and why these did not ultimately
convince me:

1. Better correlational analysis of day-to-day fluctuations: If I were
   micro-tracking my moods, physiological measurements, and physical
   reactions as well as my food and supplement intake, I might be able
   to identify what patterns of food or supplement intake correlate
   with what moods. People I know who micro-track tend to have reasons
   like this.

   This is a pretty good reason for some people. People who suffer
   from allergic reactions, stomach issues, or large mood swings could
   probably benefit from such diagnostic data very concretely. In my
   case, I haven't had major issues of this sort frequently; the few
   rare times I do have such issues, I manually record in my [notes
   folder](https://github.com/vipulnaik/diet-exercise-health/tree/master/notes)
   along with details specific to the situation. I also don't trust my
   self-reflection to assign quantifiable and consistent measures of
   things like my mood.

2. Having micro-tracking permits some sort of aggregations that
   wouldn't be possible just with macro-tracking, such as information
   on time of day, time gaps, etc.: For instance, rather than just
   know how much of a Vitamin D supplement I took in the last three
   years, I can learn how much of it I took in the mornings versus at
   night, and what the day-to-day fluctuation in intake was. Possibly,
   such details matter a lot for assessing the impact of the
   supplement.

   I agree that this is a potential benefit; however, as of now I am
   not collecting enough fine-grained data on the other side to
   meaningfully correlate with. It seems to me that combining total
   consumption with some general information on when I usually consume
   supplements is enough.

I'm curious to hear what people think I'm missing, or any other
insights people want to share!
