# docs-skill

Documentation quality system for Claude Code. Applies scannability, clarity, and accessibility principles to markdown documents and runs automatic language checking with humanizer skills.

## Installation

### Claude Code (primary)

Copy the `docs-skill/` folder to your skills directory:

```bash
cp -r docs-skill/ ~/.claude/skills/docs/
```

### Cursor

Copy `dist/cursor/docs-skill.mdc` to `.cursor/rules/` in your project.

### GitHub Copilot

Copy `dist/copilot/docs-skill.instructions.md` to `.github/` in your project.

### Cline

Copy `dist/cline/docs-skill.md` to `.cline/rules/` in your project.

### Continue

Copy `dist/continue/docs-skill.md` to `.continue/rules/` in your project.

### JetBrains AI

Copy `dist/jetbrains/docs-skill.md` to your project root or AI configuration directory.

### Claude.ai

Upload `dist/docs-skill.skill` via the Claude.ai skill upload interface.

### Generic / Other

Copy `dist/generic/docs-skill.md` to your AI tool's instruction directory.

## Build

Regenerate all dist files from the canonical source:

```bash
py build.py
```

After pushing to GitHub, verify that reference URLs are accessible:

```bash
py build.py --verify
```

## License

MIT
