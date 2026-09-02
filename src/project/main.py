"""Entry point. Replace this with your actual project.

    python -m project.main "your prompt here"
"""

from __future__ import annotations

import argparse
import sys

import anthropic

from project.client import ask, report_usage, text_of


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="what to ask")
    parser.add_argument(
        "--usage",
        action="store_true",
        help="print token counts to stderr",
    )
    args = parser.parse_args(argv)

    try:
        response = ask(args.prompt)
    except anthropic.AuthenticationError:
        print(
            "ANTHROPIC_API_KEY is not set in this terminal. See the README.",
            file=sys.stderr,
        )
        return 1
    except anthropic.RateLimitError as e:
        retry = e.response.headers.get("retry-after", "60")
        print(f"Rate limited. Try again in {retry}s.", file=sys.stderr)
        return 1
    except anthropic.APIConnectionError:
        print("Could not reach the API. Check your connection.", file=sys.stderr)
        return 1

    print(text_of(response))

    if args.usage:
        print(report_usage(response), file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
