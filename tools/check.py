#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki checker. Reads pages.json and site/. Changes nothing. Standard library only.

    python3 tools/check.py            errors stop the run (exit 1); to-dos are listed
    python3 tools/check.py --freeze   to-dos count as errors too; use before the freeze
    python3 tools/check.py --page W003       show every finding for one page
    python3 tools/check.py --quiet           summary table only

ERRORS: things that cost a medal or award, or break the build.
  manifest   pages.json broken: bad W-ID, duplicate, bad URL, standard page removed
  missing    a page in pages.json has no file
  metadata   page metadata comment missing or disagreeing with pages.json
  footer     licence line or gitlab.igem.org repository link missing
  figure     a <figure> with no F ID (data-fig), no caption, or a bad or duplicate ID;
             an <img> outside any <figure>, unless marked data-decorative
  fact       a .fact with no V ID, or a badly formed one
  external   a script, stylesheet, image, font, iframe or media file loading from
             outside iGEM (plain links to other sites are allowed)
  brokenlink an internal link or asset that does not exist
  binary     an image, font, audio or video file inside the repository
  theme      a colour literal outside assets/css/tokens.css
  size       site/ over the 10 MiB artifact limit
  nav        assets/data/site-nav.js is out of date; run tools/build.py

TO-DOS: unfinished work, allowed until the freeze.
  guide, text, figure, fact, id, owner, setting, ai
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MANIFEST = os.path.join(ROOT, "pages.json")
ARTIFACT_LIMIT = 10 * 1024 * 1024

# iGEM rules as of 2026 (2027 not published on 2026-11-05). Slugs judges reach by fixed URL.
STANDARD = {
    "contribution": "Bronze #3", "engineering": "Silver #1", "human-practices": "Silver #2, Best IHP",
    "education": "Best Education", "entrepreneurship": "Best Entrepreneurship", "hardware": "Best Hardware",
    "inclusivity": "Inclusivity Award", "measurement": "Best Measurement", "model": "Best Model",
    "alternative-platform": "Best Alternative Platform", "safety-and-security": "Safety and Security Award",
    "software": "Best Software", "sustainability": "Best Sustainable Development Impact",
}
# Pages iGEM's official 2026 wiki template ships by default, besides the above.
TEMPLATE_DEFAULT = {"", "description", "experiments", "notebook", "results", "team"}

ALLOWED_HOST = re.compile(r"(^|\.)igem\.(wiki|org)$", re.I)
BINARY = re.compile(r"\.(png|jpe?g|gif|webp|heic|tiff?|bmp|ico|mp4|mov|webm|mp3|wav|woff2?|ttf|otf|eot)$", re.I)
COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgb|rgba|hsl|hsla)\(")
PLACEHOLDER_IDS = re.compile(r"\b(?:R____|C____|D____|I____|K____|S___@v_|BBa_____)")
SETTINGS = re.compile(r"PROJECT_NAME|TEAM_ID")
BRACKET = re.compile(r"\[[^\[\]]*[一-鿿][^\[\]]*\]")
DATE_PH = re.compile(r"YYYY-MM(-DD)?")


class Page(HTMLParser):
    """Collects the elements the checks need."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.figures, self.imgs, self.facts = [], [], [], []
        self.resources, self.links, self.counts = [], [], Counter()
        self.ids, self.text = set(), []
        self.current_fig = None
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        line = self.getpos()[0]
        if a.get("id"):
            self.ids.add(a["id"])
        if tag not in self.VOID:
            self.stack.append(tag)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "figure":
            self.current_fig = {"line": line, "id": a.get("data-fig"), "page": a.get("data-page"), "caption": False,
                                "pending": "fig--pending" in cls}
            self.figures.append(self.current_fig)
        if tag == "figcaption" and self.current_fig is not None:
            self.current_fig["caption"] = True
        if tag == "img":
            self.imgs.append({"line": line, "src": a.get("src"), "alt": a.get("alt"),
                              "in_fig": self.current_fig is not None, "decorative": "data-decorative" in a})
        if "fact" in cls:
            self.facts.append({"line": line, "id": a.get("data-v"), "pending": "fact--pending" in cls})
        if "data-ph" in a:
            self.counts["data_ph"] += 1
        if "guide" in cls:
            self.counts["guide"] += 1
        if "ai" in cls:
            self.counts["ai"] += 1
        if tag == "script" and a.get("src"):
            self.resources.append((line, a["src"]))
        if tag == "link" and a.get("href") and (a.get("rel") or "").lower() in ("stylesheet", "icon", "preload"):
            self.resources.append((line, a["href"]))
        if tag in ("img", "iframe", "video", "audio", "source", "embed") and a.get("src"):
            self.resources.append((line, a["src"]))
        if tag == "object" and a.get("data"):
            self.resources.append((line, a["data"]))
        if tag == "a" and a.get("href"):
            self.links.append((line, a["href"]))

    def handle_endtag(self, tag):
        if tag == "figure":
            self.current_fig = None
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if self.stack and tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


class Report:
    def __init__(self):
        self.errors, self.todos = [], []
        self.per_page = defaultdict(Counter)

    def error(self, where, kind, msg):
        self.errors.append((where, kind, msg))

    def todo(self, where, kind, n=1, msg=""):
        self.todos.append((where, kind, n, msg))
        self.per_page[where][kind] += n


def is_external(url):
    parts = urlsplit(url)
    if url.startswith("//"):
        return not ALLOWED_HOST.search(parts.hostname or "")
    if parts.scheme in ("http", "https"):
        return not ALLOWED_HOST.search(parts.hostname or "")
    return False


def local_target(page_file, url):
    """Return the site-relative path a local URL resolves to, or None for non-local."""
    parts = urlsplit(url)
    if parts.scheme or url.startswith("//") or not parts.path:
        return None
    if parts.path.startswith("/"):
        return parts.path.lstrip("/")
    return os.path.normpath(os.path.join(os.path.dirname(page_file), parts.path))


def target_exists(rel):
    full = os.path.join(SITE, rel)
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))


def check_manifest(data, rep):
    pages = data.get("pages", [])
    seen_w, seen_slug = Counter(p.get("w_id") for p in pages), Counter(p.get("slug") for p in pages)
    tabs = {t["id"] for t in data.get("tabs", [])}
    for p in pages:
        w = p.get("w_id", "?")
        if not re.fullmatch(r"W\d{3}", w or ""):
            rep.error("pages.json", "manifest", "bad W-ID %r" % w)
        if seen_w[w] > 1:
            rep.error("pages.json", "manifest", "duplicate W-ID " + w)
        if seen_slug[p.get("slug")] > 1:
            rep.error("pages.json", "manifest", "duplicate slug %r" % p.get("slug"))
        if p.get("url_path") != "/" + p.get("slug", ""):
            rep.error("pages.json", "manifest", "%s url_path does not match slug" % w)
        if p.get("slug") and p.get("tab") not in tabs:
            rep.error("pages.json", "manifest", "%s unknown tab %r" % (w, p.get("tab")))
        if p.get("class") not in data.get("classes", {}):
            rep.error("pages.json", "manifest", "%s unknown class %r" % (w, p.get("class")))
        if p.get("creates_drive_folder"):
            if not (p.get("drive_folder") or "").startswith(w + " "):
                rep.error("pages.json", "manifest", "%s drive_folder must start with its W-ID" % w)
            if not re.fullmatch(w + r"_[A-Za-z0-9]+_Master", p.get("master_doc") or ""):
                rep.error("pages.json", "manifest", "%s master_doc must be %s_<Page>_Master" % (w, w))
    slugs = {p.get("slug") for p in pages}
    for slug, why in STANDARD.items():
        if slug not in slugs:
            rep.error("pages.json", "manifest", "standard page /%s removed (%s goes unjudged)" % (slug, why))
    for slug in TEMPLATE_DEFAULT:
        if slug not in slugs:
            rep.error("pages.json", "manifest", "official template page /%s removed" % slug)


def meta_value(src, key):
    m = re.search(r"^\s*" + re.escape(key) + r":\s*(.+?)\s*$", src, flags=re.M)
    return m.group(1) if m else None


def check_page(data, page, rep):
    where, site = page["w_id"], data["site"]
    path = os.path.join(SITE, page["file"])
    if not os.path.isfile(path):
        rep.error(where, "missing", "%s has no file at site/%s" % (page["url_path"], page["file"]))
        return
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    parsed = Page()
    parsed.feed(src)
    visible = "\n".join(parsed.text)

    # metadata
    for key, want in (("W-ID", page["w_id"]), ("URL", page["url_path"])):
        got = meta_value(src, key)
        if got != want:
            rep.error(where, "metadata", "%s is %r, pages.json says %r" % (key, got, want))
    for key in ("Content owner", "Coding owner", "Cross-checker"):
        got = meta_value(src, key)
        if got is None:
            rep.error(where, "metadata", "no %s line" % key)
        elif not re.fullmatch(r"P\d{3}", got):
            rep.todo(where, "owner", 1, key)
    if ('data-w="%s"' % page["w_id"]) not in src:
        rep.error(where, "metadata", 'body data-w does not match')

    # footer: required by iGEM on every page
    if "creativecommons.org/licenses/by/4.0" not in src or "Creative Commons Attribution 4.0" not in src:
        rep.error(where, "footer", "licence line missing")
    if site["gitlab_url"] not in src:
        rep.error(where, "footer", "link to %s missing" % site["gitlab_url"])

    # figures
    seen = set()
    for f in parsed.figures:
        fid = f["id"]
        if not fid:
            rep.error(where, "figure", "line %d: <figure> without an F ID (data-fig)" % f["line"])
        elif fid == "F____":
            rep.todo(where, "figure", 1, "line %d" % f["line"])
        elif not re.fullmatch(r"F\d{4}", fid):
            rep.error(where, "figure", "line %d: bad F ID %r" % (f["line"], fid))
        else:
            if fid in seen:
                rep.error(where, "figure", "line %d: %s used twice on this page" % (f["line"], fid))
            seen.add(fid)
            if f["pending"]:
                rep.error(where, "figure", "line %d: %s still has class fig--pending" % (f["line"], fid))
        if not f["caption"]:
            rep.error(where, "figure", "line %d: figure has no caption" % f["line"])
        if f["page"] and f["page"] != page["w_id"]:
            rep.error(where, "figure", "line %d: data-page %s is not this page" % (f["line"], f["page"]))
    for img in parsed.imgs:
        if not img["in_fig"] and not img["decorative"]:
            rep.error(where, "figure", "line %d: <img> outside a figure: give it an F ID or mark data-decorative" % img["line"])
        if img["alt"] is None:
            rep.error(where, "figure", "line %d: <img> has no alt" % img["line"])

    # facts
    for f in parsed.facts:
        if not f["id"]:
            rep.error(where, "fact", "line %d: .fact without a V ID (data-v)" % f["line"])
        elif f["id"] == "V____":
            rep.todo(where, "fact", 1, "line %d" % f["line"])
        elif not re.fullmatch(r"V\d{4}", f["id"]):
            rep.error(where, "fact", "line %d: bad V ID %r" % (f["line"], f["id"]))

    # text placeholders
    if parsed.counts["guide"]:
        rep.todo(where, "guide", parsed.counts["guide"])
    n = max(parsed.counts["data_ph"], len(BRACKET.findall(re.sub(r"\[V____[^\]]*\]", "", visible))))
    if n:
        rep.todo(where, "text", n)
    n = len(PLACEHOLDER_IDS.findall(visible)) + len(DATE_PH.findall(visible)) + visible.count("P___")
    if n:
        rep.todo(where, "id", n)
    n = len(SETTINGS.findall(src))
    if n:
        rep.todo(where, "setting", n, "PROJECT_NAME or TEAM_ID; set in pages.json and run tools/build.py")
    if parsed.counts["ai"]:
        rep.todo(where, "ai", parsed.counts["ai"], "AI-drafted text still marked: a person must own and rewrite it")

    # resources and links
    for line, url in parsed.resources:
        if is_external(url):
            rep.error(where, "external", "line %d loads %s" % (line, url))
            continue
        rel = local_target(page["file"], url)
        if rel and not target_exists(rel):
            rep.error(where, "brokenlink", "line %d: %s" % (line, url))
    for line, url in parsed.links:
        rel = local_target(page["file"], url)
        if rel and not target_exists(rel):
            rep.error(where, "brokenlink", "line %d: %s" % (line, url))


def check_tree(data, rep):
    total = 0
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "public")]
        for name in files:
            full = os.path.join(folder, name)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith("site" + os.sep):
                total += os.path.getsize(full)
            if BINARY.search(name):
                rep.error("repo", "binary", "%s: images, fonts and media go on static.igem.wiki or video.igem.org" % rel)
    if total > ARTIFACT_LIMIT:
        rep.error("repo", "size", "site/ is %.1f MiB; the artifact limit is 10 MiB" % (total / 1048576.0))

    for folder, _, files in os.walk(os.path.join(SITE, "assets")):
        for name in files:
            full = os.path.join(folder, name)
            rel = os.path.relpath(full, ROOT)
            if not name.endswith((".css", ".js")):
                continue
            with open(full, encoding="utf-8") as fh:
                src = fh.read()
            bare = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
            if name.endswith(".css"):
                if name != "tokens.css" and COLOUR.search(bare):
                    rep.error("repo", "theme", "%s has a colour literal: use a token from tokens.css" % rel)
                for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)", bare):
                    if is_external(m.group(1)):
                        rep.error("repo", "external", "%s loads %s" % (rel, m.group(1)))
                for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", bare):
                    if is_external(m.group(1)):
                        rep.error("repo", "external", "%s imports %s" % (rel, m.group(1)))
            else:
                for m in re.finditer(r"""\.src\s*=\s*['"]([^'"]+)""", bare):
                    if is_external(m.group(1)):
                        rep.error("repo", "external", "%s loads %s" % (rel, m.group(1)))

    roster = os.path.join(SITE, "assets", "data", "roster.js")
    if os.path.isfile(roster):
        with open(roster, encoding="utf-8") as fh:
            src = fh.read()
        n = len(re.findall(r'pid:\s*"P___"', src))
        if n:
            team = next((p["w_id"] for p in data["pages"] if p["slug"] == "team"), "repo")
            rep.todo(team, "text", n, "roster.js placeholders")
        for m in re.finditer(r'photo:\s*"(https?://[^"]+)"', src):
            if is_external(m.group(1)):
                rep.error("repo", "external", "roster.js photo %s" % m.group(1))

    nav = os.path.join(SITE, "assets", "data", "site-nav.js")
    if not os.path.isfile(nav):
        rep.error("repo", "nav", "assets/data/site-nav.js is missing; run tools/build.py")
    else:
        with open(nav, encoding="utf-8") as fh:
            src = fh.read()
        for p in data["pages"]:
            if p["slug"] and ('"slug": "%s"' % p["slug"]) not in src:
                rep.error("repo", "nav", "/%s is not in site-nav.js; run tools/build.py" % p["slug"])
    if data["site"].get("draft_marks"):
        rep.todo("site", "setting", 1, "pages.json site.draft_marks is true: set false for the freeze")
    if not os.path.isfile(os.path.join(ROOT, "LICENSE")):
        rep.error("repo", "footer", "LICENSE file missing (iGEM requires CC BY 4.0)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--freeze", action="store_true", help="count to-dos as errors")
    ap.add_argument("--page", help="show findings for one W-ID")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    args = ap.parse_args()

    with open(MANIFEST, encoding="utf-8") as fh:
        data = json.load(fh)
    rep = Report()
    check_manifest(data, rep)
    for page in data["pages"]:
        check_page(data, page, rep)
    check_tree(data, rep)

    kinds = ["guide", "text", "figure", "fact", "id", "owner", "setting", "ai"]
    print("%-6s %-24s %s" % ("W-ID", "URL", " ".join("%6s" % k for k in kinds)))
    for p in data["pages"]:
        c = rep.per_page.get(p["w_id"], Counter())
        if args.page and args.page != p["w_id"]:
            continue
        print("%-6s %-24s %s" % (p["w_id"], p["url_path"], " ".join("%6s" % (c[k] or ".") for k in kinds)))

    for where, kind, msg in rep.errors:
        if not args.quiet and (not args.page or args.page == where):
            print("ERROR  %-10s %-10s %s" % (where, kind, msg))
    if args.page:
        for where, kind, n, msg in rep.todos:
            if where == args.page:
                print("TO-DO  %-10s %-10s %s %s" % (where, kind, n, msg))

    n_todo = sum(n for _, _, n, _ in rep.todos)
    n_pages = sum(1 for p in data["pages"] if os.path.isfile(os.path.join(SITE, p["file"])))
    by_class = Counter(p["class"] for p in data["pages"])
    print("\n%d/%d pages present (%s)." % (n_pages, len(data["pages"]),
          ", ".join("%s %d" % kv for kv in sorted(by_class.items()))))
    print("%d errors, %d unfilled placeholders." % (len(rep.errors), n_todo))
    if rep.errors:
        return 1
    if args.freeze and n_todo:
        print("--freeze: not ready. Unfilled placeholders must be gone before the wiki freeze.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
