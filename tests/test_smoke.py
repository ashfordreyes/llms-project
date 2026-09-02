"""Tests that do not call the API.

The API costs money and is not deterministic, so it does not belong in a test
suite that you want to run constantly. Test the ordinary code here; measure the
model in `evals/`.
"""

from __future__ import annotations

import pytest

from project.prompts import load_prompt


def test_example_prompt_loads():
    assert "billing" in load_prompt("example-classify")


def test_header_is_stripped():
    """The YAML header is documentation for you, not context for the model."""
    body = load_prompt("example-classify")
    assert not body.startswith("---")
    assert "purpose:" not in body


def test_missing_prompt_says_what_exists():
    with pytest.raises(FileNotFoundError, match="Available:"):
        load_prompt("does-not-exist")
