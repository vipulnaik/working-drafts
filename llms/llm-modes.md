# LLM modes

Facebook post: https://www.facebook.com/vipulnaik.r/posts/pfbid02JTSQUtZwD6KW3TV5F1YHJBK8HngJxHmyxADtBjXtdazvXdydpiMUn27HD29y4ACl

Post text:

Here's a summary of the three main modes (with two subtypes each) of using LLMs. I came up with the three modes in my head and then refined and identified the six subtypes collaboratively with Claude. The summary was provided by Claude with light editing by me, although it's very similar to what I would have written myself:

Mode 1: LLM as consultant

- Orientation mode 1: Human get enough understanding to act; inner model is incidental or temporary. Typical for context-switchers, unfamiliar codebases, lookup-heavy work.
- Internalization mode 1: Human builds a durable inner model; LLM is a thinking partner toward that end. Conversations are intermediate cognitive artifacts, revisited and consolidated over time. This is my primary mode.

Mode 2: LLM as directed worker
- Hands-on mode 2: Human checkpoints at each step, catching failures and redirecting. Analogous to frequent testing during development. Robust to poor mental model of the LLM. I use this mode occasionally for writing scripts and executing relatively well-defined tasks.
- Hands-off mode 2: Human delegates and accepts output without deep inspection. Requires a well-calibrated and stable mental model of the LLM — a depreciating asset that resets with model updates and is never fully reasoned from first principles given nondeterminism.

Mode 3: LLM as embedded workflow tool
- Passive ambient mode 3: LLM reacts to human's work stream without explicit invocation (autocomplete, grammar checking). Risks suppressing the human's own generative instinct over time.
- Active co-pilot mode 3: Human still invokes but loop is tight enough to feel continuous (Cursor-style). Judgment ownership can erode without noticing.

A few additional notes:
- The mode 1 / mode 2 distinction blurs in mathematical proof discovery (and in general, in cutting-edge insight discovery), where artifact and understanding are close to the same thing.
- Hands-on mode 2 is the frequent-testing equivalent; hands-off mode 2 requires a much better mental model of a nondeterministic, unspecified system that changes without announcement.
- Mode 3 is where local LLMs have structural advantages; modes 1 and 2 favor cloud for capability reasons currently.

Thoughts?
