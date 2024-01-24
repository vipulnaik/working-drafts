# Is conditional awaiting misleading?

Question url: https://stackoverflow.com/questions/77870459/is-conditional-awaiting-misleading

Question title: Is conditional awaiting misleading?

I've been toying with a JavaScript implementation similar to the one provided at https://developer.mozilla.org/en-US/docs/Web/API/Scheduling/isInputPending#examples and had a discussion with a colleague around whether the implementation might be misleading. Here is the abstracted-out version of the discussion.

For the purpose of this discussion, I assume that we're inside an async function and don't care about return values (i.e., we are interested only in side-effects and in the order in which things execute). These assumptions may not be strictly necessary but they simplify things for us.

Let's say `condition` is a boolean, `conditionalCodeBlock` is a code block that we only want to run when `condition` is true (and for simplicity we can assume it returns a promise), and `unconditionalCodeBlock` is a block we want to execute (a) after the promise for `conditionalCodeBlock` evaluates if `condition` is true, (b) immediately and synchronously otherwise (i.e., without yielding).

In the context of the examples for isInputPending that I linked at the beginning, `condition` would be a check for navigator.scheduling.isInputPending, `conditionalCodeBlock` is just yielding (nothing too special happens inside there), and `unconditionalCodeBlock` is the code we actually want to execute if there is no pending input.

Here are two versions of the code that do this:

Long version without `await`:

```javascript
if (condition) {
    conditionalCodeBlock.then(unconditionalCodeBlock);
} else {
    unconditionalCodeBlock;
}
```

Short version with `await`:

```
if (condition) {
    await conditionalCodeBlock;
}
unconditionalCodeBlock;
```

Both of them achieve the same thing effectively; the latter version is shorter because `unconditionalCodeBlock` doesn't need to be repeated in the two cases.

However, the flip side of the second block is that it hides the fact that `unconditionalCodeBlock` is being invoked in different ways depending on whether `condition` is true or false: it's invoked asynchronously if true and synchronously if false. A colleague pointed out that sweeping this complexity under the rug can be misleading and make it harder to reason about the code, so his preference would be for the more verbose first way.

I'm curious what people think about the pros and cons of the two ways of structuring the code, and what criteria they would use to decide which way is better in a specific situation.

Here is some more specific code (combining different code snippets that my colleague and I wrote into one giant code snippet) just to showcase that async/await in JavaScript works as I described, and provide a little more clarity on how things yield to each other:

```javascript
var innerFunctionUsingPromise = (str) => {
  console.log('before promise evaluation: ' + str)
  return Promise.resolve(str)
    .then(v => {console.log('attached to promise: ' + v); return v;})
}

var innerFunctionNotUsingPromise = (str) => {
  console.log('no promise evaluation: ' + str);
}

var conditionalTrue = async () => {
  console.log('Pre: Conditional True')
  if (true) {
    console.log('before innerFunctionNotUsingPromise in conditionalTrue without await')
    innerFunctionNotUsingPromise('conditionalTrue without await')
    console.log('before innerFunctionUsingPromise in conditionalTrue without await')
    innerFunctionUsingPromise('conditionalTrue without await')
    console.log('before innerFunctionNotUsingPromise in conditionalTrue with await')
    await innerFunctionNotUsingPromise('conditionalTrue with await')
    console.log('before innerFunctionUsingPromise in conditionalTrue with await')
    await innerFunctionUsingPromise('conditionalTrue with await')
    console.log('Post: Conditional True Inside')
  }
  console.log('Post: Conditional True Outside')
}

var conditionalFalse = async () => {
  console.log('Pre: Conditional False')
  if (false) {
    console.log('before innerFunctionNotUsingPromise in conditionalFalse without await')
    innerFunctionNotUsingPromise('conditionalFalse without await')
    console.log('before innerFunctionUsingPromise in conditionalFalse without await')
    innerFunctionUsingPromise('conditionalFalse without await')
    console.log('before innerFunctionNotUsingPromise in conditionalFalse with await')
    await innerFunctionNotUsingPromise('conditionalFalse with await')
    console.log('before innerFunctionUsingPromise in conditionalFalse with await')
    await innerFunctionUsingPromise('conditionalFalse with await')
    console.log('Post: Conditional False Inside')
  }
  console.log('Post: Conditional False Outside')
}

console.log('Pre: Global')
conditionalTrue()
conditionalFalse()
console.log('Post: Global')
```

This is the result:

```
Pre: Conditional True
before innerFunctionNotUsingPromise in conditionalTrue without await
no promise evaluation: conditionalTrue without await
before innerFunctionUsingPromise in conditionalTrue without await
before promise evaluation: conditionalTrue without await
before innerFunctionNotUsingPromise in conditionalTrue with await
no promise evaluation: conditionalTrue with await
Pre: Conditional False
Post: Conditional False Outside
Post: Global
attached to promise: conditionalTrue without await
before innerFunctionUsingPromise in conditionalTrue with await
before promise evaluation: conditionalTrue with await
attached to promise: conditionalTrue with await
Post: Conditional True Inside
Post: Conditional True Outside
```

The above code can help verify these things:

* As expected, none of the stuff inside `if (false)` in `conditionalFalse` gets triggered. This also means that the code after the `if (false)` executes immediately and synchronously as there is no yielding happening in that case.
* All functions, whether using `await` or not, start executing immediately when invoked.
* In the case of an `await`ed function, the caller yields the microtask queue, so even when the awaited function completes (and even if it doesn't include any promise evaluation!) the control doesn't immediately return to the caller; everything that is in the queue at the time of yielding gets executed first.
* Similarly, any time we get to a `Promise.resolve`, the microtask queue is yielded, so the code inside will get executed after everything else in the queue at the time of yielding.
