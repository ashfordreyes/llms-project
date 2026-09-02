# Individual Project — LLMs & You

A starting point for your semester project. Clone it, rename it, and make it
yours.

This template is deliberately **empty of content and opinionated about
process.** It does not contain a project. It contains the structure that the
projects which go well in this course all turn out to have, and the three
practices that separate them from the ones that do not:

1. **Your prompts are source code.** They live in `prompts/`, they are edited
   deliberately, and their history is readable. See [`PROMPTING.md`](PROMPTING.md).
2. **Your decisions are written as you make them.** Why you chose something goes
   in `docs/adr/`; what actually changed goes in [`CHANGELOG.md`](CHANGELOG.md).
   Both are graded — see the
   [ADR guide](https://Nalaquq.github.io/llms-and-you/guides/writing-adrs/).
3. **Your claims are measured.** A change that "seems better" is a guess until
   `evals/` says otherwise.

---

## Getting started

**1. Make your own copy, and clone it.** One command, with the
[GitHub CLI](https://cli.github.com/) signed in:

**macOS / Linux**

```bash
gh repo create llms-project \
  --template Nalaquq/llms-and-you-project \
  --public --clone
cd llms-project
```

**Windows (PowerShell)**

```powershell
gh repo create llms-project `
  --template Nalaquq/llms-and-you-project `
  --public --clone
cd llms-project
```

Do not fork, and do not clone this repository directly. A fork stays linked to
this one; a direct clone points at a repository you cannot push to. `--template`
gives you a repository that is yours, with a clean history.

Prefer the website? [Create one from the
template](https://github.com/Nalaquq/llms-and-you-project/generate), then clone
what you made — step 2 shows how.

**2. Clone it and set up an environment.**

Every command in this README is given twice, once for each platform, including
where the two are identical. Use the half that matches your machine and ignore
the other; mixing them is the most common way this goes wrong.

**macOS / Linux**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
cd YOUR-PROJECT
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
cd YOUR-PROJECT
```

Then the environment, which is genuinely different:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell says `running scripts is disabled on this system`, run this once
in the same window and then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Your prompt starts with `(.venv)` when it is active. Activate again every time
you open a new terminal.

**3. Set your API key.** It goes in an environment variable, never in a file.

**macOS / Linux**

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

Lasts until you close the terminal. To make it permanent, add that line to
`~/.zshrc` or `~/.bashrc` and open a new one.

**Windows (PowerShell)**

```powershell
$env:ANTHROPIC_API_KEY = 'sk-ant-...'
```

Lasts until you close the window. To make it permanent:

```powershell
[Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-...', 'User')
```

Then open a new terminal — the one you typed it in will not see it.

If you get `AuthenticationError`, this is what is wrong. Check the key is set in
*this* terminal: `echo $ANTHROPIC_API_KEY` on macOS and Linux,
`echo $env:ANTHROPIC_API_KEY` on Windows.

**4. Turn on the credential guard.** Once per clone.

**macOS / Linux**

```bash
git config core.hooksPath .githooks
```

**Windows (PowerShell)**

```powershell
git config core.hooksPath .githooks
```

This blocks a commit that contains something shaped like an API key. A key
pushed to GitHub is scraped within minutes, and deleting it in the next commit
does not help — it stays in the history.

**5. Check that it works,** with the virtual environment active.

**macOS / Linux**

```bash
python -m project.main "Say hello in exactly five words."
```

**Windows (PowerShell)**

```powershell
python -m project.main "Say hello in exactly five words."
```

**6. Open [`TODO.txt`](TODO.txt) and put something in it.** It is the running
list of what the next version of your prompt has to do, kept in sections by
where each item ends up — in the prompt, in `evals/`, in an ADR, or in a
question for your instructor. An hour after you have the thought, you no longer
have the thought.

---

## What is in here

| Path | What it is for |
|:---|:---|
| `TODO.txt` | What the next version of your prompt needs to do. Start using it in week one. |
| `PROMPTING.md` | The practices this course grades. Read this first. |
| `prompts/` | Your prompts, as versioned files. One per prompt, not one per project. |
| `src/project/` | Your code. `client.py` is written for you; the rest is yours. |
| `evals/` | Your test set. Start it in week one, not the week before it is due. |
| `docs/adr/` | Your decision log — why you chose things. Graded. |
| `CHANGELOG.md` | What changed and when. Graded alongside the ADRs. |
| `tests/` | Ordinary tests, for the parts that are ordinary code. |

Rename `src/project/` to something that describes your project, and update the
`name` in `pyproject.toml` to match.

---

## The rules that are not obvious

**Do not put a key in your code.** Not even temporarily, not even in a file you
plan to delete. See step 4.

**Do not commit model output as if it were a result.** An output is evidence of
one run. A result is what `evals/` reports across your whole test set.

**Do not adjust `temperature`.** Nearly every prompt engineering tutorial online
tells you to. On current frontier models that parameter has been removed and
sending it returns an error. Use `effort` instead — see `PROMPTING.md`. When
sources contradict, [the API reference](https://docs.claude.com/en/api/overview)
wins.

**Cite AI use.** The course policy applies to your project exactly as it applies
to everything else, and the two ways to fail it are in
[the syllabus](https://Nalaquq.github.io/llms-and-you/syllabus/#using-ai).
