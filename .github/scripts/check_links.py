"""Check for broken links across the site's content.

Two kinds of checks:
1. `url_pdf` fields in publications must point to a file that actually
   exists under static/ (this is what caught us out with duplicate/renamed
   PDFs before — now it's automatic).
2. Every http(s) URL found anywhere in content/**/*.md (DOIs, collaborator
   sites, social links, journal pages...) gets requested and its status
   checked.

Definite dead links (404/410, or a missing local url_pdf file) fail the
job. Everything else (403s from bot-blocking publishers, timeouts, 5xx) is
only a warning — those happen too often on academic sites to make a
reliable hard gate, but they're still worth seeing in the log.
"""

import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
STATIC = ROOT / "static"

URL_RE = re.compile(r"https?://[^\s\)\]\"'>]+")
URL_PDF_RE = re.compile(r"^url_pdf:\s*(\S+)\s*$", re.M)

HEADERS = {
    # A generic "bot" UA gets flat-out blocked (403/404) by some sites
    # (Bluesky, LinkedIn...) regardless of whether the link is actually
    # fine, so pretend to be a normal browser instead.
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 15
HARD_FAIL_CODES = {404, 410}


def check_local_pdfs() -> list[str]:
    failures = []
    for md in sorted(CONTENT.glob("publication/*/index.md")):
        text = md.read_text(encoding="utf-8")
        m = URL_PDF_RE.search(text)
        if not m:
            continue
        rel = m.group(1).strip().strip("'\"").lstrip("/")
        if not (STATIC / rel).exists():
            failures.append(f"{md.relative_to(ROOT)}: url_pdf points to missing file static/{rel}")
    return failures


def collect_urls() -> dict[str, list[str]]:
    urls: dict[str, list[str]] = {}
    for md in sorted(CONTENT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for match in URL_RE.findall(text):
            url = match.rstrip(".,;:")
            urls.setdefault(url, []).append(str(md.relative_to(ROOT)))
    return urls


def check_url(url: str) -> tuple[bool, str]:
    # HEAD support is unreliable across the web (some servers/SPAs 404 or
    # 405 it even though GET works fine), so only trust a HEAD success —
    # any HEAD failure falls back to a real GET before we call it broken.
    last_detail = "unknown"
    for method in ("head", "get"):
        try:
            resp = requests.request(
                method, url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=(method == "get")
            )
            if resp.status_code < 400:
                return True, f"{resp.status_code}"
            last_detail = f"{resp.status_code}"
        except requests.RequestException as exc:
            last_detail = f"error: {exc.__class__.__name__}"
    return False, last_detail


def main() -> None:
    hard_failures = check_local_pdfs()
    warnings: list[str] = []

    urls = collect_urls()
    print(f"Checking {len(urls)} unique URLs found across content/...\n")

    for url, sources in sorted(urls.items()):
        ok, detail = check_url(url)
        code = None
        if not ok and detail.isdigit():
            code = int(detail)
        if ok:
            status = "OK"
        elif code in HARD_FAIL_CODES:
            status = "DEAD"
        else:
            status = "WARN"

        if status != "OK":
            where = ", ".join(sources[:3]) + ("…" if len(sources) > 3 else "")
            line = f"[{status}] {url} ({detail}) — in {where}"
            print(line)
            if status == "DEAD":
                hard_failures.append(line)
            else:
                warnings.append(line)

    print(f"\n{len(urls)} URLs checked, {len(warnings)} warnings, {len(hard_failures)} dead links.")

    if hard_failures:
        print("\nDead links / missing files (failing the job):")
        for f in hard_failures:
            print(f" - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
