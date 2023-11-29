# ChatGPT 4 solved all the gotcha problems I posed that tripped ChatGPT 3.5

In December 2022, I [shared logs of my interactions with the
then-nascent ChatGPT 3.5 (December 15, 2022
version)](https://www.lesswrong.com/posts/w7c2iKjsDrNqoymxQ/to-err-is-neural-select-logs-with-chatgpt). In
April 2023, at my request (and with financial compensation by me) my
friend [Issa Rice](https://issarice.com/) reran those prompts against
ChatGPT 4 (using a paid subscription that he had at the time). He
shared the findings in gists
[here](https://gist.github.com/riceissa/378f230875210b7214a8e2c54f111bc9)
and
[here](https://gist.github.com/riceissa/ea7c8abc038eff2e1a6e0379691e67ca). Things
were a little busy for me at the time, so I didn't get around to
formatting and sharing those logs, and then after a few months I
forgot about them. I just remembered this so I've decided to format
and share the logs.

The TL;DR is that ChatGPT 3.5 fumbled on the bulk of my questions,
making a bunch of errors and often doubling down on them, but ChatGPT
4 got everything correct, and almost always on the first try. In fact,
in most cases, the text of the responses had no incorrect statements
as far as Issa or I could make out.

Similar to the original post, the interactions are in blockquotes and
I've included my comments on the interactions outside the
blockquotes. I have used **bold** for cases where it made incorrect
statements, and *italics* for cases where it made correct statements
that directly contradicted nearby incorrect statements. Unlike the
original post, though, you'll see very little use of bold and italics
in this post.

You may want to open the original post side-by-side to compare the
answers.

NOTE: I also did one intermediate test against the 2023-01-09 version
of ChatGPT 3.5 that you can see
[here](https://github.com/vipulnaik/working-drafts/commit/427f5997d48d78c69e3e16eeca99f0b22dc3ffd3). This
had slightly better but overall fairly similar results as my original
post, so I did not format and share the post.

I have shared a few further thoughts in the Conclusion section.

## Product of negative numbers (session 1; 2023-04-08)

> Issa: What is an example of an odd negative number?

> ChatGPT: An example of an odd negative number is -7.

> Issa: What is an example where two negative numbers multiply to give
> a negative number?

> ChatGPT: Normally, when you multiply two negative numbers, you get a
> positive number. This is because the negative signs cancel each
> other out. There isn't an example where two negative numbers
> multiply to give a negative number, as it contradicts the basic
> rules of multiplication.

> Issa: Can the product of two negative numbers be negative?

> ChatGPT: No, the product of two negative numbers cannot be
> negative. When you multiply two negative numbers, their negative
> signs cancel each other out, resulting in a positive product. This
> is a fundamental property of multiplication involving negative
> numbers.

These answers look great! I can't find any
meaningful flaw with them. My very minor quibble is with the use of
the word "Normally" in the second answer, which seems unnecessary and
confusing.

## Product of odd integers and product of even integers (session 1; 2023-04-08)

> Issa: Can the product of two odd integers be even?

> ChatGPT: No, the product of two odd integers cannot be even. When
  you multiply two odd integers, the product will always be odd.

> Here's a simple explanation:

> An odd integer can be represented as (2n + 1), where n is any
> integer.

> Let's take two odd integers:

> Odd integer 1: 2n + 1

> Odd integer 2: 2m + 1

> Now, multiply these two odd integers:

> (2n + 1) * (2m + 1)

> Expanding this expression, we get:

> 4nm + 2n + 2m + 1

> This can be written as:

> 2(2nm + n + m) + 1

> Since 2nm + n + m is an integer, the expression 2(2nm + n + m) + 1
> represents an odd integer. Thus, the product of two odd integers
> will always be odd.

> Issa: Can the product of two even integers be odd?

> No, the product of two even integers cannot be odd. When you
> multiply two even integers, the product will always be even.

> Here's a simple explanation:

> An even integer can be represented as (2n), where n is any integer.

> Let's take two even integers:

> Even integer 1: 2n

> Even integer 2: 2m

> Now, multiply these two even integers:

> (2n) * (2m)

> Expanding this expression, we get:

> 4nm

> This can be written as:

> 2(2nm)

> Since 2nm is an integer, the expression 2(2nm) represents an even
> integer. Thus, the product of two even integers will always be even.

The answers seem correct; if I were scoring these on a test I'd give
them full scores. One could quibble and say, for instance, that m has
not been declared to be an integer in either answer, which is
technically a failure of rigor, but I would overlook that failure in a
human submission. In any case, I didn't even ask for a proof here, and
it still supplied me with a mostly-complete proof.

In fact, the answers feel so good that I suspect that these are just
part of ChatGPT's knowledge base and it's not figuring them out on the
fly. But it's unclear.

## Integer-valued polynomial with rational coefficients (session 1; 2023-04-08)

> Issa: What is an example of a polynomial with rational coefficients?

> ChatGPT: An example of a polynomial with rational coefficients is:

> P(x) = (3/4)x^3 - (2/3)x^2 + (5/2)x - 7

> In this polynomial, each coefficient is a rational number (a number
> that can be expressed as a fraction with integers in the numerator
> and the denominator).

> Issa: Give an example of a polynomial with rational coefficients that always takes integer values at integers

> ChatGPT: A polynomial that always takes integer values at integers
> is called an integer-valued polynomial. Here's an example of an
> integer-valued polynomial with rational coefficients:

> P(x) = (1/2)x(x - 1)

> **This polynomial is actually a representation of the arithmetic
> sequence where the common difference is 1**. When you substitute any
> integer value for x, you will get an integer result:

> For example, let's substitute a few integer values for x:

> P(0) = (1/2)(0)(0 - 1) = 0

> P(1) = (1/2)(1)(1 - 1) = 0

> P(2) = (1/2)(2)(2 - 1) = 1

> P(3) = (1/2)(3)(3 - 1) = 3

> P(4) = (1/2)(4)(4 - 1) = 6

> As you can see, for each integer value of x, the polynomial P(x)
> yields an integer result.

> Issa: Give an example of a polynomial with rational coefficients
> that are not all integers, such that the polynomial always takes
> integer values at integers

> ChatGPT: An example of a polynomial with rational coefficients that
> are not all integers, but still takes integer values at integers,
> is:

> P(x) = (1/2)x(x - 1)

> This polynomial represents the triangular numbers, which are the
> sums of consecutive integers from 1 to a given integer value. When
> you substitute any integer value for x, you will get an integer
> result:

> For example, let's substitute a few integer values for x:

> P(0) = (1/2)(0)(0 - 1) = 0

> P(1) = (1/2)(1)(1 - 1) = 0

> P(2) = (1/2)(2)(2 - 1) = 1

> P(3) = (1/2)(3)(3 - 1) = 3

> P(4) = (1/2)(4)(4 - 1) = 6

> As you can see, for each integer value of x, the polynomial P(x)
> yields an integer result, even though one of its coefficients, 1/2,
> is not an integer.

The answers seem pretty good. The volunteering of the "integer-valued
polynomial" jargon again suggests that ChatGPT already knew the
information, rather than figuring it out on the spot. I did highlight
one sentence in one of the answers that seems off; likely the intended
meaning was that the polynomial represents the *sum* of the
sequence. Also, the reasoning offered (for why the polynomial always
takes integer values at integers) only covers nonnegative
integers. Again, however, the prompt didn't ask for proof, so I can
hardly fault it for providing only a partial explanation.

## Product of prime numbers (session 1; 2023-04-08)

> Issa: Is the product of two prime numbers always prime?

> ChatGPT: No, the product of two prime numbers is not always
> prime. In fact, it is never prime (**except for the special case
> when one of the prime numbers is 1**, *which is not considered prime
> by definition*). When you multiply two prime numbers, the product
> will have at least two distinct prime factors: the two prime numbers
> being multiplied.

> For example, let's multiply two prime numbers, 3 and 5:

> 3 * 5 = 15

> The result, 15, is not a prime number because it has factors other
> than 1 and itself (3 and 5).

Other than some minor confusion about the status of 1 (an issue that
we also saw with ChatGPT 3.5, albeit to a much greater extent there),
the answer seems correct. ChatGPT 4 volunteered not just that it isn't
always prime, but that it's never prime. It also gave the outline of
an explanation.

## gcd of distinct prime numbers (session 1; 2023-04-08)

> Issa: Is the gcd of two distinct prime numbers always prime?

> ChatGPT: No, the greatest common divisor (gcd) of two distinct prime
> numbers is not always prime. In fact, the gcd of two distinct prime
> numbers is always 1. This is because prime numbers have no common
> divisors other than 1. By definition, a prime number has exactly two
> distinct positive divisors: 1 and the number itself. Since the two
> prime numbers are distinct, they do not share any divisors other
> than 1.

Both the answer and explanation seem correct!

## Status of 1 as a prime number (session 1; 2023-04-08)

In the earlier session, the status of 1 as a prime number emerged
naturally from ChatGPT's incorrect answers to other questions. In this
session, the need didn't arise, but Issa still asked ChatGPT the
equivalent questions to those asked in the original session. So this
time I'm breaking this into a separate section.

> Issa: Is 1 prime or composite?

> ChatGPT: The number 1 is neither prime nor composite. By definition,
> a prime number has exactly two distinct positive divisors: 1 and the
> number itself. Since 1 has only one distinct positive divisor, which
> is 1, it does not meet the criteria for being a prime number.

> A composite number has more than two distinct positive divisors. As
> 1 has only one distinct positive divisor, it also does not meet the
> criteria for being a composite number.

> Issa: Is 1 positive?

> ChatGPT: Yes, 1 is a positive number. Positive numbers are those
> greater than zero, and since 1 is greater than 0, it is considered a
> positive number.

> Issa: Is 1 a positive integer?

> ChatGPT: Yes, 1 is a positive integer. Positive integers are whole
> numbers greater than zero, and since 1 is a whole number greater
> than 0, it is considered a positive integer.

The answers seem correct (and again, keep in mind that the questions
are being asked for equivalence with the original questions where they
made more sense in light of ChatGPT's incorrect responses to previous
questions).

## Sum of prime numbers (session 2; 2023-04-08)

> Issa: Is the sum of two prime numbers always prime?

> ChatGPT: No, the sum of two prime numbers is not always prime. In
> fact, the sum of two prime numbers is often even (except when one of
> them is 2, which is the only even prime number), and even numbers
> greater than 2 are not prime because they can be divided by 2
> without a remainder.

> For example, consider the prime numbers 3 and 5. Their sum is 8,
> which is an even number and not a prime since it can be divided by 2
> and 4. Similarly, the sum of the prime numbers 7 and 11 is 18, which
> is also even and not prime because it has multiple factors, such as
> 2, 3, 6, and 9.

> Issa: What is the sum of the largest and second largest prime number?

> ChatGPT: The concept of the "largest" prime number is not
> applicable, as there is an infinite number of prime
> numbers. According to the famous theorem proven by the ancient Greek
> mathematician Euclid, there is no largest prime number. He
> demonstrated that whenever you have a list of prime numbers, you can
> always find another prime number that is not in your list.

> As a result, it is impossible to determine the sum of the largest
> and second largest prime numbers, since neither of these can be
> definitively identified.

Both answers seem correct! ChatGPT 3.5 had gotten confused and tried
to find the sum of the largest and second largest *known* prime
numbers. ChatGPT 4 got my intent and avoided the trap.

## 15: even or odd? (session 2; 2023-04-08)

These questions made sense in the contex of the original session, as
ChatGPT 3.5 had previously claimed that 15 is even, and continued to
double down on the claim through the answers. ChatGPT 4 is being asked
the same questions for equivalence even though it doesn't make the
same mistakes. So the questions may seem a bit weird.

> Issa: Is 15 an odd integer?

> ChatGPT: Yes, 15 is an odd integer. An integer is considered odd if
> it cannot be evenly divided by 2, meaning there is a remainder when
> divided by 2. In the case of 15, when divided by 2, it results in a
> quotient of 7 with a remainder of 1. Since there is a remainder, 15
> is an odd integer.

> Issa: What are the odd integers between 1 and 20?

> ChatGPT: The odd integers between 1 and 20 are the numbers that
> cannot be evenly divided by 2, leaving a remainder when divided by
> 2. Here is the list of odd integers between 1 and 20:

> 1, 3, 5, 7, 9, 11, 13, 15, 17, 19

> Issa: Explain why 16 is an odd integer

> ChatGPT: Apologies for any confusion, but 16 is actually an even
> integer, not an odd integer. An integer is considered even if it can
> be evenly divided by 2 without leaving a remainder. In the case of
> 16, it can be divided by 2 to give a quotient of 8 with no remainder
> (16 / 2 = 8). Since there is no remainder, 16 is an even integer.

## Sum of odd integers (session 2; 2023-04-08)

> Issa: Can you give an example of two odd integers whose sum is odd?

> ChatGPT: I apologize for any confusion in my previous responses. It
> is not possible for the sum of two odd integers to be odd. When you
> add two odd integers together, the result will always be an even
> integer.

> To understand why, consider the general form of odd integers:

> An odd integer can be written as (2n + 1) or (2m + 1), where n and m are integers.

> When you add two odd integers together, you get:

> (2n + 1) + (2m + 1) = 2n + 2m + 2 = 2(n + m + 1)

> Since the sum can be written as a product of 2 and another integer
> (n + m + 1), the result will always be even.

The answer seems fine!

## Square of odd integer (session 2; 2023-04-08)

> Issa: What is an odd integer whose square is even?

> ChatGPT: There is no odd integer whose square is even. When you
> square an odd integer, the result is always odd.

> To understand why, consider the general form of odd integers:

> An odd integer can be written as (2n + 1), where n is an integer.

> When you square an odd integer, you get:

> (2n + 1)^2 = (2n + 1)(2n + 1) = 4n^2 + 4n + 1 = 2(2n^2 + 2n) + 1

> Since the squared odd integer can be written as 2 multiplied by an
> integer (2n^2 + 2n) plus 1, the result will always be odd.

The answer seems fine! ChatGPT 3.5 had also gotten this correct, but
ChatGPT 4 provides a proof and therefore a more convincing
explanation.

## Sum of prime numbers (round two) (session 2; 2023-04-08)

> Issa: Is the sum of two prime numbers always even?

> ChatGPT: The sum of two prime numbers is not always even. However,
> it is usually even, with one specific exception: when one of the
> prime numbers is 2, which is the only even prime number. In this
> case, the sum of two prime numbers can be odd.

> For example, consider the prime numbers 2 and 3. Their sum is 5,
> which is an odd number.

> But in all other cases where both prime numbers are odd, their sum
> will be even:

> For example, the sum of the prime numbers 3 and 5 is 8, which is an
> even number. Similarly, the sum of the prime numbers 7 and 11 is 18,
> which is also even.

> Issa: Can every positive even integer greater than 4 be expressed as
> the sum of two odd prime numbers?

> Yes, every positive even integer greater than 4 can be expressed as
> the sum of two odd prime numbers. This statement is known as the
> Goldbach Conjecture, which is an unsolved problem in number theory
> that dates back to 1742.

> Although the Goldbach Conjecture has not been proven, extensive
> computational evidence supports the conjecture for very large even
> integers. However, despite the strong empirical evidence, a general
> proof remains elusive.

Looks good, though I would have preferred if ChatGPT led with the
information that the Goldbach Conjecture hasn't been proven, and so
didn't say "Yes" so forcefully at the start.

## 41 and Sophie Germain primes (session 2; 2023-04-08)

> Issa: What is special about 41?

> ChatGPT: The number 41 has a few interesting properties:

> Prime number: 41 is a prime number, meaning it has exactly two
> distinct positive divisors: 1 and itself (41). It cannot be divided
> evenly by any other positive integers.

> Sum of consecutive integers: 41 can be expressed as the sum of
> consecutive integers, specifically the first six positive even
> integers: 2 + 4 + 6 + 8 + 10 + 11 = 41.

> Centered square number: 41 is a centered square number. Centered
> square numbers can be represented as a square with a dot in the
> center and all other dots surrounding the center dot in a square
> shape. The formula for the nth centered square number is given by: 1
> + 8(n-1), where n is a positive integer. In the case of 41, n = 6,
> so 41 = 1 + 8(6-1) = 1 + 8(5) = 1 + 40 = 41.

> Euler's famous prime-generating polynomial: In mathematics, the
> polynomial f(n) = n^2 + n + 41 generates prime numbers for the
> values of n from 0 to 39. This polynomial was discovered by Swiss
> mathematician Leonhard Euler. After n = 39, the generated numbers
> are no longer always prime, but the fact that it generates 40
> consecutive prime numbers is quite remarkable.

> Issa: Is 41 a Sophie Germain prime?

> ChatGPT: Yes, 41 is a Sophie Germain prime. A Sophie Germain prime
  is a prime number p for which 2p + 1 is also prime. These primes are
  named after the French mathematician Sophie Germain.

> In the case of 41, if we apply the definition:

> 2 * 41 + 1 = 82 + 1 = 83

> Since both 41 and 83 are prime numbers, 41 is indeed a Sophie
> Germain prime.

> Issa: Is 41 a safe prime?

> ChatGPT: No, 41 is not a safe prime. A safe prime is a prime number
> of the form 2p + 1, where p is also a prime number. Safe primes are
> a subset of Sophie Germain primes, and p is a Sophie Germain prime.

> In the case of 41, we should check if there is a prime number p for
> which 2p + 1 equals 41. However, we already established that 41 is a
> Sophie Germain prime, where 2 * 41 + 1 equals 83. **Thus, 41 does
> not fit the definition of a safe prime**, as it is not of the form
> 2p + 1 with p being prime.

> Issa: That reasoning does not make sense to me. Why does 41 being a
> Sophie Germain prime mean that 41 is not a safe prime?

> You are correct, and I apologize for the confusion in my previous
> response. The fact that 41 is a Sophie Germain prime does not
> automatically disqualify it from being a safe prime. Let me provide
> a clearer explanation.

> A safe prime is a prime number of the form 2p + 1, where p is also a
> prime number. To determine whether 41 is a safe prime, we need to
> see if there is a prime number p such that 2p + 1 equals 41.

> In this case:

> 2p + 1 = 41

> 2p = 40

> p = 20

> Since 20 is not a prime number, 41 cannot be a safe prime. The
> reasoning in my previous response was indeed incorrect, and I
> apologize for any confusion.

Looks good, other than the flawed reasoning in ChatGPT's first attempt
at trying to figure out if 41 is a safe prime.

## Conclusion

The big jump in capabilities from ChatGPT 3.5 to ChatGPT 4 is
well-known, and I'm hardly the first to comment on it, but nonetheless
I think it is interesting because I created, ran, and published the
prompts and responses against ChatGPT 3.5 *before* ChatGPT 4 became
available, so it is in some sense a "pre-registered" test. The
improvement in the answers was way more than I had expected: I had
been expecting that the errors would reduce but not that they would go
down to such a huge extent.

My experience is fairly similar to that of Bryan Caplan who [saw a
grade jump from D to A on his midterm when going from ChatGPT 3.5 to
ChatGPT
4](https://betonit.substack.com/p/gpt-retakes-my-midterm-and-gets-an).

There was also a qualitative shift in the answers, with ChatGPT 3.5
using proof by example and ChatGPT 4 actually providing mathematically
rigorous proofs in many cases. The improvement to rigor was something
that I had seen partially in [my test on ChatGPT 3.5 in January
2023](https://github.com/vipulnaik/working-drafts/commit/427f5997d48d78c69e3e16eeca99f0b22dc3ffd3),
but that rerun had not cut down on the error rate significantly.

I don't know for sure how ChatGPT 4 managed to improve so much. In
particular, I don't know how much of this improvement stemmed from
ChatGPT 4 having memorized more facts and proofs, versus it becoming a
better reasoner. I suspect the former played a significant role; the
language used in the proofs as well as the kinds of examples provided
suggests that ChatGPT already "knew" the answers. For instance,
ChatGPT invoking the jargon of "integer-valued polynomial" and then
providing the triangular numbers as an example is strongly suggestive
of it having the information in its knowledge base. However, it's
possible that ChatGPT 3.5 also "knew" the correct information and was
just less discerning about how to use it, so it ended up not using
it. So perhaps the improvement to ChatGPT 4 stemmed from it being able
to better prioritize what parts of its knowledge base to invoke based
on the question.

I consider it unlikely that my interactions with ChatGPT 3.5 (that led
to my original post) played a significant role as training data that
helped make ChatGPT 4 so much better. However, I can't rule that out.

A sobering possibility is that the improvement is actually *pretty
small* on the grand spectrum of intelligence; it just looks huge to us
because we are zoomed in on the portion of intelligence at and around
human levels. This harks back to the famous [village idiot/Einstein
scale by
Eliezer](https://www.lesswrong.com/posts/3Jpchgy53D2gB5qdk/my-childhood-role-model)
where he posits that village idiot and Einstein are actually very
close by on the spectrum of intelligence. So if ChatGPT 4 is blowing
our minds by doing correctly what ChatGPT 3.5 couldn't, ChatGPT 5 or 6
or 7 may be way way way beyond what we can imagine.
