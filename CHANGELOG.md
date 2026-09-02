# Changelog

What changed in this project, and when.

This is graded alongside your ADR log, and the two are not the same thing. An
**ADR** says *why* you chose something over the alternative you rejected. A
**changelog** says *what actually moved, and in what order.* Keep both — at the
end of term you will need to answer both questions, and neither record answers
the other's.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/):
group entries under `Added`, `Changed`, `Fixed`, or `Removed`, newest at the
top.

## How to use it

Write the entry when you make the change, not at the end of the week. An entry
is one or two lines. If a change was significant enough to need reasoning,
write the ADR too and link it from here.

The useful habit: when an eval score moves, say which change moved it. That
sentence is most of your final write-up already written.

---

## [Unreleased]

### Added

- Started from the course template.

<!--
Delete the example below once you have real entries.

### Changed

- Split the classification prompt in two, one pass to extract and one to
  label. Eval went 6/10 -> 9/10; the failures were all the model trying to do
  both at once. See ADR-0003.

### Fixed

- `other` was never being returned. The prompt listed it but gave no rule for
  when to use it, so the model treated it as decorative.
-->
