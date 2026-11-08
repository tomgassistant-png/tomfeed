#!/usr/bin/env python3
"""Rebuild index.html from feed.json.

Does not add or rewrite ordinary feed items. Every build includes:
- an edition line at the top, in Asia/Jerusalem, from the same timestamp as the footer
- a root font size of 138% (120% plus another 15%)
- an "Edit interests (curiosities.md)" link near the edition line and in the footer
- the noindex robots meta tag

An Off Leash update is shown only in the edition that first adds it. This script
marks that edition on the item. A later build, once generated_at has moved on,
drops the item. No placeholder is added when there is no new update.
"""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
FEED_PATH = ROOT / "feed.json"
OUT_PATH = ROOT / "index.html"
EDIT_URL = "https://github.com/tomgassistant-png/tomfeed/edit/main/curiosities.md"
EDIT_LABEL = "Edit interests (curiosities.md)"
UTC = ZoneInfo("UTC")
JERUSALEM = ZoneInfo("Asia/Jerusalem")
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def parse_generated_at(value: str) -> datetime:
    text = value.strip()
    text = re.sub(r"\s+UTC$", "", text)
    if text.endswith("Z"):
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    else:
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            dt = datetime.strptime(text, "%Y-%m-%d %H:%M")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def edition_line(generated_at: datetime) -> str:
    local = generated_at.astimezone(JERUSALEM)
    hour12 = local.hour % 12 or 12
    ampm = "AM" if local.hour < 12 else "PM"
    local_text = (
        f"{WEEKDAYS[local.weekday()]}, {MONTHS[local.month - 1]} {local.day}, "
        f"{local.year}, {hour12}:{local.minute:02d} {ampm}"
    )
    utc_text = generated_at.strftime("%H:%M")
    return f"Edition: {local_text} Israel time ({utc_text} UTC)"


def footer_stamp(generated_at: datetime) -> str:
    return generated_at.strftime("generated %Y-%m-%d %H:%M UTC")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def is_off_leash(item: dict) -> bool:
    title = item.get("title") or ""
    source = item.get("source") or ""
    return title.startswith("Off Leash") or "Off Leash" in source


def is_utility(item: dict) -> bool:
    url = item.get("url") or ""
    return "wttr.in" in url or "finance.yahoo.com" in url


def apply_off_leash(feed: dict) -> bool:
    """Keep an Off Leash item only for the edition that first adds it.

    The item is pinned below weather and markets. The next edition drops it.
    When none is new, the section is omitted (no placeholder).
    Returns True when feed.json should be rewritten.
    """
    edition = str(feed.get("generated_at") or "")
    others = []
    showing = []
    changed = False
    for item in feed["items"]:
        if not is_off_leash(item):
            others.append(item)
            continue
        shown_edition = item.get("off_leash_edition")
        if item.get("off_leash_shown") and shown_edition == edition:
            showing.append(item)
            continue
        if item.get("off_leash_shown"):
            changed = True
            continue
        item = dict(item)
        item["off_leash_shown"] = True
        item["off_leash_edition"] = edition
        showing.append(item)
        changed = True
    if len(showing) > 1:
        showing.sort(key=lambda it: it.get("published_at") or "", reverse=True)
        showing = showing[:1]
        changed = True
    prefix = []
    rest = []
    passed_utility = False
    for item in others:
        if not passed_utility and is_utility(item):
            prefix.append(item)
        else:
            passed_utility = True
            rest.append(item)
    new_items = prefix + showing + rest
    if new_items != feed["items"]:
        changed = True
    feed["items"] = new_items
    return changed


def render_item(item: dict) -> str:
    title = item["title"]
    url = item["url"]
    source = item["source"]
    published = item["published_at"]
    klass = "item"
    if title.startswith("Off Leash") or "Off Leash" in source:
        klass = "item off-leash"
    body = item.get("body") or ""
    body_html = f'\n      <div class="item-body">{esc(body)}</div>' if body else ""
    return f'''    <article class="{klass}" data-item-url="{esc(url)}">
      <h2 class="headline"><a href="{esc(url)}">{esc(title)}</a></h2>
      <p class="meta"><time class="rel-time" datetime="{esc(published)}">{esc(published)}</time> · <span class="source">{esc(source)}</span> · <a class="url" href="{esc(url)}">{esc(url)}</a></p>{body_html}
    </article>'''


def render_page(feed: dict) -> str:
    generated = parse_generated_at(str(feed["generated_at"]))
    edition = edition_line(generated)
    stamp = footer_stamp(generated)
    articles = "\n".join(render_item(item) for item in feed["items"])
    edit = f'<a href="{esc(EDIT_URL)}">{esc(EDIT_LABEL)}</a>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
  <title>Curiosities Feed</title>
  <style>
    :root {{
      --bg: #f8f9fa;
      --text: #1f2937;
      --muted: #6b7280;
      --link: #1d4ed8;
      --border: #e5e7eb;
      --headline: #111827;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ font-size: 138%; }}
    body {{
      font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
      padding: 2rem 1rem 4rem;
    }}
    .wrap {{ max-width: 42rem; margin: 0 auto; }}
    .edition {{
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 0.85rem;
    }}
    .edition a, footer a {{ color: var(--link); }}
    header {{
      border-bottom: 1px solid var(--border);
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
    }}
    h1 {{
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .sub {{ color: var(--muted); font-size: 0.9rem; margin-top: 0.35rem; }}
    .item {{
      border-bottom: 1px solid var(--border);
      margin-bottom: 1.15rem;
      padding-bottom: 1.15rem;
    }}
    .item.off-leash {{
      background: #fffbeb;
      border-left: 3px solid #d97706;
      padding-left: 0.85rem;
    }}
    .headline {{ font-size: 1.12rem; font-weight: 700; line-height: 1.35; margin-bottom: 0.35rem; }}
    .headline a {{ color: var(--headline); text-decoration: none; }}
    .headline a:hover {{ color: var(--link); text-decoration: underline; }}
    .meta, .url {{ color: var(--muted); font-size: 0.82rem; }}
    .url {{ word-break: break-all; text-decoration: none; }}
    .url:hover {{ color: var(--link); text-decoration: underline; }}
    .item-body {{
      white-space: pre-wrap;
      margin-top: 0.75rem;
      font-size: 0.95rem;
      line-height: 1.5;
      max-width: 40rem;
    }}
    footer {{
      color: var(--muted);
      font-size: 0.8rem;
      margin-top: 2rem;
    }}
    footer p + p {{ margin-top: 0.35rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <p class="edition">{esc(edition)} · {edit}</p>
    <header>
      <h1>Curiosities Feed</h1>
      <p class="sub">Newest first</p>
    </header>
    <main>
{articles}
    </main>
    <footer>
      <p>{esc(stamp)}</p>
      <p>Interests come from curiosities.md. {edit}</p>
    </footer>
  </div>
  <script>
    (function () {{
      function rel(iso) {{
        var then = new Date(iso);
        if (isNaN(then)) return iso;
        var sec = Math.floor((Date.now() - then.getTime()) / 1000);
        if (sec < 60) return "just now";
        var min = Math.floor(sec / 60);
        if (min < 60) return min === 1 ? "1 minute ago" : min + " minutes ago";
        var hr = Math.floor(min / 60);
        if (hr < 24) return hr === 1 ? "1 hour ago" : hr + " hours ago";
        var day = Math.floor(hr / 24);
        if (day < 7) return day === 1 ? "1 day ago" : day + " days ago";
        var week = Math.floor(day / 7);
        if (week < 5) return week === 1 ? "1 week ago" : week + " weeks ago";
        var month = Math.floor(day / 30);
        return month === 1 ? "1 month ago" : month + " months ago";
      }}
      document.querySelectorAll("time.rel-time").forEach(function (el) {{
        var iso = el.getAttribute("datetime");
        if (iso) el.textContent = rel(iso);
      }});
    }})();
  </script>
</body>
</html>
'''


def main() -> None:
    feed = json.loads(FEED_PATH.read_text())
    if apply_off_leash(feed):
        FEED_PATH.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n")
    page = render_page(feed)
    if 'name="robots" content="noindex, nofollow, noarchive, nosnippet"' not in page:
        raise SystemExit("missing robots meta")
    if "font-size: 138%" not in page:
        raise SystemExit("missing root font size")
    if page.count(EDIT_LABEL) < 2 or EDIT_URL not in page:
        raise SystemExit("missing edit link")
    OUT_PATH.write_text(page)
    print(edition_line(parse_generated_at(str(feed["generated_at"]))))
    print(f"wrote {OUT_PATH.name} ({len(feed['items'])} items)")


if __name__ == "__main__":
    main()
