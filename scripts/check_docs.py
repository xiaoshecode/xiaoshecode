"""Validate handbook records and relative links without network access."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def main():
    errors = []
    records = list((ROOT / "data/repositories").glob("*.json"))
    if not records:
        errors.append("No repository records found")
    expected_pages = set()
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8-sig"))
        for key in ("name", "summary", "purpose", "setup", "usage", "structure", "changes", "checks", "limitations"):
            if key not in record:
                errors.append(f"{path.name}: missing {key}")
        destination = SITE / "repos" / record["name"] / "index.html"
        expected_pages.add(destination.resolve())
        if not destination.is_file():
            errors.append(f"Missing generated page: {record['name']}")
    for destination in (SITE / "repos").glob("*/index.html"):
        if destination.resolve() not in expected_pages:
            errors.append(f"Stale page has no source record: {destination.parent.name}")
    pages = list(SITE.rglob("*.html"))
    for path in pages:
        parser = Links()
        parser.feed(path.read_text(encoding="utf-8"))
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(SITE.resolve()):
                errors.append(f"{path.name}: link outside site: {link}")
            elif not target.exists():
                errors.append(f"{path.relative_to(SITE)}: broken link: {link}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(records)} records, {len(pages)} HTML pages; all local links resolve")


if __name__ == "__main__":
    main()
