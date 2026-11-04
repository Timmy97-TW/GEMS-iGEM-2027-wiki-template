/* Builds the member cards from assets/data/roster.js into #team-grid.
   No photo set: shows an initials tile. Filters come from the track field. */
(function () {
  "use strict";
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function card(m) {
    const initials = m.name && !m.name.startsWith("[") ? m.name.trim().split(/\s+/).map((w) => w[0]).slice(0, 2).join("") : m.pid;
    const picture = m.photo
      ? '<img class="member__photo" src="' + esc(m.photo) + '" alt="Portrait of ' + esc(m.name) + '" loading="lazy" />'
      : '<div class="member__tile" aria-hidden="true">' + esc(initials) + "</div>";
    return '<article class="member" data-track="' + esc(m.track) + '">' + picture +
      '<div class="member__body"><h3 class="member__name">' + esc(m.name) + "</h3>" +
      '<p class="member__meta">' + esc([m.role, m.track].filter(Boolean).join(" · ")) + "</p>" +
      '<p class="member__bio">' + esc(m.bio) + "</p>" +
      '<ul class="member__tasks">' + (m.tasks || []).map((t) => "<li>" + esc(t) + "</li>").join("") + "</ul></div></article>";
  }

  document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("team-grid");
    const filter = document.getElementById("team-filter");
    const roster = window.ROSTER || [];
    if (!grid) return;
    grid.innerHTML = roster.map(card).join("");
    if (!filter) return;
    const tracks = [...new Set(roster.map((m) => m.track).filter(Boolean))];
    filter.innerHTML = ["All"].concat(tracks).map((t, i) =>
      '<button type="button" data-track="' + esc(t) + '" aria-pressed="' + (i === 0) + '">' + esc(t) + "</button>").join("");
    filter.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      [...filter.children].forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      [...grid.children].forEach((c) => { c.hidden = b.dataset.track !== "All" && c.dataset.track !== b.dataset.track; });
    });
  });
})();
