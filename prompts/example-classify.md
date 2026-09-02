---
purpose: Sort an incoming support message into one of four queues.
input: One message, plain text, typically under 200 words.
output: JSON — {"queue": one of billing|technical|account|other, "confidence": low|high}
failed:
  - "Asked for a confidence score 0-1. Got 0.85 for everything, including
     inputs it clearly could not classify. Two buckets are honest; a decimal
     is false precision."
  - "Left out the `other` category. It forced every unclear message into
     `technical`, which made the technical queue useless."
---

Sort the support message into exactly one queue.

- `billing` — payments, invoices, refunds, pricing.
- `technical` — something is broken or not behaving as documented.
- `account` — login, permissions, closing or transferring an account.
- `other` — anything else, including messages that are too vague to sort.

Use `other` freely. A message that could plausibly be two queues, or that does
not say enough to tell, belongs in `other` — do not guess between them.

Return `confidence: low` whenever you used `other`, or whenever a different
reader could reasonably have picked a different queue.

Return only the JSON object. No explanation.
