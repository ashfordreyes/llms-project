# Prompts

One file per prompt. Not one file per project, and not a string inside a `.py`.

The reason is in [`PROMPTING.md`](../PROMPTING.md) section 1, but the short
version: at the end of term you have to explain what you changed and why it
helped. `git log prompts/classify.md` answers that. Your memory does not.

## The header

Every prompt file starts with a YAML header. `load_prompt()` strips it before
sending, so it costs you no tokens and you can be honest in it.

The field people skip is `failed`. It is the most valuable one — both for your
write-up and for the version of you in three weeks who is about to retry
something that already did not work.

See [`example-classify.md`](example-classify.md). Delete it once you have your
own.
