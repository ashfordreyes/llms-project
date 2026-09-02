"""Load prompts from files instead of embedding them in code.

See PROMPTING.md section 1 for why this is not just tidiness.
"""

from __future__ import annotations

from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(name: str) -> str:
    """Return the text of `prompts/{name}.md`, without its YAML header.

    The header is documentation for you. The model should not see it.
    """
    path = PROMPT_DIR / f"{name}.md"
    if not path.exists():
        available = sorted(p.stem for p in PROMPT_DIR.glob("*.md"))
        raise FileNotFoundError(f"no prompt named {name!r}. Available: {available}")

    text = path.read_text(encoding="utf-8")

    # Strip a leading `---`-delimited header if there is one.
    if text.startswith("---"):
        _, _, rest = text.partition("---")
        header, sep, body = rest.partition("---")
        if sep:
            return body.strip()

    return text.strip()
