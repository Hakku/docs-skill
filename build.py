"""Docs Skill v1 build script.

Generates all dist files from the canonical docs-skill/SKILL.md source.
Usage: py build.py [--verify]
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

REPO = Path(__file__).parent
SKILL_MD = REPO / "docs-skill" / "SKILL.md"
PRINCIPLES_MD = REPO / "docs-skill" / "references" / "principles.md"
DIST = REPO / "dist"

GITHUB_BRANCH = "main"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/Hakku/docs-skill/{GITHUB_BRANCH}/docs-skill/references/principles.md"

LOCAL_REF = "see references/principles.md"
CC_READ_LINE = 'Lue `references/principles.md` (suhteessa tämän skillin hakemistoon). Nämä ohjaavat arviointia.'

PLATFORMS = {
    "cursor": {
        "path": "cursor/docs-skill.mdc",
        "frontmatter": lambda d: [
            f"description: {_yaml_str(d)}",
            'globs: "**/*.md,**/*.txt"',
            "alwaysApply: false",
        ],
    },
    "copilot": {
        "path": "copilot/docs-skill.instructions.md",
        "frontmatter": lambda d: [
            "name: docs-skill",
            'applyTo: "**/*.md,**/*.txt"',
            f"description: {_yaml_str(d)}",
        ],
    },
    "cline": {"path": "cline/docs-skill.md"},
    "continue": {
        "path": "continue/docs-skill.md",
        "frontmatter": lambda d: [
            "name: docs-skill",
            'globs: "**/*.md,**/*.txt"',
            "alwaysApply: false",
            f"description: {_yaml_str(d)}",
        ],
    },
    "jetbrains": {"path": "jetbrains/docs-skill.md"},
    "generic": {"path": "generic/docs-skill.md"},
    "agents": {"path": "agents/AGENTS.md"},
}


def parse_skill():
    """Return (body, short_description) from SKILL.md.

    Handles YAML multi-line block scalar (description: >) by collecting
    all indented continuation lines after the key.
    """
    text = SKILL_MD.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md: frontmatter missing")

    fm = parts[1]
    fm_lines = fm.splitlines()

    desc_lines = []
    in_desc = False
    for line in fm_lines:
        if re.match(r"^description:\s*>", line):
            in_desc = True
            continue
        if in_desc:
            if line.startswith(" ") or line.startswith("\t"):
                desc_lines.append(line.strip())
            else:
                break

    if desc_lines:
        desc_full = " ".join(desc_lines)
    else:
        match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        desc_full = match.group(1).strip() if match else ""

    sentences = desc_full.split(". ")
    desc_short = ". ".join(sentences[:2])
    if not desc_short.endswith("."):
        desc_short += "."

    body = parts[2].lstrip("\n")
    return body, desc_short


def _yaml_str(value: str) -> str:
    """Return YAML-safe double-quoted string for frontmatter values."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _checked_replace(text, old, new, label):
    """Replace old->new and assert exactly one occurrence existed."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"build: expected exactly 1 occurrence of {label!r}, found {count}. "
            "Check SKILL.md reference strings match LOCAL_REF / CC_READ_LINE."
        )
    return text.replace(old, new)


def build_platforms(body, desc):
    """Generate platform-specific dist files.

    Removes CC_READ_LINE (CC-specific Read instruction) and replaces
    LOCAL_REF with the GitHub raw URL.
    """
    # Remove the full CC_READ_LINE line (including newline)
    dist_body = _checked_replace(body, CC_READ_LINE + "\n", "", "CC_READ_LINE")
    # Replace local reference with GitHub URL
    dist_body = _checked_replace(dist_body, LOCAL_REF, GITHUB_RAW_URL, "LOCAL_REF")

    results = []
    for name, cfg in PLATFORMS.items():
        out = DIST / cfg["path"]
        out.parent.mkdir(parents=True, exist_ok=True)

        fm_fn = cfg.get("frontmatter")
        if fm_fn:
            fm_lines = fm_fn(desc)
            content = "---\n" + "\n".join(fm_lines) + "\n---\n\n" + dist_body
        else:
            content = dist_body

        out.write_text(content, encoding="utf-8", newline="\n")
        chars = len(content)
        results.append((name, cfg["path"], chars))

    return results


def build_skill():
    """Build dist/docs-skill.skill for Claude.ai.

    Claude.ai only accepts name + description in YAML frontmatter.
    Strips allowed-tools, metadata before packaging.
    ZIP includes SKILL.md + references/principles.md.
    CC_READ_LINE is kept (file is packaged in ZIP).
    """
    text = SKILL_MD.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md: frontmatter missing")

    fm = parts[1]
    fm_lines = fm.splitlines()

    def _short_desc(full):
        s = ". ".join(full.split(". ")[:2])
        if not s.endswith("."):
            s += "."
        return s[:197] + "..." if len(s) > 200 else s

    kept = []
    in_desc = False
    desc_lines = []
    for line in fm_lines:
        if re.match(r"^name:", line):
            kept.append(line)
            in_desc = False
        elif re.match(r"^description:\s*>", line):
            in_desc = True
            desc_lines = []
        elif re.match(r"^description:\s*(.+)$", line) and not in_desc:
            m = re.match(r"^description:\s*(.+)$", line)
            kept.append(f"description: {_yaml_str(_short_desc(m.group(1).strip()))}")
        elif in_desc:
            if line.startswith(" ") or line.startswith("\t"):
                desc_lines.append(line.strip())
            else:
                kept.append(f"description: {_yaml_str(_short_desc(' '.join(desc_lines)))}")
                in_desc = False
                if re.match(r"^name:", line):
                    kept.append(line)

    if in_desc and desc_lines:
        kept.append(f"description: {_yaml_str(_short_desc(' '.join(desc_lines)))}")

    if not any(k.startswith("name:") for k in kept):
        raise ValueError("SKILL.md: no name found in frontmatter — cannot build .skill")
    if not any(k.startswith("description:") for k in kept):
        raise ValueError("SKILL.md: no description found in frontmatter — cannot build .skill")

    # Keep CC_READ_LINE (file is in ZIP), but replace LOCAL_REF with GitHub URL
    skill_body = parts[2]
    skill_body = _checked_replace(skill_body, LOCAL_REF, GITHUB_RAW_URL, "LOCAL_REF (.skill)")

    stripped = "---\n" + "\n".join(kept) + "\n---" + skill_body

    skill_path = DIST / "docs-skill.skill"
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    fixed_time = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(skill_path, "w", zipfile.ZIP_DEFLATED) as zf:
        info = zipfile.ZipInfo("docs-skill/SKILL.md", date_time=fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, stripped)

        info = zipfile.ZipInfo("docs-skill/references/principles.md", date_time=fixed_time)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, PRINCIPLES_MD.read_text(encoding="utf-8"))

    return skill_path


def verify_github_url():
    """HTTP HEAD to GITHUB_RAW_URL — expect 200."""
    print(f"\nVerifying: {GITHUB_RAW_URL}")
    req = Request(GITHUB_RAW_URL, method="HEAD")
    try:
        resp = urlopen(req, timeout=10)
        code = resp.status
        if code == 200:
            print(f"  OK ({code})")
        else:
            print(f"  WARNING: unexpected status {code}")
    except Exception as e:
        print(f"  FAILED: {e}")


def main():
    body, desc = parse_skill()
    print("Docs Skill v1 -- Build\n")

    # Clean dist/ to prevent stale files from prior versions persisting.
    if DIST.exists():
        if not DIST.resolve().is_relative_to(REPO.resolve()):
            raise ValueError(f"DIST path {DIST} is outside repo — refusing to delete")
        shutil.rmtree(DIST)
    DIST.mkdir()

    results = build_platforms(body, desc)
    print("Platform packages:")
    for name, path, chars in results:
        print(f"  {name:12s} {path:50s} {chars:>6,} chars")

    skill_path = build_skill()
    print(f"\nSKILL: {skill_path.relative_to(REPO)}")
    with zipfile.ZipFile(skill_path) as zf:
        print(f"  Contents: {', '.join(zf.namelist())}")

    print("\nDone.")

    if "--verify" in sys.argv:
        verify_github_url()


if __name__ == "__main__":
    main()
