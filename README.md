# docs-skill

Documentation quality system for AI coding assistants. Evaluates and improves markdown documents against three principles: **scannability**, **writing quality**, and **accessibility**. Chains humanizer skills to clean up AI-sounding language in the output (Finnish or English).

## What it does

1. **Evaluates** your document against structured principles (headers, paragraph length, topic sentences, keyword placement, sentence complexity, jargon)
2. **Rewrites** prose for clarity while preserving code blocks, tables, and links byte-for-byte
3. **Chains humanizer** to remove AI-sounding patterns -- Finnish text gets `finnish-humanizer`, English gets `english-humanizer`

Works on READMEs, guides, API docs, and any markdown meant for humans. Won't touch AI tool configuration files (CLAUDE.md, SKILL.md, etc.).

## Usage

In Claude Code:

```
/docs path/to/README.md
```

Other platforms: paste the skill instructions and provide the document in your prompt.

## Installation

**Claude Code** -- copy the skill folder:

```bash
cp -r docs-skill/ ~/.claude/skills/docs/
```

Other platforms:

| Platform | File | Destination |
|----------|------|-------------|
| Cursor | `dist/cursor/docs-skill.mdc` | `.cursor/rules/` |
| GitHub Copilot | `dist/copilot/docs-skill.instructions.md` | `.github/` |
| Cline | `dist/cline/docs-skill.md` | `.cline/rules/` |
| Continue | `dist/continue/docs-skill.md` | `.continue/rules/` |
| JetBrains AI | `dist/jetbrains/docs-skill.md` | Project root |
| Claude.ai | `dist/docs-skill.skill` | Upload via skill interface |
| Generic | `dist/generic/docs-skill.md` | AI tool's instruction directory |

## Build

Regenerate all dist files from the canonical source (`docs-skill/SKILL.md`):

```bash
py build.py
```

Verify that reference URLs resolve after pushing:

```bash
py build.py --verify
```

## How it works

`docs-skill/SKILL.md` is the canonical source. `build.py` generates platform-specific versions by stripping Claude Code frontmatter and swapping local file paths to GitHub raw URLs. For Claude.ai, it produces a `.skill` ZIP that bundles the principles file inside.

See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture decisions and the eval framework.

## License

MIT
