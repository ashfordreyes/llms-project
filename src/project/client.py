"""The one place that talks to the API.

Keeping every call in one module means cost accounting, caching, and error
handling are decided once rather than re-invented at each call site.
"""

from __future__ import annotations

import anthropic

from project.config import EFFORT, MAX_TOKENS, MODEL

# Reads ANTHROPIC_API_KEY from the environment. Never pass a key literal here.
client = anthropic.Anthropic()


def ask(
    prompt: str,
    *,
    system: str | None = None,
    cache_system: bool = False,
    effort: str = EFFORT,
) -> anthropic.types.Message:
    """Send one prompt and return the whole response object.

    The whole object, not just the text -- `usage` is where cost lives, and you
    will need it in Week 13. Use `text_of()` when you only want the words.

    Set `cache_system=True` when the same system prompt is reused across calls
    and is long (roughly 1024 tokens or more). Below that it silently will not
    cache. See PROMPTING.md section 7.
    """
    kwargs: dict = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": effort},
    }

    if system is not None:
        if cache_system:
            kwargs["system"] = [
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        else:
            kwargs["system"] = system

    return client.messages.create(**kwargs)


def text_of(response: anthropic.types.Message) -> str:
    """Pull the text out of a response.

    `response.content` is a list of blocks and not all of them are text -- with
    thinking on, the first one usually is not. Indexing `content[0].text` works
    until it suddenly does not.
    """
    return "".join(block.text for block in response.content if block.type == "text")


def count_tokens(prompt: str, *, system: str | None = None) -> int:
    """What this prompt will cost you in input tokens, before you send it.

    Use this rather than guessing, and rather than a tokenizer from a different
    vendor -- token counts are model-specific and another vendor's number is
    simply wrong here.
    """
    kwargs: dict = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system is not None:
        kwargs["system"] = system

    return client.messages.count_tokens(**kwargs).input_tokens


def report_usage(response: anthropic.types.Message) -> str:
    """A one-line cost summary. Print it while you are developing.

    `cache_read_input_tokens` staying at 0 across repeated calls means your
    caching is not working -- something in the prefix is changing between
    requests.
    """
    u = response.usage
    return (
        f"in {u.input_tokens:,} | out {u.output_tokens:,} | "
        f"cache write {getattr(u, 'cache_creation_input_tokens', 0):,} | "
        f"cache read {getattr(u, 'cache_read_input_tokens', 0):,}"
    )
