"""Post a short announcement to Bluesky for newly added publications.

Run from the repo root. Reads publication slugs from the NEW_FILES env var
(newline-separated paths to content/publication/<slug>/index.md), or from a
single --slug argument for manual testing. Credentials come from the
BLUESKY_HANDLE / BLUESKY_APP_PASSWORD env vars (GitHub Actions secrets).
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

API = "https://bsky.social/xrpc"
TEXT_LIMIT = 290


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, fm_text, _ = text.split("---\n", 2)
    return yaml.safe_load(fm_text) or {}


def find_image(pub_dir: Path) -> Path:
    for name in ("featured.jpg", "featured.png"):
        candidate = pub_dir / name
        if candidate.exists():
            return candidate
    return Path("assets/media/sharing.png")


def build_text(title: str, journal: str, year: str, url: str) -> str:
    text = f"New paper: {title}"
    if journal:
        text += f" — published in {journal}"
        if year:
            text += f" ({year})"
    text += f".\n{url}"
    if len(text) > TEXT_LIMIT:
        # Trim the title first, keep journal/year/url intact.
        overflow = len(text) - TEXT_LIMIT
        title = title[: max(0, len(title) - overflow - 1)].rstrip() + "…"
        text = build_text_raw(title, journal, year, url)
    return text


def build_text_raw(title: str, journal: str, year: str, url: str) -> str:
    text = f"New paper: {title}"
    if journal:
        text += f" — published in {journal}"
        if year:
            text += f" ({year})"
    text += f".\n{url}"
    return text


def login(handle: str, password: str) -> tuple[str, str]:
    resp = requests.post(
        f"{API}/com.atproto.server.createSession",
        json={"identifier": handle, "password": password},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["accessJwt"], data["did"]


def upload_thumb(headers: dict, img_path: Path) -> dict | None:
    if not img_path.exists():
        return None
    mime = "image/jpeg" if img_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    resp = requests.post(
        f"{API}/com.atproto.repo.uploadBlob",
        headers={**headers, "Content-Type": mime},
        data=img_path.read_bytes(),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["blob"]


def announce(index_path: Path, headers: dict, did: str) -> None:
    pub_dir = index_path.parent
    slug = pub_dir.name
    fm = parse_frontmatter(index_path)

    title = fm.get("title", slug)
    journal = re.sub(r"\*", "", str(fm.get("publication", ""))).strip()
    date = str(fm.get("date", ""))
    year = date[:4] if date else ""
    url = f"https://neuroplanelab.org/publication/{slug}/"
    summary = fm.get("summary") or (f"{journal}, {year}." if journal else "")

    text = build_text(title, journal, year, url)
    thumb = upload_thumb(headers, find_image(pub_dir))

    external = {"uri": url, "title": title, "description": summary}
    if thumb:
        external["thumb"] = thumb

    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "langs": ["en"],
        "embed": {"$type": "app.bsky.embed.external", "external": external},
    }

    resp = requests.post(
        f"{API}/com.atproto.repo.createRecord",
        headers=headers,
        json={"repo": did, "collection": "app.bsky.feed.post", "record": record},
        timeout=30,
    )
    resp.raise_for_status()
    print(f"Posted {slug} -> {resp.json().get('uri')}")


def main() -> None:
    handle = os.environ.get("BLUESKY_HANDLE")
    password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not handle or not password:
        print(
            "Missing BLUESKY_HANDLE / BLUESKY_APP_PASSWORD env vars — "
            "add them as repo secrets before this workflow can post.",
            file=sys.stderr,
        )
        sys.exit(1)

    if "--slug" in sys.argv:
        slug = sys.argv[sys.argv.index("--slug") + 1]
        files = [Path(f"content/publication/{slug}/index.md")]
    else:
        raw = os.environ.get("NEW_FILES", "")
        files = [Path(line.strip()) for line in raw.splitlines() if line.strip()]

    if not files:
        print("No new publications to announce.")
        return

    access_jwt, did = login(handle, password)
    headers = {"Authorization": f"Bearer {access_jwt}"}

    for f in files:
        if not f.exists():
            print(f"Skipping {f}: file not found", file=sys.stderr)
            continue
        announce(f, headers, did)


if __name__ == "__main__":
    main()
