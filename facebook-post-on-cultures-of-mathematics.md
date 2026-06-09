Post link: https://www.facebook.com/vipulnaik.r/posts/pfbid021NK5jwEtmdpYdKKUqzBbyL8gGm1RVr6ndht4PBcxbsx5b1orvCNBnSzAy1vsJ82vl

Content:

In mathematics, we often hear about the two cultures of mathematics (theory-building versus problem-solving), popularized by Tim Gowers in his paper https://www.dpmms.cam.ac.uk/~wtg10/2cultures.pdf.

However, my own read of mathematics is that there are three distinct cultures that interact in interesting ways.

(1) Earned confidence / puzzle elegance culture: You negotiate the exact definitions of concepts, the exact axioms for your system, the weakest hypotheses for your conclusion, the strongest conclusion for your hypotheses, the quantification of failure of a statement holding. You don't relax into a world and absorb its ambient assumptions; you're constantly questioning what is true and what the minimal way of achieving it is. The goal isn't just understanding a mathematical object, it's understanding the texture of reasoning. This is very similar to elegant puzzle design: every piece of the puzzle plays a role, nothing is superfluous.

Examples in mathematics: large parts of late 19th century / early 20th century algebra that are now undergraduate algebra. Introductory point set topology, introductory abstract algebra, large parts of group theory, the useful parts of category theory, axiomatic set theory (ZFC, before getting into cardinals), first-order model theory, proof theory, computability theory, complexity theory.

Examples in software engineering: type system culture, formal verification culture, many aspects of security culture, test-driven development, various kinds of contract-based coding for APIs and data storage (normal forms, etc.), alerting and monitoring systems, principled performance optimization that is about identifying the exact structure of memory or CPU usage.

(2) World immersion culture: You inhabit a world so thoroughly that its assumptions fade into the background. You keep building on top of it and drawing on the richness that it gives you.

Examples in mathematics: pretty much the upper/esoteric end of large parts of 21st century mathematics, including algebraic geometry and algebraic number theory (the Langlands program),  various parts of abstract algebra particularly as we get to infinite and very complicated objects (geometric group theory, rings and fields), research-grade algebraic topology (in contrast with the basics of homology and cohomology that are strongly earned confidence), set theory when you are deep into infinities, model theory beyond first-order, category theory once it stops being about categories as a useful framework for mathematics and starts being about categories for categories' sake.

Examples in software engineering: framework-driven development where you inhabit the framework (like React or Angular) so deeply that you forget that JavaScript and HTML exist as things on their own, large-scale architectural patterns (domain-driven design, hexagonal architecture), platform and abstraction immersion (AWS, Kubernetes) where you forget the real hardware underneath.

(3) Problem-solving culture: The problems are in some sense "arbitrary" -- the goal of them is to develop or showcase machinery that can solve those problems and other similar problems. The connection between problem and machinery lacks the puzzle elegance of earned confidence culture -- the machinery is rarely exactly powered to the problem, sometimes being underpowered, sometimes overpowered.

Examples in mathematics: large parts of combinatorics including the Erdos tradition, large parts of analysis (such as PDEs) and analytic number theory. The exception in combinatorics that's more earned confidence is things like flow/cut theorems and regularity lemmas, but these are a small part of the field.

Examples in software engineering: large amounts of coding work fit here -- solve the problem somehow; the machinery may not be an exact fit and the solution may not match the problem exactly. Some performance optimization hacks and security vulnerability detection live here (the rest lives in earned confidence culture). Useful open source tooling also often lives here (occasionally it has earned confidence character).

Colophon: This was based on discussion with Claude Sonnet 4.6. The core insights were mine; some nuances and the subfield classification informed by Claude's responses to my thoughts. The final copy was written entirely by me. The conversation with Claude went into several additional details not included in this post.
