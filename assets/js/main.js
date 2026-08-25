/* KIBH — progressive enhancement only. The site renders fully without this. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  var label = toggle.querySelector(".visually-hidden");

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", String(open));
    nav.setAttribute("data-open", String(open));
    if (label) label.textContent = open ? "Menü schließen" : "Menü öffnen";
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  // Close when a link is followed, so the drawer doesn't cover the target.
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  // Reset state if the viewport grows past the drawer breakpoint (1024px).
  var mq = window.matchMedia("(min-width: 1025px)");
  var onChange = function (e) { if (e.matches) setOpen(false); };
  if (mq.addEventListener) mq.addEventListener("change", onChange);
  else if (mq.addListener) mq.addListener(onChange);
})();

/* Tab groups (E-Rechnung solutions). Without JS every panel stays visible,
   which is still readable -- the `hidden` attribute is only applied here. */
(function () {
  "use strict";

  var groups = document.querySelectorAll("[data-tabs]");
  if (!groups.length) return;

  Array.prototype.forEach.call(groups, function (group) {
    var buttons = group.querySelectorAll("[data-tab]");
    var panels = group.querySelectorAll("[data-panel]");

    function select(name, focus) {
      Array.prototype.forEach.call(buttons, function (b) {
        var on = b.getAttribute("data-tab") === name;
        b.setAttribute("aria-selected", String(on));
        b.tabIndex = on ? 0 : -1;
        if (on && focus) b.focus();
      });
      Array.prototype.forEach.call(panels, function (p) {
        p.hidden = p.getAttribute("data-panel") !== name;
      });
    }

    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener("click", function () {
        select(b.getAttribute("data-tab"), false);
      });
    });

    group.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
      var names = Array.prototype.map.call(buttons, function (b) {
        return b.getAttribute("data-tab");
      });
      var i = names.indexOf(document.activeElement.getAttribute("data-tab"));
      if (i < 0) return;
      e.preventDefault();
      select(names[(i + (e.key === "ArrowRight" ? 1 : -1) + names.length) % names.length], true);
    });

    select(group.querySelector('[data-tab][aria-selected="true"]')
      ? group.querySelector('[data-tab][aria-selected="true"]').getAttribute("data-tab")
      : buttons[0].getAttribute("data-tab"), false);
  });

  // "Mehr erfahren" on a solution card opens that card's tab and scrolls to it.
  var jumps = document.querySelectorAll("[data-tab-jump]");
  Array.prototype.forEach.call(jumps, function (j) {
    j.addEventListener("click", function () {
      var name = j.getAttribute("data-tab-jump");
      var btn = document.querySelector('[data-tab="' + name + '"]');
      if (!btn) return;
      btn.click();
      btn.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
})();

/* Scroll-in animations. Mirrors the entrance animations the WordPress original
   plays on the E-Rechnung page: blocks fade up, images slide in from the side
   they sit on. Elements stay put until the observer reveals them, and the
   `js-anim` class on <html> means nothing is hidden when JS is unavailable. */
(function () {
  "use strict";

  var items = document.querySelectorAll("[data-anim]");
  if (!items.length) return;

  if (!("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(items, function (el) { el.classList.add("is-in"); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-in");
      io.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.05 });

  Array.prototype.forEach.call(items, function (el) { io.observe(el); });

  // A panel revealed by a tab switch was never on screen, so its own elements
  // never intersected. Reveal whatever the newly shown panel contains.
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-tab], [data-tab-jump]");
    if (!btn) return;
    window.setTimeout(function () {
      document.querySelectorAll("[data-panel]:not([hidden]) [data-anim]")
        .forEach(function (el) { el.classList.add("is-in"); });
    }, 30);
  });
})();
