"""Generate a default featured image for a "new paper" news post.

Usage (from the repo root):
    python3 .github/scripts/make_news_card.py content/post/<slug> [--force]

Reads the post's `doi`, finds the publication page with the same DOI under
content/publication/, and draws a 1600x1000 card (8:5, the aspect of the news
thumbnails) with journal, year, paper title and authors in the lab palette.
Writes <post>/featured.png, which the site and the Bluesky announcer pick up.

Needs Pillow, the Source Sans 3 fonts (installed locally, or pass --font-dir)
and `rsvg-convert` to render the logo (skipped with a warning if missing).
"""

import argparse
import io
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000
PAPER = "#f7f6f2"
INK = "#1a2432"
SOFT = "#5f6b7a"
BLUE = "#1e56c2"
BLUE_DEEP = "#0f3a7d"
ACCENT = "#c8631f"
LINE = "#dcdad2"
PI = "Herranz-Pérez"
MARGIN = 120

FONT_DIRS = [Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/usr/share/fonts")]


def frontmatter(path: Path) -> dict:
    """Minimal parser for the flat front matter Hugo Blox writes (no PyYAML needed):
    `key: value`, values folded onto indented lines, and `- item` lists."""
    _, fm, _ = path.read_text(encoding="utf-8").split("---\n", 2)
    data, key = {}, None
    for raw in fm.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] not in " -" and ":" in raw:
            key, _, val = raw.partition(":")
            key, val = key.strip(), val.strip()
            data[key] = [] if val == "" else val.strip("'\"")
        elif key and raw.lstrip().startswith("- "):
            if not isinstance(data[key], list):
                data[key] = []
            data[key].append(raw.lstrip()[2:].strip().strip("'\""))
        elif key and isinstance(data[key], str):
            data[key] = (data[key] + " " + raw.strip()).strip("'\"")
    return data


def find_publication(doi: str) -> dict:
    for idx in Path("content/publication").glob("*/index.md"):
        fm = frontmatter(idx)
        if str(fm.get("doi", "")).strip().lower() == doi.lower():
            return fm
    sys.exit(f"No publication in content/publication with doi {doi}")


def font(name: str, size: int, extra_dirs: list[Path]) -> ImageFont.FreeTypeFont:
    for d in extra_dirs + FONT_DIRS:
        hits = list(d.rglob(name)) if d.exists() else []
        if hits:
            return ImageFont.truetype(str(hits[0]), size)
    sys.exit(f"Font {name} not found (use --font-dir)")


def short_authors(authors: list[str]) -> str:
    """'Thao P Phan' -> 'Phan TP'; keep first, PI and last, ellipsis between."""
    def fmt(full: str) -> str:
        parts = full.split()
        last = parts[-1]
        # keep compound surnames joined by hyphen as they are
        initials = "".join(p[0] for p in parts[:-1] if p[0].isalpha())
        return f"{last} {initials}".strip()

    names = [fmt(a) for a in authors]
    if len(names) <= 6:
        return ", ".join(names)
    pi = next((n for n in names if n.startswith(PI)), None)
    out = f"{names[0]}, {names[1]} … "
    if pi and pi not in names[:2] + names[-1:]:
        out += f"{pi} … "
    return out + names[-1]


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def logo(height: int) -> Image.Image | None:
    exe = shutil.which("rsvg-convert")
    svg = Path("assets/media/logo-full.svg")
    if not exe or not svg.exists():
        print("warning: rsvg-convert or logo SVG missing, drawing without logo", file=sys.stderr)
        return None
    png = subprocess.run([exe, "-h", str(height), str(svg)], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir", type=Path)
    ap.add_argument("--force", action="store_true", help="overwrite an existing featured image")
    ap.add_argument("--font-dir", type=Path, action="append", default=[])
    args = ap.parse_args()

    out = args.post_dir / "featured.png"
    existing = list(args.post_dir.glob("featured.*"))
    if existing and not args.force:
        sys.exit(f"{existing[0]} already exists (use --force)")

    post = frontmatter(args.post_dir / "index.md")
    doi = str(post.get("doi", "")).strip()
    if not doi:
        sys.exit("Post has no `doi` in its front matter")
    pub = find_publication(doi)

    title = pub["title"]
    journal = str(pub.get("publication", "")).replace("*", "")
    year = str(pub.get("date", ""))[:4]
    authors = short_authors(pub.get("authors", []))

    f_eyebrow = font("SourceSans3-Semibold.otf", 30, args.font_dir)
    f_journal = font("SourceSans3-Semibold.otf", 40, args.font_dir)
    f_authors = font("SourceSans3-Regular.otf", 32, args.font_dir)
    f_url = font("SourceSans3-Semibold.otf", 28, args.font_dir)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # left accent band + top rule, as in the site masthead
    d.rectangle([0, 0, 18, H], fill=BLUE)
    d.rectangle([18, 0, W, 6], fill=BLUE_DEEP)

    x, text_w = MARGIN, W - 2 * MARGIN
    fy = H - 190  # footer rule; kept clear of Bluesky's 1.91:1 centre crop

    # title: biggest size that fits in at most 4 lines
    for size in (84, 76, 68, 62, 56, 50):
        f_title = font("SourceSans3-Semibold.otf", size, args.font_dir)
        lines = wrap(d, title, f_title, text_w)
        if len(lines) <= 4:
            break
    lh = int(size * 1.16)
    a_lines = wrap(d, authors, f_authors, text_w)[:2]
    block = 58 + 84 + lh * len(lines) + 30 + 44 * len(a_lines)

    # centre the text block vertically between the top rule and the footer
    y = max(100, (fy - block) // 2 + 10)
    spaced(d, (x, y), "NEW PAPER", f_eyebrow, ACCENT, 6)
    y += 58
    d.text((x, y), f"{journal} · {year}" if year else journal, font=f_journal, fill=BLUE)
    y += 84
    for ln in lines:
        d.text((x, y), ln, font=f_title, fill=INK)
        y += lh
    y += 30
    for ln in a_lines:
        d.text((x, y), ln, font=f_authors, fill=SOFT)
        y += 44

    # footer
    d.line([x, fy, W - MARGIN, fy], fill=LINE, width=2)
    lg = logo(120)
    if lg:
        img.paste(lg, (x - 14, fy + 22), lg)
    url = "neuroplanelab.org"
    d.text((W - MARGIN - d.textlength(url, font=f_url), fy + 64), url, font=f_url, fill=SOFT)

    img.save(out, optimize=True)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
