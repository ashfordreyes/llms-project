# Prompt engineering practices for this project

This is the short version of what the course argues, written as things to do
rather than things to know. It is the standard your project is graded against.

---

## 1. A prompt is a file, not a string

The single most common failure in a semester project is a prompt that lives
inside an f-string, gets edited nineteen times, and cannot be reconstructed at
the end of term when you need to explain what you did.

Keep prompts in `prompts/` as `.md` files and load them:

```python
from project.prompts import load_prompt

system = load_prompt("classify")          # reads prompts/classify.md
```

You get three things for free: `git diff` shows what actually changed between
two versions, `git log` gives you the history you will need for your write-up,
and the prompt stops being tangled with the code that sends it.

**Each prompt file carries its own header.** What it is for, what it expects,
what it returns, and — the part people skip — what you tried that did not work.
See [`prompts/example-classify.md`](prompts/example-classify.md).

---

## 2. Change one thing at a time

If you change the instruction, the examples, and the output format together and
the score improves, you have learned nothing about which change did it. This is
the discipline the whole field is bad at and the reason
[Week 5's reading](https://Nalaquq.github.io/llms-and-you/schedule/) exists.

One change, re-run the evals, record the number. Then the next change.

---

## 3. Specificity beats politeness

Models do not respond to enthusiasm. They respond to constraints.

| Weaker | Stronger |
|:---|:---|
| "Please summarize this well." | "Summarize in three sentences. Name the disagreement, not the topic." |
| "Extract the important fields." | "Return JSON with keys `date`, `amount`, `vendor`. Use `null` where absent." |
| "Be accurate." | "Quote the sentence you drew each claim from. If it is not in the text, say `not stated`." |

The pattern: say what the output must contain, what it must not, and what to do
when the input does not support an answer. That last one prevents most
hallucination you will see in this course.

---

## 4. Give the model a way to say "no"

A model with no permitted failure output will invent one. Every prompt that
extracts or answers should specify what to emit when the answer is not there —
`null`, `not stated`, an empty list. Then your eval can check for it.

This is the cheapest hallucination defence that exists and almost nobody does it.

---

## 5. Examples do work, up to a point

Few-shot examples teach format and edge-case handling faster than instructions
do. Two or three good ones usually beat a paragraph of description.

They stop helping — and start hurting — when they are all similar. If your three
examples are three easy cases, you have taught the model that hard cases do not
occur. Pick examples that disagree with each other.

---

## 6. Structure the output when you need to parse it

If you are going to read the response with code, constrain it rather than
regexing prose. Use `output_config` (structured outputs) or ask for JSON and
validate it. Do not write a parser for a format you did not require.

---

## 7. Cache what does not change

Prompt caching bills repeated prefix content at roughly a tenth of the price.
It matters as soon as you have a long system prompt or a document you ask many
questions about. See `client.py`, and the cost work in Week 13.

Order matters: `tools`, then `system`, then `messages`. Put the stable part
first and the varying part last, or nothing caches.

---

## 8. Thinking and effort, not temperature

Current models take `thinking: {"type": "adaptive"}` and
`output_config: {"effort": ...}` with levels `low` through `max`.

- **`low`** — simple, high-volume, or latency-sensitive work.
- **`high`** — the default, and right for most of what you will do.
- **`max`** — when being correct matters more than what it costs.

`temperature` is removed on these models and returns an error. `budget_tokens`
is also gone. If a tutorial tells you otherwise, the tutorial predates the model.

---

## 9. Measure before you believe

Build `evals/cases.jsonl` from real inputs, including the ones you find
annoying. Ten honest cases beat a hundred easy ones. Add a case every time you
find a failure — that is what turns a bug into a regression test.

Your write-up needs a number that moved, not a paragraph saying the prompt got
better.

---

## 10. Write the ADR when you decide, not afterwards

You will be tempted to reconstruct your decisions at the end of term. It does
not work: what you write is a justification of where you ended up, not a record
of what you chose between. The alternatives are the part that gets graded, and
they are exactly the part you cannot remember three weeks later.

Template in [`docs/adr/template.md`](docs/adr/template.md).

And log the change itself in [`CHANGELOG.md`](CHANGELOG.md). The ADR carries the
reasoning; the changelog carries the order things happened in. When you write up
the project, you will want both.
