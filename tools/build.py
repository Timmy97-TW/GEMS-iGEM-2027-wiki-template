#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keeps the site in step with pages.json. Standard library only.

    python3 tools/build.py                      write nav data, stamp titles and
                                                footers, scaffold any missing page
    python3 tools/build.py new SLUG --title T --tab TAB --caption C
                                                add a topic-specific page
    python3 tools/build.py --list               print the manifest

Page files are never overwritten: a page is scaffolded only if its file does
not exist. Only the <title> line and the block between the FOOTER markers are
rewritten on every run, so the footer is defined once, here, while staying plain
HTML on every page (the licence and repository lines must be on every page, even
with JavaScript off).
"""
import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outlines import OUTLINES, SHARED_ABSTRACT  # noqa: E402

SITE = os.path.join(ROOT, "site")
MANIFEST = os.path.join(ROOT, "pages.json")
FOOT_START = "<!-- FOOTER:START (written by tools/build.py) -->"
FOOT_END = "<!-- FOOTER:END -->"
E = html.escape
NO_REFS = ("", "team", "attributions", "milestone", "notebook", "drylab-notebook")


def load():
    with open(MANIFEST, encoding="utf-8") as fh:
        return json.load(fh)


def save(data):
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def base_of(page):
    return "../" * (page["slug"].count("/") + 1) if page["slug"] else ""


def title_of(page, site):
    head = "%s · %s · iGEM %s" % (site["project_name"], site["team_name"], site["year"])
    return head if not page["slug"] else "%s | %s" % (page["title"], head)


def repo_label(site):
    return re.sub(r"^https://", "", site["gitlab_url"])


# ---- nav data ---------------------------------------------------------------

def write_nav(data):
    site = data["site"]
    nav = []
    for tab in data["tabs"]:
        pages = []
        for p in data["pages"]:
            if p["tab"] != tab["id"]:
                continue
            entry = {"title": p["title"], "slug": p["slug"], "caption": p.get("caption", "")}
            if p.get("prize"):
                entry["badge"] = "★"
            pages.append(entry)
        nav.append({"id": tab["id"], "name": tab["name"], "pages": pages})
    siteobj = {"brand": site["project_name"], "year": site["year"], "draftMarks": bool(site.get("draft_marks"))}
    out = ("/* Written by tools/build.py from pages.json. Do not edit by hand. */\n"
           "window.SITE = %s;\nwindow.NAV = %s;\n"
           % (json.dumps(siteobj, ensure_ascii=False), json.dumps(nav, ensure_ascii=False, indent=1)))
    with open(os.path.join(SITE, "assets", "data", "site-nav.js"), "w", encoding="utf-8") as fh:
        fh.write(out)


# ---- footer -----------------------------------------------------------------

def footer(data, page):
    site, base = data["site"], base_of(page)
    cols = []
    for tab in data["tabs"]:
        links = "".join('<li><a href="%s%s/">%s</a></li>' % (base, p["slug"], E(p["title"]))
                        for p in data["pages"] if p["tab"] == tab["id"])
        cols.append('<div><h2>%s</h2><ul>%s</ul></div>' % (E(tab["name"]), links))
    return """%s
<footer class="footer">
  <div class="footer__inner">
    <nav class="footer__map" aria-label="Site map">%s</nav>
    <div class="footer__legal">
      <p><b>%s</b> &middot; %s &middot; iGEM %s</p>
      <p>&copy; %s &middot; Content on this site is licensed under a <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">Creative Commons Attribution 4.0 International license</a>.</p>
      <p>The repository used to create this website is available at <a href="%s">%s</a>.</p>
    </div>
  </div>
</footer>
%s""" % (FOOT_START, "".join(cols), E(site["project_name"]), E(site["team_name"]), site["year"],
         site["year"], site["gitlab_url"], repo_label(site), FOOT_END)


def stamp(data, page):
    path = os.path.join(SITE, page["file"])
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    new = re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % E(title_of(page, data["site"])),
                 src, count=1, flags=re.S)
    pattern = re.escape(FOOT_START) + r".*?" + re.escape(FOOT_END)
    if re.search(pattern, new, flags=re.S):
        new = re.sub(pattern, lambda m: footer(data, page), new, count=1, flags=re.S)
    else:
        print("WARNING: %s has no footer markers; run tools/check.py" % page["file"])
    if new != src:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)


# ---- placeholders -------------------------------------------------------------

def fig(page, hint):
    w = page["w_id"]
    return ('<figure class="fig fig--pending" data-fig="F____" data-page="%s">\n'
            '  <div class="fig__slot">F____ | %s<br />File name F_____%s_topic_vNN | hosted on static.igem.wiki | '
            'swap in only when "Ready to publish" is TRUE in Hub Figures</div>\n'
            '  <figcaption><span class="fig__label"></span> [Caption: %s. State n, the statistical method and the controls.] '
            '<span class="fig__id">F____</span></figcaption>\n'
            '</figure>\n' % (w, E(hint), w, E(hint)))


def fact(hint):
    return '<span class="fact fact--pending" data-v="V____" title="V number in Hub Facts">[V____ %s]</span>' % E(hint)


PARA = '<p class="ph" data-ph>[Body text, brought in by the content owner from the Master doc.]</p>\n'
ATTR = ('<p class="attr" data-ph><b>Attribution.</b> Designed by P___; carried out by P___; '
        'checked by P___. External help: [Name; needs K____].</p>\n')


def dbtl_step(letter, name, inner):
    return ('<li class="dbtl__step"><h4><span class="dbtl__badge" aria-hidden="true">%s</span>%s</h4>\n%s</li>\n'
            % (letter, name, inner))


def block_dbtl(page, data):
    ph = '<p class="ph" data-ph>[%s]</p>\n'
    steps = (dbtl_step("D", "Design", ph % "This cycle's hypothesis and design, and why we chose it")
             + dbtl_step("B", "Build", ph % "What we actually built, which C or H it maps to, with R____")
             + dbtl_step("T", "Test", ph % "How we tested it, and the result" + fig(page, "Test result for this cycle"))
             + dbtl_step("L", "Learn", ph % "Was the hypothesis confirmed or refuted, and what did that change in the next cycle"))
    return ('<div class="cycle" data-cycle="1">\n<h3>Cycle 1: [The problem this cycle tackles]</h3>\n'
            '<ol class="dbtl">\n%s</ol>\n'
            '<p class="ledger" data-ph>Evidence: R____ · F____ · %s · Decision D____</p>\n</div>\n'
            '<!-- Next cycle: copy the whole .cycle and add one to data-cycle. -->\n' % (steps, fact("Key number for this cycle")))


def block_notebook(page, data):
    entry = ('<details class="nb-entry" data-date="YYYY-MM-DD" data-run="R____">\n'
             '  <summary><time>YYYY-MM-DD</time>[Title of this Run]</summary>\n'
             '  <p class="nb-entry__ids">R____ · S___@v_ · C____</p>\n'
             '  <p class="ph" data-ph>[Plan and Results, brought in from the Run Record; do not retype them.]</p>\n'
             '</details>\n')
    return ('<div class="nb">\n<div class="nb-tools">\n'
            '<input class="nb-search" type="search" placeholder="Search entries" aria-label="Search entries" />\n'
            '<select class="nb-month" aria-label="Month"><option value="">All months</option></select>\n'
            '</div>\n%s</div>\n<!-- New entry: copy one .nb-entry. -->\n' % (entry * 3))


def block_parts(page, data):
    row = ('<tr><td>[Part name]</td><td><a href="https://registry.igem.org/">BBa_____</a></td>'
           '<td>[Basic / Composite / Improved]</td><td>C____</td><td data-ph>[One sentence: what it does]</td></tr>\n')
    return ('<div class="table-scroll"><table>\n<thead><tr><th>Part</th><th>Registry</th><th>Type</th>'
            '<th>Construct ID</th><th>Function</th></tr></thead>\n<tbody>\n%s</tbody>\n</table></div>\n' % (row * 2))


def block_ihp(page, data):
    return ('<article class="ihp-card" data-interaction="I____" data-consent="K____">\n'
            '<h3>[Who: name or organisation only with a K; otherwise their role]</h3>\n<dl>\n'
            '<dt>Why them</dt><dd data-ph>[Why we approached them]</dd>\n'
            '<dt>What we asked</dt><dd data-ph>[What we asked]</dd>\n'
            '<dt>What we learned</dt><dd data-ph>[What we learned; direct quotes need a V and a K]</dd>\n'
            '<dt>What changed</dt><dd data-ph>[What changed in the project as a result, with D____]</dd>\n'
            '<dt>Records</dt><dd>I____ · K____</dd>\n</dl>\n</article>\n'
            '<!-- New card: copy one .ihp-card. -->\n')


def block_team(page, data):
    return ('<div class="team-filter" id="team-filter" role="group" aria-label="Filter by sub-team"></div>\n'
            '<div class="team-grid" id="team-grid"></div>\n'
            '<noscript><p>This list is built with JavaScript. The roster is in assets/data/roster.js.</p></noscript>\n')


def block_attr_link(page, data):
    return ('<p>The full, official record is the Attributions Form on our '
            '<a href="https://teams.igem.org/%s">iGEM team page</a>.</p>\n' % data["site"]["igem_team_id"])


def block_attribution(page, data):
    rows = "".join('<tr><th scope="row">%s</th><td>P___</td><td>P___</td><td>[Name; needs K____]</td></tr>\n' % a
                   for a in ("Project idea", "Design", "Experiments", "Modelling and software", "Hardware",
                             "Human Practices", "Wiki and media"))
    return ('<div class="table-scroll"><table class="attr-table">\n<thead><tr><th>Area</th><th>Students</th>'
            '<th>Advisors and instructors</th><th>External help</th></tr></thead>\n<tbody>\n%s</tbody>\n</table></div>\n'
            % rows)


def block_timeline(page, data):
    item = ('<li><time datetime="YYYY-MM-DD">YYYY-MM-DD</time><h3>[What happened that day]</h3>'
            '<p class="ph" data-ph>[One or two sentences of caption, from Milestones Caption]</p></li>\n')
    return '<ol class="timeline">\n%s</ol>\n%s<!-- New entry: copy one li. -->\n' % (item * 3, fig(page, "A photo that stands for the year"))


def block_doors(page, data):
    wanted = ("description", "engineering", "results", "human-practices", "contribution", "team")
    items = "".join('<li><a href="%s/"><b>%s</b>%s</a></li>\n' % (p["slug"], E(p["title"]), E(p.get("caption", "")))
                    for p in data["pages"] if p["slug"] in wanted)
    return '<ul class="home-doors">\n%s</ul>\n' % items


BLOCKS = {"dbtl": block_dbtl, "notebook": block_notebook, "parts": block_parts, "ihp": block_ihp,
          "team": block_team, "attribution-link": block_attr_link, "attribution": block_attribution,
          "timeline": block_timeline, "doors": block_doors}

GENERIC = {"lede": "[What this page is about.]", "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Approach", "Explain the approach and the reasons for it. This is a supporting page: link to it from the relevant standard pages, because judges will not find it on their own.", {"figs": ["Diagram of the approach"]}),
    ("Results", "Every claim gets one figure and one number.", {"figs": ["Main result"], "facts": ["Main result value"]}),
]}


# ---- page scaffold -------------------------------------------------------------

def section_html(page, data, heading, guide, opt):
    out = ['<section>\n<h2>%s</h2>\n<aside class="guide"><b>What judges look for:</b> %s</aside>\n' % (E(heading), E(guide))]
    block = opt.get("block")
    if block not in ("dbtl", "notebook", "parts", "ihp", "team", "attribution", "timeline", "doors"):
        out.append(PARA)
    for hint in opt.get("facts", []):
        out.append('<p>%s</p>\n' % fact(hint))
    if block:
        out.append(BLOCKS[block](page, data))
    for hint in opt.get("figs", []):
        out.append(fig(page, hint))
    if opt.get("attr"):
        out.append(ATTR)
    out.append("</section>\n")
    return "".join(out)


META = """<!--
  WIKI PAGE METADATA. Keep this block: tools/check.py reads it. Hub Pages is the source for people.
  W-ID: %s
  URL: %s
  Class: %s
  Content owner: P___
  Coding owner: P___
  Cross-checker: P___
  Master doc: %s
  Drive folder: %s/%s
  Figures: %s, named F____W_topic_vNN with this page's W-ID
-->"""

DOC = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>%(title)s</title>
  <meta name="description" content="[One-sentence page summary]" />
  <link rel="icon" href="https://static.igem.wiki/common/icons/favicons/igem-2022.svg" />
  <link rel="license" href="https://creativecommons.org/licenses/by/4.0/" />
  <link rel="stylesheet" href="%(base)sassets/css/tokens.css" />
  <link rel="stylesheet" href="%(base)sassets/css/site.css" />
  <link rel="stylesheet" href="%(base)sassets/css/components.css" />
</head>
<body data-w="%(w)s">
%(meta)s
<div id="site-nav" data-base="%(base)s" data-tab="%(tab)s" data-page="%(slug)s"></div>
<div class="sitenav-spacer"></div>
<header class="pagehead"><div class="pagehead__inner">
<p class="pagehead__kicker">%(kicker)s</p>
<h1>%(h1)s</h1>
<p class="pagehead__lede" data-ph>%(lede)s</p>
%(judged)s</div></header>
<div class="pagegrid">
<details class="toc" open><summary class="toc__title">On this page</summary><div class="toc__inner"></div></details>
<main class="pagebody">
%(sections)s%(refs)s</main>
</div>
%(foot)s
<script src="%(base)sassets/data/site-nav.js"></script>
<script src="%(base)sassets/js/nav.js"></script>
<script src="%(base)sassets/js/page.js"></script>
%(extra)s</body>
</html>
"""

REFS = ('<section class="refs" id="references">\n<h2>References</h2>\n'
        '<aside class="guide"><b>What judges look for:</b> Best Wiki asks whether content is properly cited, including images and past teams\' work. '
        'Writing [1] in the text links to the first entry automatically. Delete this section if there are no references.</aside>\n'
        '<ol>\n<li data-ph>[Author. Title. Journal Year. Link]</li>\n</ol>\n</section>\n')


def scaffold(data, page):
    path = os.path.join(SITE, page["file"])
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    site, base = data["site"], base_of(page)
    outline = OUTLINES.get(page["slug"] or "home", GENERIC)
    tab = next((t["name"] for t in data["tabs"] if t["id"] == page["tab"]), "")
    extra = ""
    if page["slug"] == "team":
        extra = ('<script src="%sassets/data/roster.js"></script>\n<script src="%sassets/js/team.js"></script>\n'
                 % (base, base))
    judged = ""
    if page.get("judged_for"):
        judged = '<p class="pagehead__judged draft-only">Judged for: %s</p>\n' % E("; ".join(page["judged_for"]))
    doc = DOC % {
        "title": E(title_of(page, site)), "base": base, "w": page["w_id"],
        "meta": META % (page["w_id"], page["url_path"], page["class"], page["master_doc"], site["drive_root"],
                        page["drive_folder"], site["figures_folder"]),
        "tab": page["tab"], "slug": page["slug"], "kicker": E(outline.get("kicker", tab)),
        "h1": E(page["title"] if page["slug"] else site["project_name"]),
        "lede": E(outline.get("lede", "[What this page is about.]")), "judged": judged,
        "sections": "".join(section_html(page, data, h, g, o) for h, g, o in outline["sections"]),
        "refs": "" if page["slug"] in NO_REFS else REFS, "foot": footer(data, page), "extra": extra}
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return True


NOT_FOUND = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Page not found | %(team)s</title>
  <link rel="icon" href="https://static.igem.wiki/common/icons/favicons/igem-2022.svg" />
  <script>
    /* iGEM serves this file from any address, so relative links would break.
       Works at the iGEM address and in a local preview at the server root. */
    var WIKI_BASE = location.pathname.indexOf("%(prefix)s") === 0 ? "%(prefix)s" : "/";
    ["tokens", "site"].forEach(function (n) {
      var l = document.createElement("link");
      l.rel = "stylesheet";
      l.href = WIKI_BASE + "assets/css/" + n + ".css";
      document.head.appendChild(l);
    });
  </script>
</head>
<body>
<main class="notfound">
  <h1>This page does not exist</h1>
  <p><a id="home" href="/">Back to the homepage</a></p>
</main>
<script>document.getElementById("home").href = WIKI_BASE;</script>
<footer class="footer"><div class="footer__inner"><div class="footer__legal">
  <p>&copy; %(year)s &middot; Content on this site is licensed under a <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">Creative Commons Attribution 4.0 International license</a>.</p>
  <p>The repository used to create this website is available at <a href="%(repo)s">%(label)s</a>.</p>
</div></div></footer>
</body>
</html>
"""


def write_404(data):
    site = data["site"]
    doc = NOT_FOUND % {"team": E(site["team_name"]), "prefix": "/" + site["team_slug"] + "/", "year": site["year"],
                       "repo": site["gitlab_url"], "label": repo_label(site)}
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)


def sync(data):
    write_nav(data)
    made = [p["file"] for p in data["pages"] if scaffold(data, p)]
    for p in data["pages"]:
        stamp(data, p)
    write_404(data)
    print("nav written; %d pages; %d new: %s" % (len(data["pages"]), len(made), ", ".join(made) or "-"))


def cmd_new(args):
    data = load()
    slug = args.slug.strip("/")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*", slug):
        sys.exit("slug must be lower-case words joined by hyphens: " + slug)
    if any(p["slug"] == slug for p in data["pages"]):
        sys.exit("slug already exists: " + slug)
    if args.tab not in [t["id"] for t in data["tabs"]]:
        sys.exit("tab must be one of: " + ", ".join(t["id"] for t in data["tabs"]))
    w = "W%03d" % (1 + max(int(p["w_id"][1:]) for p in data["pages"]))
    doc = re.sub(r"[^A-Za-z0-9]", "", args.title.title())
    data["pages"].append({
        "w_id": w, "slug": slug, "url_path": "/" + slug, "file": slug + "/index.html", "title": args.title,
        "tab": args.tab, "caption": args.caption, "class": "topic-specific", "igem_basis": "project",
        "judged_for": [], "drive_folder": "%s %s" % (w, args.title), "master_doc": "%s_%s_Master" % (w, doc),
        "creates_drive_folder": True, "prize": False})
    save(data)
    sync(data)
    print("added %s at /%s. Now add a Hub Pages row and the Drive folder '%s %s' under %s."
          % (w, slug, w, args.title, data["site"]["drive_root"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="print the manifest")
    sub = ap.add_subparsers(dest="cmd")
    n = sub.add_parser("new", help="add a topic-specific page")
    n.add_argument("slug")
    n.add_argument("--title", required=True)
    n.add_argument("--tab", required=True)
    n.add_argument("--caption", default="")
    args = ap.parse_args()
    if args.cmd == "new":
        cmd_new(args)
        return
    data = load()
    if args.list:
        for p in data["pages"]:
            print("%s  %-24s %-14s %s" % (p["w_id"], p["url_path"], p["class"], p["drive_folder"]))
        return
    sync(data)


if __name__ == "__main__":
    main()
