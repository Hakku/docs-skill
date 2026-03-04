# Development

## Architecture Decisions

### Public repository

The dist files reference `raw.githubusercontent.com` URLs for `principles.md`. Non-CC platforms (Cursor, Copilot, etc.) need HTTP access to the reference file, so the repo must be public.

### main branch, no tag pinning

Dist URLs point to the `main` branch. Tag pinning was considered but rejected: tags don't exist at build time, causing a chicken-and-egg problem where dist URLs would be broken on first build. If versioned releases become necessary later, a `--release v1.0.0` CLI flag can override `GITHUB_BRANCH`.

### Regex frontmatter stripping (not PyYAML)

Claude.ai `.skill` uploads accept only `name` and `description` in YAML frontmatter. The build strips other fields (`allowed-tools`, `metadata`, `license`) using line-by-line regex filtering, the same approach as english-humanizer. Reasons: zero external dependencies, `yaml.dump()` reformats quoting and block scalars unpredictably, and the frontmatter structure is controlled (6 keys, block scalar description).

### CC_READ_LINE handling

The canonical SKILL.md contains a CC-specific instruction: `Lue references/principles.md (suhteessa tämän skillin hakemistoon).` This line tells Claude Code to read the local file via its Read tool.

- **`.skill` ZIP:** Keeps the line — `principles.md` is packaged in the ZIP, so CC can read it locally.
- **Other platforms:** Removes the line — these platforms can't execute CC Read instructions. They get a GitHub URL instead.

Build constants: `CC_READ_LINE` (the line to conditionally remove) and `LOCAL_REF` (the replaceable marker `see references/principles.md` -> GitHub URL).

### No ChatGPT platform

The docs skill uses Claude Code's `Skill` tool to chain humanizer skills (`/finnish-humanizer`, `/english-humanizer`). ChatGPT has no equivalent skill chaining mechanism, so a ChatGPT dist would be incomplete.

### raw.githubusercontent.com URLs

Dist files link to `raw.githubusercontent.com` (not `github.com/blob/`). The blob URL returns an HTML page, not raw markdown content.

## Pipeline

### Current

```
Idea -> /interview -> SPEC.md -> Manual SKILL.md -> /skill-validator -> Manual testing -> build.py -> repo
```

### Target (with Skill Creator)

```
Idea -> /interview -> SPEC.md -> /skill-creator create -> SKILL.md
     -> /skill-validator (validate)
     -> /skill-creator eval -> evals.json + benchmark
     -> /skill-creator optimize -> description optimization
     -> build.py -> repo
```

## Eval Types

| Type | What it tests | Tool | Example |
|------|--------------|------|---------|
| **Trigger eval** | Does the skill trigger from a given prompt? | Skill Creator `run_eval.py` | "Tee README paremmaksi" -> /docs activates |
| **Quality eval** | Does the skill produce correct output? | Skill Creator grader agent | "Paranna README" -> code blocks untouched |

Expectations marked `programmatic-candidate` can later be automated as programmatic assertions when the eval runner supports it. Currently all expectations are LLM-graded.
