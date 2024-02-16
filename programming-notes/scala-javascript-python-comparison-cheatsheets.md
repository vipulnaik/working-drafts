# Scala / JavaScript / Python comparison cheatsheets

These cheatsheets are mostly for my own benefit, but I thought it
might be a good idea to make them public as there's no proprietary
information here. Caveat emptor -- may contain mistakes, and may miss
nuances.

My experience with these languages as of 2024-02-14:

* Scala: 6 years doing extensive coding and data analysis in Scala,
  2-3 years using it more sporadically.

* JavaScript: 6 years coding sporadically in it, but spending a lot
  more time (over 7-8 years) *reading* JavaScript code regulary to
  understand how particular codebases work.

* Python: 1-2 years coding regularly (though not extensively) in
  Python, and 7-8 years of occasional reading and writing of Python
  code.

## Variable assignment and typing

Construct | Scala | JavaScript | Python
-- | -- | -- | --
constant declaration | `val <variableName> = <variableValue>` | `const <variableName> = <variableValue>` | N/A, everything can be reassigned, but convention is to use capital letters for things intended to be constant
variable declaration | `var <variableName> = <variableValue>` | `var <variableName> = <variableValue>` (functoin scope) and `let <variableName> = <variableValue>` (block scope) | `<variableName> = <variableValue>`
type information | optional but necessary if implicitly recasting: `(var\|const) <variableName>:<variableType> = <variableValue>` | not declared | not declared

## Function/procedure/method definition

Construct | Scala | JavaScript | Python
-- | -- | -- | --
function/procedure/method structure | `def <nameForInvocation> (<args to invoke with, separated by commas, with type signature needed for each arg>) { ... body ... }` | `function <nameForInvocation> (<args to invoke with, separated by commas>) { ... body ...}`| `def <nameForInvocation>(<args to invoke with, separated by commas>):\n...body...`
return type signature | optional, can be included as `:<returnType>` after closing paren for args and before opening brace for body; necessarily if implicit type-casting is needed; if a return type is specified, there should be an `=` after that and before the opening brace | N/A | N/A
return syntax | last executed line before orderly end, including last line within conditional blocks; explicit `return` also allowed for early return | explicit `return` | explicit `return`
lambda function syntax | `<args> => <what to do with args>` | `<args> => <what to do with args>` | `lambda <args>: <what to do with args>`

## Array cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
explicit array enumeration | `List(<elements separated by comma>)` | `[<elements separated by comma>]` | `[<elements separated by comma>]`
access to element at index `i` of array `myList` (starting from 0) | `myList(i)` | `myList[i]` | `myList[i]`
size of array `myList` | `myList.size` | `myList.length` | `len(myList)`
access to last element of array `myList` | `myList.last` | `myList[myList.length - 1]` | `myList[-1]`
slice from element `i` (inclusive) to element `j` (non-inclusive) of array `myList` | `myList.slice(i,j)` | `myList.slice(i,j)` | `myList.slice(i,j)`
map an array `myList` via function `myFunc` | `myList.map(myFunc)` | `myList.map(myFunc)` | `list(map(myFunc, myList))`
apply something to each element of `myList` (without saving) | `myList.foreach(...)` | `myList.forEach(...)` | for loop: `for ... in myList:\n...`
every element of `myList` satisfies condition `myCond` | `myList.forall(myCond)` | `myList.every(myCond)` | `all(myCond(u) for u in myList)`
there is an element of `myList` satisfying condition `myCond` | `myList.exists(myCond)` | `myList.some(myCond)` | `any(myCond(u) for u in myList)`
return an array that is the subsequence of `myList` that satisfies condition `myCond` | `myList.filter(myCond)` | `myList.filter(myCond)` | `list(filter(myCond, myList))`
list of integers from 1 to `n` (`n` a predefined positive integer) | `(1 to n).toList` | `[...Array(n).keys()].map(i => i + 1)` | `list(range(1, n + 1))`

## String cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
join an array of strings `myList` using a separator string `mySep` (which could be empty) | `myList.mkString(mySep)` | `myList.join(mySep)` | `mySep.join(myList)`
split a string `myString` over a separator string `mySep` | `myString.split(mySep)` | `myString.split(mySep)` | `myString.split(mySep)` (note that unlike the join case, this is *not* interchanged from the other two languages)
reverse a string `myString` | `myString.reverse` | `myString.split("").reverse().join("")` | `"".join(list(reversed(myString)))`
concatenate strings `myString1` and `myString2` | `myString1 + myString2` | `myString1 + myString2` | `myString1 + myString2`
interpolate string `myString` (variable name) into a larger string | `s"...${myString}..."` | `\`...${myString}...\`` | `f"...{myString}..."`

## Tuples cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
explicit tuple construction | `(<entries of tuple separated by comma>)` | N/A | `(<entries of tuple separated by comma>)`
access to coordinate `i` of tuple `myTup` (starting from 1) | `myTup._<i>` (only explicit numbers can be used in the subscript; variables, even constant | N/A | `myTup[i - 1]` (as Python treats the tuple as an array, and uses 0-indexing for arrays)

## Sorting (and related manipulation) cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
return a sorted version of `myList` | `myList.sortBy(identity)` | `[...myList].sort()` (the `...` is to prevent myList itself from being mutated) | `sorted(myList)`
sort `myList` in-place | no direct way; just reassign the `myList.sortBy(identity)` to `myList`| `myList.sort()` (also returns the sorted version) | `myList.sort()` (returns nothing)
return a sorted version of `myList` by a function `myFunc` | `myList.sortBy(myFunc)` | `[...myList].sort(myFunc)` | `sorted(myList, key = myFunc)`
return a reversed version of `myList` | `myList.reverse` | `[...myList].reverse()` | `list(reversed(myList))`
reverse `myList` in place | no direct way; just rassign `myList.reverse` to `myList` | `myList.reverse()` (also returns the reversed version) | `myList.reverse()` (returns nothing)

## Condition syntax cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
parentheses around condition for if? | yes | yes | needed only if condition spans multiple lines
then | N/A, put the instruction directly after the condition, usually with `) {\n` separator | N/A, put the instruction directly after the condition, usually with `) {` separator | N/A, put the instruction in the next linem with `:\n` separator
else if | `else if` | `else if` | `elif`

## Case match cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
opener of cases | `<expression> match` | `switch(<expression>)` | `match <expression>` (new from Python 3.10)
case lines | `case <value> =>` | `case <value>:` | `case <value>:`
case line for matching everything | `case _ =>` | `default:` | `case _:`
breaks after matching a case? | yes | no | yes

## Exception-handling cheatsheet

Construct | Scala | JavaScript | Python
-- | -- | -- | --
try/catch exceptions | `try {...} catch {<case matches>}` | `try {...} catch(e) {<code that can access e, the variable into which the exception is stored>} finally {...}` | `try {...} except <exception type (optional)>: {...} except <next exception type (optional)> {...} ... finally {...}`
throw exception | `throw new Exception(<message>)` (can also throw a more specific exception class) | `throw new Error(<message>)` (the `new` is optional) | `raise Exception(<message>)`

## Async cheatsheet

NOTE: Scala has Promises too; see for instance
[here](https://www.baeldung.com/scala/futures-promises). But for
practical purposes we only use futures.

Construct | Scala | JavaScript | Python
-- | -- | -- | --
holder of async stuff | `Future` | `Promise` | ??
connector for stuff to execute once the async thing returns | `.map` | `.then` | ??
forced await on `myAsyncThing`| `Await.result(myAsyncThing, Duration.inf)` | `await myAsyncThing` | ??
exception-handling for the async thing | `.recover` | `.catch` | ??
returning an async `thingToReturn` synchronously | `Future.successful(thingToReturn)` | N/A | ??
returning an async `thingToReturn` asynchronously | `Future(thingToReturn)` | `Promise.resolve(thingToReturn)` | ??
convert a sequence of async stuff into a single async thing | `Future.sequence` | `Promise.all` | ??
