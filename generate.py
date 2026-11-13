#!/usr/bin/env python3
"""Rebuild index.html from feed.json.

Does not add or rewrite ordinary feed items. Every build includes:
- an edition line at the top, in Asia/Jerusalem, from the same timestamp as the footer
- a root font size of 138%
- an "Edit interests (curiosities.md)" link near the edition line and in the footer
- the noindex robots meta tag
- no save button (on hold): do not emit a save link on any item
- target="_blank" rel="noopener noreferrer" on every outbound anchor

An item may include an optional summary string. When that string is non-empty,
the page shows it as a paragraph directly under the item's title, link, and meta line.

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

# URLs already saved to Google Tasks, so the button shows the saved state.
INITIAL_SAVED = [
    "https://aljazeera.com/news/2026/10/14/how-israels-yellow-line-is-reshaping-southern-lebanon",
    "https://app.xmind.com/share/bA9yLCfq????xid=S46oLiVN",
    "https://arstechnica.com/space/2026/07/how-hard-is-it-to-build-orbital-data-centers-actually",
    "https://cambridge.org/core/journals/antiquity/collections/trade-and-connections",
    "https://e-ir.org/p/trumps-vision-for-greenland-and-the",
    "https://haaretz.com/opinion/2026-10-02/ty-article-opinion/.premium/no-the-new-yorker-did-not-blame-punctuation-for-palestinian-suffering/000001a0-fdff-d8c5-aff7-fdff69110000",
    "https://marginalrevolution.com/marginalrevolution/2026/08/anthropomorphizing-ai.html",
    "https://marginalrevolution.com/marginalrevolution/2026/09/more-optimistic-results-on-ai-and-job-markets.html",
    "https://mfo-my.sharepoint.com/:t:/r/personal/goldberger_mfo_org/Documents/03",
    "https://newyorker.com/magazine/2026/06/15/radical-duke-danielle-allen-book-review",
    "https://newyorker.com/magazine/2026/09/28/on-the-mark-louis-menand-book-review",
    "https://newyorker.com/news/the-lede/what-chinas-vibe-coding-capital-can-tell-us-about-the-ai-boom",
    "https://nytimes.com/2024/05/16/magazine/israel-west-bank-settler-violence-impunity.html",
    "https://openhouse-magazine.com",
    "https://palladiummag.com/2026/09/18/dont-count-out-the-country-house",
    "https://pbs.org/wnet/gperf/now-hear-this-rachmaninoff-reborn-about/16617",
    "https://thespacereview.com/article/5231/1",
    "https://timesofisrael.com/golan-druze-increasingly-embrace-israel-reject-syria-in-seismic-shift-triggered-by-tragedy",
    "https://wandervogel.art/p/radiocast-no-5-the-god-who-comes",
    "https://wwfm.org/show/the-piano-matters-with-david-dubal/2026-06-24/the-piano-matters-june-17",
    "https://x.com/hamptonism/status/2072316268326052157",
    "https://x.com/i/status/2043852793320980810",
    "https://ynet.co.il/news/article/hjqb2uahzl",
    "https://youtube.com/watch?v=SNnCtAR_8Q8",
    "https://youtube.com/watch?v=b_W0z6hZlrI",
    "https://youtube.com/watch?v=vqphgWu1Is8",
    "https://zinebriboua.com/p/the-islamic-republics-illusion-of",
]


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


def outbound_link(href: str, inner: str, *, klass: str = "", title: str = "") -> str:
    """Anchor that opens off-site. Every generated <a> goes through here."""
    parts = ["<a"]
    if klass:
        parts.append(f'class="{esc(klass)}"')
    parts.append(f'href="{esc(href)}"')
    parts.append('target="_blank"')
    parts.append('rel="noopener noreferrer"')
    if title:
        parts.append(f'title="{esc(title)}"')
    return " ".join(parts) + f">{inner}</a>"


def is_off_leash(item: dict) -> bool:
    title = item.get("title") or ""
    source = item.get("source") or ""
    return title.startswith("Off Leash") or "Off Leash" in source


def is_utility(item: dict) -> bool:
    url = item.get("url") or ""
    return "wttr.in" in url or "finance.yahoo.com" in url or "google.com/finance" in url


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
    summary = item.get("summary")
    summary_html = ""
    if isinstance(summary, str) and summary.strip():
        summary_html = f'\n      <p class="summary">{esc(summary.strip())}</p>'
    title_link = outbound_link(url, esc(title))
    source_link = outbound_link(url, esc(url), klass="url")
    return f'''    <article class="{klass}" data-item-url="{esc(url)}">
      <h2 class="headline">{title_link}</h2>
      <p class="meta"><time class="rel-time" datetime="{esc(published)}">{esc(published)}</time> · <span class="source">{esc(source)}</span> · {source_link}</p>{summary_html}{body_html}
    </article>'''


def render_page(feed: dict) -> str:
    generated = parse_generated_at(str(feed["generated_at"]))
    edition = edition_line(generated)
    stamp = footer_stamp(generated)
    articles = "\n".join(render_item(item) for item in feed["items"])
    edit = outbound_link(EDIT_URL, esc(EDIT_LABEL))
    saved_json = json.dumps(INITIAL_SAVED, ensure_ascii=False)
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
    .item.saved {{ opacity: 0.52; }}
    .item.saved .headline a {{ font-weight: 500; color: var(--muted); }}
    .headline {{ font-size: 1.12rem; font-weight: 700; line-height: 1.35; margin-bottom: 0.35rem; }}
    .headline a {{ color: var(--headline); text-decoration: none; }}
    .headline a:hover {{ color: var(--link); text-decoration: underline; }}
    .meta, .url {{ color: var(--muted); font-size: 0.82rem; }}
    .url {{ word-break: break-all; text-decoration: none; }}
    .url:hover {{ color: var(--link); text-decoration: underline; }}
    .save {{ color: var(--link); text-decoration: none; white-space: nowrap; }}
    .save:hover {{ text-decoration: underline; }}
    .saved-badge {{ color: var(--muted); font-style: italic; white-space: nowrap; }}
    .summary {{
      color: #4b5563;
      font-weight: 400;
      line-height: 1.5;
      margin-top: 0.65rem;
    }}
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

      var initialSaved = {saved_json};
      function normUrl(href) {{
        try {{
          var u = new URL(href);
          if (u.hostname.indexOf("www.") === 0) u.hostname = u.hostname.slice(4);
          if (u.hostname === "youtu.be") {{
            return "https://youtube.com/watch?v=" + u.pathname.replace(/^\\//, "");
          }}
          if (u.hostname.indexOf("youtube.com") >= 0 && u.searchParams.get("v")) {{
            return "https://youtube.com/watch?v=" + u.searchParams.get("v");
          }}
          var out = u.origin + u.pathname.replace(/\\/$/, "");
          if (u.search) out += u.search;
          return out.toLowerCase();
        }} catch (e) {{
          return (href || "").toLowerCase().replace(/\\/$/, "");
        }}
      }}
      function applySaved(urls) {{
        var set = {{}};
        (urls || []).forEach(function (u) {{ set[normUrl(u)] = true; }});
        document.querySelectorAll("article.item[data-item-url]").forEach(function (el) {{
          var href = el.getAttribute("data-item-url");
          if (!set[normUrl(href)]) return;
          el.classList.add("saved");
          var save = el.querySelector("a.save");
          if (save) {{
            var badge = document.createElement("span");
            badge.className = "saved-badge";
            badge.textContent = "✓ Saved";
            save.replaceWith(badge);
          }}
        }});
      }}
      applySaved(initialSaved);

      var params = new URLSearchParams(window.location.search);
      var token = params.get("t") || localStorage.getItem("tomfeed_api_token");
      if (params.get("t")) localStorage.setItem("tomfeed_api_token", params.get("t"));
      if (token) {{
        fetch("/api/tomfeed/saved", {{ headers: {{ "Authorization": "Bearer " + token }} }})
          .then(function (r) {{ return r.ok ? r.json() : null; }})
          .then(function (data) {{ if (data && data.urls) applySaved(data.urls); }})
          .catch(function () {{}});
      }}
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
    if ".summary {" not in page:
        raise SystemExit("missing summary style")
    if 'class="save"' in page or "📌 Save" in page:
        raise SystemExit("save button must stay off")
    anchors = re.findall(r"<a\b[^>]*>", page)
    if not anchors or any(
        'target="_blank"' not in tag or 'rel="noopener noreferrer"' not in tag
        for tag in anchors
    ):
        raise SystemExit("outbound link missing target=_blank")
    OUT_PATH.write_text(page)
    print(edition_line(parse_generated_at(str(feed["generated_at"]))))
    print(f"wrote {OUT_PATH.name} ({len(feed['items'])} items)")


if __name__ == "__main__":
    main()
