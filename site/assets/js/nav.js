/* Builds the navigation from assets/data/site-nav.js, which tools/build.py
   writes from pages.json. Every link is prefixed with the page's own data-base,
   so the same file works at any folder depth and at any wiki address.
   Pages stay readable without JavaScript: the footer carries a static site map. */
(function () {
  "use strict";

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function pageLink(p, base, current) {
    const here = p.slug === current ? ' aria-current="page"' : "";
    const badge = p.badge ? '<span class="sitenav__badge">' + esc(p.badge) + "</span>" : "";
    const caption = p.caption ? '<span class="sitenav__caption">' + esc(p.caption) + "</span>" : "";
    return '<a class="sitenav__link" href="' + base + p.slug + '/"' + here + '>' +
           '<span class="sitenav__title">' + esc(p.title) + badge + "</span>" + caption + "</a>";
  }

  function build(root) {
    const base = root.dataset.base || "";
    const tabNow = root.dataset.tab || "";
    const pageNow = root.dataset.page || "";
    const nav = window.NAV || [];
    const site = window.SITE || {};

    root.className = "sitenav";
    root.innerHTML =
      '<div class="sitenav__bar"><div class="sitenav__inner">' +
        '<a class="sitenav__brand" href="' + (base || "./") + '"><span class="sitenav__mark" aria-hidden="true">' +
          esc(String(site.year || "").slice(-2)) + '</span><span class="sitenav__word">' + esc(site.brand || "") + "</span></a>" +
        '<nav class="sitenav__tabs" aria-label="Main">' +
          nav.map((t) => '<button class="sitenav__tab' + (t.id === tabNow ? " is-section" : "") +
            '" type="button" data-tab="' + esc(t.id) + '" aria-expanded="false" aria-haspopup="true">' + esc(t.name) + "</button>").join("") +
        "</nav>" +
        '<button class="sitenav__burger" type="button" aria-expanded="false" aria-label="Open menu">&#9776;</button>' +
      "</div></div>" +
      nav.map((t) => '<div class="sitenav__panel" data-tab="' + esc(t.id) + '">' +
        t.pages.map((p) => pageLink(p, base, pageNow)).join("") + "</div>").join("") +
      '<nav class="sitenav__drawer" aria-label="Main, small screens">' +
        nav.map((t) => '<p class="sitenav__group">' + esc(t.name) + "</p>" +
          t.pages.map((p) => pageLink(p, base, pageNow)).join("")).join("") +
      "</nav>";

    const btns = [...root.querySelectorAll(".sitenav__tab")];
    const panels = [...root.querySelectorAll(".sitenav__panel")];
    const burger = root.querySelector(".sitenav__burger");
    let openId = null, closeTimer = null, shownAt = 0;

    const show = (id) => {
      clearTimeout(closeTimer);
      if (id !== openId) shownAt = performance.now();
      openId = id;
      btns.forEach((b) => {
        const on = b.dataset.tab === id;
        b.classList.toggle("is-open", on);
        b.setAttribute("aria-expanded", String(on));
      });
      panels.forEach((p) => p.classList.toggle("is-open", p.dataset.tab === id));
    };
    const hideSoon = () => { clearTimeout(closeTimer); closeTimer = setTimeout(() => show(null), 160); };
    const setDrawer = (open) => {
      root.classList.toggle("drawer-open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };
    const entries = (id) => {
      const p = panels.find((x) => x.dataset.tab === id);
      return p ? [...p.querySelectorAll("a[href]")] : [];
    };

    btns.forEach((b, i) => {
      b.addEventListener("mouseenter", () => show(b.dataset.tab));
      b.addEventListener("click", () => {
        (openId === b.dataset.tab && performance.now() - shownAt > 400) ? show(null) : show(b.dataset.tab);
      });
      b.addEventListener("keydown", (e) => {
        if (e.key === "ArrowDown") {
          e.preventDefault(); show(b.dataset.tab);
          const first = entries(b.dataset.tab)[0];
          if (first) first.focus();
        } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          const next = btns[(i + (e.key === "ArrowRight" ? 1 : btns.length - 1)) % btns.length];
          if (openId) show(next.dataset.tab);
          next.focus();
        } else if (e.key === "Tab" && !e.shiftKey && openId === b.dataset.tab) {
          const first = entries(b.dataset.tab)[0];
          if (first) { e.preventDefault(); first.focus(); }
        }
      });
    });
    panels.forEach((p) => {
      p.addEventListener("mouseenter", () => clearTimeout(closeTimer));
      p.addEventListener("mouseleave", hideSoon);
    });
    root.querySelector(".sitenav__tabs").addEventListener("mouseleave", hideSoon);
    root.addEventListener("focusout", (e) => {
      if (e.relatedTarget && !root.contains(e.relatedTarget)) show(null);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      const back = btns.find((b) => b.dataset.tab === openId);
      show(null); setDrawer(false);
      if (back) back.focus();
    });
    document.addEventListener("click", (e) => {
      if (root.contains(e.target)) return;
      show(null); setDrawer(false);
    });
    burger.addEventListener("click", () => setDrawer(!root.classList.contains("drawer-open")));
  }

  function skipLink() {
    const main = document.querySelector("main");
    if (!main) return;
    if (!main.id) main.id = "main";
    if (!main.hasAttribute("tabindex")) main.setAttribute("tabindex", "-1");
    const a = document.createElement("a");
    a.className = "sitenav-skip";
    a.href = "#" + main.id;
    a.textContent = "Skip to content";
    document.body.prepend(a);
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (window.SITE && window.SITE.draftMarks) document.body.classList.add("is-draft");
    const root = document.getElementById("site-nav");
    if (root) build(root);
    skipLink();
  });
})();
