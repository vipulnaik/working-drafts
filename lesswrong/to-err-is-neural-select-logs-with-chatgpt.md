# To err is neural: select logs with ChatGPT

This post includes some portions of my logs with ChatGPT, where I
asked it basic arithmetic questions and it made several mistakes. I
have used **bold** for cases where it made incorrect statements, and
*italics* for cases where it made correct statements that directly
contradicted nearby incorrect statements. Actual conversation in block
quotes, my commentary on it not in block quotes. I generally include
my comment *after* the portion of the conversation being commented
upon.

I have various high-level thoughts on this, but not enough time to
flesh those thoughts out and subject them to critical scrutiny. So I
stick to fairly local commentary here.

## Product of negative numbers

The chat logs below are continuous, and formed the beginning of a
session:

> Vipul: What is an example of an odd negative number?

> ChatGPT: An example of an odd negative number is -5. Negative
> numbers are numbers that are less than zero and are represented by a
> negative sign (-). Odd numbers are integers that are not divisible
> by 2. -5 is an odd negative number because it is less than zero and
> is not divisible by 2. Some other examples of odd negative numbers
> include -3, -7, and -9.

So far, so great!

> Vipul: What is an example where two negative numbers multiply to
> give a negative number?

> ChatGPT: **An example where two negative numbers multiply to give a
> negative number is (-3) x (-4) = 12.** *When two negative numbers
> are multiplied together, the result is a positive number. This is
> because the negative signs cancel each other out. For example, (-3)
> x (-4) = (-1) x 4 = 4, which is a positive number. So, in this case,
> the product of two negative numbers is a positive number.*

> On the other hand, if we have three negative numbers, the result
> will be a negative number. For example, (-3) x (-4) x (-5) = (-1) x
> (-1) x 20 = (-1) x 20 = -20, which is a negative number.

> It's important to remember that when multiplying or dividing
> numbers, the order in which the operations are performed is
> important. This is because multiplication and division are not
> commutative, meaning that the order in which the numbers are
> multiplied or divided matters. In the example above, the order in
> which the negative numbers are multiplied is important because it
> determines whether the result is positive or negative.

Here, I successfully trip up ChatGPT by asking to come up with an
example where none is possible. ChatGPT comes up with a fake
example. But when it elaborates, it provides the reason why no example
is possible! And yet it does not realize that it has done so.

> Vipul: Can the product of two negative numbers be negative?

> **Yes, the product of two negative numbers can be negative.** *As I
> mentioned in my previous response, when two negative numbers are
> multiplied together, the result is a positive number, because the
> negative signs cancel each other out.* **For example, (-3) x (-4) =
> (-1) x 4 = 4, which is a positive number.**

> However, if we have three negative numbers, the result will be a
> negative number. For example, (-3) x (-4) x (-5) = (-1) x (-1) x 20
> = (-1) x 20 = -20, which is a negative number.

> It's important to remember that when multiplying or dividing
> numbers, the order in which the operations are performed is
> important. This is because multiplication and division are not
> commutative, meaning that the order in which the numbers are
> multiplied or divided matters. In the examples above, the order in
> which the negative numbers are multiplied is important because it
> determines whether the result is positive or negative.

I tried asking ChatGPT the underlying question without assuming the
answer, but ChatGPT still gave the same wrong answer.
