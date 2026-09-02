"""Run the prompt against every case and report what it got wrong.

    python evals/run_eval.py

This is deliberately simple. It is a starting point you are expected to change
once you know what "correct" means for your project -- exact match is rarely it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project.client import ask, text_of  # noqa: E402
from project.prompts import load_prompt  # noqa: E402

CASES = Path(__file__).parent / "cases.jsonl"


def load_cases() -> list[dict]:
    with CASES.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def grade(output: str, expected: str) -> bool:
    """Did the model get it right?

    Exact match on a JSON field, for the example prompt. Replace this -- most
    projects need something looser (does it contain the fact?) or stricter
    (is every field right?). How you grade IS your definition of correct, so
    it belongs in an ADR.
    """
    try:
        return json.loads(output).get("queue") == expected
    except json.JSONDecodeError:
        return False


def main() -> int:
    system = load_prompt("example-classify")
    cases = load_cases()

    failures = []
    for case in cases:
        try:
            output = text_of(ask(case["input"], system=system)).strip()
        except anthropic.AuthenticationError:
            print(
                "ANTHROPIC_API_KEY is not set in this terminal. See the README.",
                file=sys.stderr,
            )
            return 1
        except anthropic.RateLimitError as e:
            retry = e.response.headers.get("retry-after", "60")
            print(
                f"Rate limited at case {case['id']}. Try again in {retry}s.",
                file=sys.stderr,
            )
            return 1

        if not grade(output, case["expected"]):
            failures.append((case, output))

    passed = len(cases) - len(failures)
    print(f"{passed}/{len(cases)} passed\n")

    for case, output in failures:
        print(f"  {case['id']}")
        print(f"    input:    {case['input']}")
        print(f"    expected: {case['expected']}")
        print(f"    got:      {output}\n")

    # Non-zero exit on failure, so this can gate a commit later if you want.
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
