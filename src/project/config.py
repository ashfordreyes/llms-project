"""One place for the knobs, so they are not scattered through the code.

Everything here is a deliberate choice you should be able to defend in an ADR.
"""

# The model. Opus is the most capable; Sonnet is meaningfully cheaper and often
# enough. Changing this line is a decision -- write it down before you do.
#
#   claude-opus-5     $5.00 / $25.00 per million tokens in / out
#   claude-sonnet-5   $2.00 / $10.00
#   claude-haiku-4-5  $1.00 /  $5.00   (200K context; the others are 1M)
MODEL = "claude-opus-5"

# Ceiling on the response, not a target. Too low truncates mid-sentence.
MAX_TOKENS = 16_000

# How hard the model works before answering: low | medium | high | xhigh | max.
# `high` is the default and right for most work. Raise it when correctness
# matters more than cost; lower it for simple, high-volume calls.
EFFORT = "high"
