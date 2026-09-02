# Evaluation

The point of this directory is to make "the prompt got better" into a number.

## How to start

Start now, with ten cases. Not fifty, not the week before the deadline. Ten
real inputs, chosen so that at least three of them are ones you expect to fail.

A test set made only of easy cases will report 100% and teach you nothing.

## The format

`cases.jsonl` — one JSON object per line:

```json
{"id": "billing-01", "input": "I was charged twice this month", "expected": "billing"}
```

Add fields as you need them. Keep `id` — you will want to talk about specific
cases in your write-up, and "the one about the double charge" is harder to
grep for than `billing-01`.

## Growing it

**Every failure you find becomes a case.** That is the whole discipline. When
you notice the model doing something wrong, the fix is not to tweak the prompt
until that one input works — it is to add the input to `cases.jsonl` first, so
that you find out if your fix breaks something else.

## Running it

**macOS / Linux**

```bash
python evals/run_eval.py
```

**Windows (PowerShell)**

```powershell
python evals/run_eval.py
```

Record the number in your ADR when it changes, along with what you changed.
One change at a time — see `PROMPTING.md` section 2.
