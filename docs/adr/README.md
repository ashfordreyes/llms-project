# Decision log

One file per decision, numbered in the order you made them.

This is graded as a primary artifact, not as paperwork — see the
[assignment](https://Nalaquq.github.io/llms-and-you/assignments/) and the
[guide](https://Nalaquq.github.io/llms-and-you/guides/writing-adrs/).

## What counts as a decision worth recording

Anything where you could have done it another way and the other way was not
obviously worse. Choosing a model. Choosing what "correct" means in your evals.
Deciding to split one prompt into two. Deciding *not* to use retrieval.

Not: which variable name you used, or anything with only one sensible answer.

## The part that gets graded

**The alternatives.** An ADR whose alternatives section says "we could have not
done this" is an ADR with no alternatives in it. What gets credit is a real
option, described well enough that a reader can see why someone would have
chosen it, followed by why you did not.

## The part that is hard

Writing it *as you decide*, not afterwards. These are different activities and
the second one does not work — what you produce is a defence of where you ended
up rather than a record of what you were choosing between. You will notice the
difference the first time you try to reconstruct one.

Copy [`template.md`](template.md) to `0001-your-decision.md` and start.

## Not the same as the changelog

Both are graded and they do not overlap. An ADR answers *why this and not that*.
[`CHANGELOG.md`](../../CHANGELOG.md) answers *what moved, and when*. A change
worth an ADR usually gets a changelog line too, pointing at it.
