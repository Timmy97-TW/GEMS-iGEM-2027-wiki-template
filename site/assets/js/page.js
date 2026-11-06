/* Standard page behaviour. It reads the markup on the page and adds to it, so
   with JavaScript off the prose, figures and references are all still there.

   1. number sections and build the contents rail
   2. number figures (Figure 1, 2 ...) and link .figref cross-references
   3. turn [n] in the prose into a link to reference n, and back
   4. run tab groups
   5. open figures full-window
   6. filter notebook entries                                                  */
(function () {
  "use strict";
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
  const slug = (t) => t.toLowerCase().trim().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-");

  /* ---- 1. outline ------------------------------------------------------- */
  function outline() {
    const body = $(".pagebody"), toc = $(".toc");
    if (!body || !toc) return;
    const heads = $$("h2, h3", body).filter((h) => !h.closest(".refs, .cycle, .ihp-card, .timeline") && !("noToc" in h.dataset));
    if (!heads.length) { toc.remove(); return; }

    const list = document.createElement("ol");
    list.className = "toc__list";
    let major = 0, minor = 0, subs = null;
    heads.forEach((h) => {
      const isSub = h.tagName === "H3";
      if (isSub) minor += 1; else { major += 1; minor = 0; }
      const no = isSub ? (major ? major + "." + minor : "") : major + ".";
      if (!h.id) {
        const base = slug(h.textContent) || "section";
        let id = base, k = 2;
        while (document.getElementById(id)) id = base + "-" + k++;
        h.id = id;
      }
      const words = h.textContent.trim();
      if (no) {
        const tag = document.createElement("span");
        tag.className = "sec__no"; tag.textContent = no; tag.setAttribute("aria-hidden", "true");
        h.prepend(tag);
      }
      const a = document.createElement("a");
      a.href = "#" + h.id;
      const li = document.createElement("li");
      if (isSub && major) {
        a.textContent = words;
        li.append(a);
        if (!subs) {
          subs = document.createElement("ol");
          subs.className = "toc__subs";
          list.lastElementChild.append(subs);
        }
        subs.append(li);
        return;
      }
      li.className = "toc__sec";
      a.innerHTML = '<span class="toc__no">' + (isSub ? "" : major) + "</span>";
      a.append(words);
      li.append(a);
      list.append(li);
      subs = null;
    });
    ($(".toc__inner", toc) || toc).append(list);

    if (window.matchMedia) {
      const narrow = window.matchMedia("(max-width: 1039px)");
      const fold = () => { toc.open = !narrow.matches; };
      fold();
      narrow.addEventListener("change", fold);
    }

    const links = new Map($$("a", list).map((a) => [a.getAttribute("href").slice(1), a]));
    let queued = false;
    const spy = () => {
      queued = false;
      const line = window.innerHeight * 0.4;
      let id = null;
      for (const h of heads) {
        if (!h.getClientRects().length) continue;
        if (h.getBoundingClientRect().top <= line) id = h.id; else break;
      }
      links.forEach((a, k) => a.classList.toggle("is-active", k === id));
      const here = id && links.get(id).closest(".toc__sec");
      $$(".toc__sec", list).forEach((li) => li.classList.toggle("is-here", li === here));
    };
    const queue = () => { if (!queued) { queued = true; requestAnimationFrame(spy); } };
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue, { passive: true });
    spy();
  }

  /* ---- 2. figures ------------------------------------------------------- */
  function figures() {
    const number = new Map();
    $$("figure.fig").forEach((f, i) => {
      const n = i + 1;
      const label = $(".fig__label", f);
      if (label) label.textContent = "Figure " + n + ".";
      if (f.id) number.set(f.id, n);
    });
    $$("a.figref").forEach((a) => {
      const n = number.get((a.getAttribute("href") || "").slice(1));
      if (n) a.textContent = "Figure " + n;
    });
  }

  /* ---- 3. citations ------------------------------------------------------ */
  function citations() {
    const refs = $(".refs ol"), body = $(".pagebody");
    if (!refs || !body) return;
    const items = $$("li", refs);
    items.forEach((li, i) => { if (!li.id) li.id = "ref-" + (i + 1); });
    const first = {};
    const walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => n.parentElement.closest(".refs, a, code, pre, .toc, .guide")
        ? NodeFilter.FILTER_REJECT
        : /\[\d+(\s*,\s*\d+)*\]/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT
    });
    const texts = [];
    while (walker.nextNode()) texts.push(walker.currentNode);
    texts.forEach((node) => {
      const frag = document.createDocumentFragment();
      let last = 0;
      node.nodeValue.replace(/\[(\d+(?:\s*,\s*\d+)*)\]/g, (match, nums, at) => {
        frag.append(node.nodeValue.slice(last, at), "[");
        nums.split(",").map((n) => n.trim()).forEach((n, i, arr) => {
          const idx = parseInt(n, 10);
          if (items[idx - 1]) {
            const a = document.createElement("a");
            a.className = "cite"; a.href = "#ref-" + idx; a.textContent = n;
            if (!first[idx]) a.id = first[idx] = "cite-" + idx;
            frag.append(a);
          } else frag.append(n);
          if (i < arr.length - 1) frag.append(", ");
        });
        frag.append("]");
        last = at + match.length;
        return match;
      });
      frag.append(node.nodeValue.slice(last));
      node.replaceWith(frag);
    });
    items.forEach((li, i) => {
      if (!first[i + 1]) return;
      const a = document.createElement("a");
      a.href = "#" + first[i + 1]; a.textContent = " ↩";
      a.setAttribute("aria-label", "Back to where this was cited");
      li.append(a);
    });
  }

  /* ---- 4. tabs ----------------------------------------------------------- */
  function tabs() {
    $$(".tabs").forEach((group) => {
      const btns = $$(".tabs__btn", group), panels = $$(".tabs__panel", group);
      if (!btns.length) return;
      const show = (id) => {
        btns.forEach((b) => {
          const on = b.dataset.panel === id;
          b.setAttribute("aria-selected", String(on));
          b.tabIndex = on ? 0 : -1;
        });
        panels.forEach((p) => { p.hidden = p.id !== id; });
      };
      btns.forEach((b) => b.addEventListener("click", () => show(b.dataset.panel)));
      const hit = panels.find((p) => "#" + p.id === location.hash);
      show(hit ? hit.id : btns[0].dataset.panel);
    });
  }

  /* ---- 5. lightbox ------------------------------------------------------- */
  function lightbox() {
    const imgs = $$(".fig:not(.fig--pending) img");
    if (!imgs.length) return;
    const box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.setAttribute("aria-label", "Enlarged figure");
    box.innerHTML = '<button class="lightbox__close" aria-label="Close">×</button><figure style="margin:0"><img alt="" /><figcaption></figcaption></figure>';
    document.body.append(box);
    const big = $("img", box), cap = $("figcaption", box);
    let opener = null;
    const close = () => { box.classList.remove("is-open"); document.body.style.overflow = ""; if (opener) opener.focus(); };
    const open = (img) => {
      opener = img; big.src = img.currentSrc || img.src; big.alt = img.alt;
      const c = img.closest("figure").querySelector("figcaption");
      cap.textContent = c ? c.textContent : "";
      box.classList.add("is-open"); document.body.style.overflow = "hidden";
      $(".lightbox__close", box).focus();
    };
    imgs.forEach((img) => {
      img.tabIndex = 0; img.setAttribute("role", "button");
      img.addEventListener("click", () => open(img));
      img.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(img); } });
    });
    box.addEventListener("click", (e) => { if (e.target === box || e.target.closest(".lightbox__close")) close(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && box.classList.contains("is-open")) close(); });
  }

  /* ---- 6. notebook filter ------------------------------------------------- */
  function notebook() {
    $$(".nb").forEach((nb) => {
      const entries = $$(".nb-entry", nb), search = $(".nb-search", nb), month = $(".nb-month", nb);
      if (month) {
        [...new Set(entries.map((e) => (e.dataset.date || "").slice(0, 7)).filter((m) => /^\d{4}-\d{2}$/.test(m)))].sort().forEach((m) => {
          const o = document.createElement("option");
          o.value = m; o.textContent = m;
          month.append(o);
        });
      }
      const apply = () => {
        const q = search ? search.value.trim().toLowerCase() : "", m = month ? month.value : "";
        entries.forEach((e) => {
          const okQ = !q || e.textContent.toLowerCase().includes(q);
          const okM = !m || (e.dataset.date || "").startsWith(m);
          e.hidden = !(okQ && okM);
        });
      };
      if (search) search.addEventListener("input", apply);
      if (month) month.addEventListener("change", apply);
    });
  }

  const start = () => { outline(); figures(); citations(); tabs(); lightbox(); notebook(); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
