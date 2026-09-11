"""Restore hand-curated fields lost when `academic import --overwrite` regenerates
content/publication/*/index.md from publications.bib.

The Bibtex importer only knows about bibliographic fields (title, authors, date,
journal, doi...). It has no concept of `summary`, or of the NeuroPlaNe-specific
`np_topics` / `np_species` / `featured` classification block that gets added by
hand after each new publication is reviewed, so a fresh `--overwrite` run wipes
those fields for every existing publication, not just the new ones.

This script runs after the importer (and after the "add url_pdf" step) and, for
every publication that already existed in the previous commit, copies its old
`summary` line and its curation block (from the `# --- clasificación
NeuroPlaNe ...` comment onward) back into the freshly generated file, verbatim,
if the freshly generated file doesn't already have them. Genuinely new
publications (no previous commit to compare against) are left untouched, since
there is nothing to restore.
"""

import re
import subprocess
from pathlib import Path

FM_DELIM = re.compile(r"^---\s*$", re.M)
SUMMARY_RE = re.compile(r"^summary:.*$", re.M)
CURATION_BLOCK_RE = re.compile(r"\n(# --- clasificación NeuroPlaNe.*)\Z", re.S)


def split_frontmatter(text: str) -> tuple[str, str] | None:
    matches = list(FM_DELIM.finditer(text))
    if len(matches) < 2:
        return None
    # +1 to skip the newline that terminates the opening "---" line, so the
    # returned front matter starts directly at "title: ..." with no blank line.
    return text[matches[0].end() + 1 : matches[1].start()], text[matches[1].end() :]


def old_file_text(rel_path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"],
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def restore(md: Path) -> bool:
    old_text = old_file_text(md.as_posix())
    if old_text is None:
        return False  # new publication, nothing to restore

    old_split = split_frontmatter(old_text)
    new_text = md.read_text(encoding="utf-8")
    new_split = split_frontmatter(new_text)
    if old_split is None or new_split is None:
        return False

    old_fm, _ = old_split
    new_fm, new_body = new_split
    changed = False

    if "summary:" not in new_fm:
        m = SUMMARY_RE.search(old_fm)
        if m:
            summary_line = m.group(0)
            if re.search(r"^doi:\s*.*$", new_fm, flags=re.M):
                new_fm = re.sub(
                    r"^(doi:\s*.*)$",
                    summary_line + r"\n\1",
                    new_fm,
                    count=1,
                    flags=re.M,
                )
            else:
                new_fm = new_fm.rstrip("\n") + "\n" + summary_line + "\n"
            changed = True

    if "np_topics:" not in new_fm:
        m = CURATION_BLOCK_RE.search(old_fm)
        if m:
            block = m.group(1).rstrip("\n")
            new_fm = new_fm.rstrip("\n") + "\n\n" + block + "\n"
            changed = True

    if changed:
        md.write_text(f"---\n{new_fm}---\n{new_body}", encoding="utf-8")
    return changed


def main() -> None:
    restored = []
    for md in sorted(Path("content/publication").glob("*/index.md")):
        if restore(md):
            restored.append(md.parent.name)

    if restored:
        print(f"Restored curated fields for {len(restored)} publication(s):")
        for slug in restored:
            print(f"  - {slug}")
    else:
        print("No curated fields needed restoring.")


if __name__ == "__main__":
    main()
