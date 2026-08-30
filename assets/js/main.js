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

  // Reset state if the viewport grows past the drawer breakpoint (1119px).
  var mq = window.matchMedia("(min-width: 1120px)");
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

/* --------------------------------------------------------------------------
   Disclosure: "Mehr" over the last three homepage solution cards.

   The live page hides them behind the same toggle. CSS does the hiding and
   only under .js-anim, so with JS off every card is visible and the button
   is not rendered at all.
   -------------------------------------------------------------------------- */
(function () {
  var btns = document.querySelectorAll("[data-disclosure]");
  if (!btns.length) return;

  Array.prototype.forEach.call(btns, function (btn) {
    var target = document.getElementById(btn.getAttribute("data-disclosure"));
    if (!target) return;

    btn.addEventListener("click", function () {
      var open = target.classList.toggle("is-expanded");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = btn.getAttribute(open ? "data-label-less" : "data-label-more");

      // The cards were display:none, so they never intersected the observer
      // and are still sitting at their animation start state.
      if (open) {
        target.querySelectorAll("[data-more] [data-anim], [data-more][data-anim]")
          .forEach(function (el) { el.classList.add("is-in"); });
      }
    });
  });
})();

/* --------------------------------------------------------------------------
   Rotating word in the three-step headline, as on the live page.
   -------------------------------------------------------------------------- */
(function () {
  var els = document.querySelectorAll("[data-rotate]");
  if (!els.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduced.matches) return;

  Array.prototype.forEach.call(els, function (el) {
    var words = el.getAttribute("data-rotate").split("|");
    var slot = el.querySelector(".rotator__word");
    if (!slot || words.length < 2) return;

    // Reserve the width of the longest word so the headline does not reflow
    // on every tick.
    var probe = document.createElement("span");
    probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap";
    probe.className = slot.className;
    el.appendChild(probe);
    var widest = 0;
    words.forEach(function (w) {
      probe.textContent = w;
      widest = Math.max(widest, probe.getBoundingClientRect().width);
    });
    el.removeChild(probe);
    el.style.minWidth = Math.ceil(widest) + "px";

    var i = 0;
    window.setInterval(function () {
      i = (i + 1) % words.length;
      var next = slot.cloneNode(false);
      next.textContent = words[i];
      slot.parentNode.replaceChild(next, slot);
      slot = next;
    }, 1500);
  });
})();

/* Typed headline on the Kontakt page.
   --------------------------------------------------------------------------
   The original runs Elementor's animated headline in `typing` mode over three
   phrases, holding each one for its configured `rotate_iteration_delay` of
   2500ms. Letters are typed and deleted one at a time; the caret is CSS. */
(function () {
  "use strict";

  var HOLD = 2500;      // the original's own rotate_iteration_delay
  var TYPE = 110;       // ms per letter typed
  var ERASE = 55;       // ms per letter deleted
  var GAP = 400;        // pause on an empty line before the next phrase

  var els = document.querySelectorAll("[data-type]");
  if (!els.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  Array.prototype.forEach.call(els, function (el) {
    var phrases = el.getAttribute("data-type").split("|").filter(Boolean);
    var slot = el.querySelector(".typeline__text");
    if (!slot || phrases.length < 2) return;

    // Hold the width of the longest phrase so the centred headline does not
    // shuffle sideways on every keystroke. Re-measured on resize, because the
    // headline is fluid and a stale reservation would overflow a narrower
    // viewport.
    function reserve() {
      var probe = document.createElement("span");
      probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap";
      probe.className = slot.className;
      el.style.minWidth = "0";
      el.appendChild(probe);
      var widest = 0;
      phrases.forEach(function (t) {
        probe.textContent = t;
        widest = Math.max(widest, probe.getBoundingClientRect().width);
      });
      el.removeChild(probe);
      // The caret sits inside the wrapper too, so its own width is part of
      // what has to be reserved.
      el.style.minWidth = Math.ceil(widest + 3) + "px";
    }
    reserve();

    var pending;
    window.addEventListener("resize", function () {
      window.clearTimeout(pending);
      pending = window.setTimeout(reserve, 150);
    });

    var i = 0;
    var n = phrases[0].length;
    var typing = false;

    function tick() {
      var text = phrases[i];
      if (typing) {
        n += 1;
        slot.textContent = text.slice(0, n);
        if (n >= text.length) {
          typing = false;
          window.setTimeout(tick, HOLD);
          return;
        }
        window.setTimeout(tick, TYPE);
      } else {
        n -= 1;
        slot.textContent = text.slice(0, Math.max(n, 0));
        if (n <= 0) {
          i = (i + 1) % phrases.length;
          typing = true;
          n = 0;
          window.setTimeout(tick, GAP);
          return;
        }
        window.setTimeout(tick, ERASE);
      }
    }

    window.setTimeout(tick, HOLD);
  });
})();

/* Forms with no backend yet. Without this a submit posts the page to itself
   and looks like a successful send. */
(function () {
  "use strict";

  var forms = document.querySelectorAll("form[data-inert]");
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener("submit", function (e) { e.preventDefault(); });
  });
})();
