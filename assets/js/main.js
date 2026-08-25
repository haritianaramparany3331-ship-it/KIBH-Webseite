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
