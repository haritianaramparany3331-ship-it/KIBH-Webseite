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
      // Write into the label span if there is one, so a chevron or icon beside
      // it survives the swap. Falls back to the button itself.
      var label = btn.querySelector(".btn__label") || btn;
      label.textContent = btn.getAttribute(open ? "data-label-less" : "data-label-more");

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

/* --------------------------------------------------------------------------
   Magnetic booking CTAs.

   Scoped to button-styled links pointing at the booking page and nothing else.
   The cursor pulls the button a fraction of its own offset from the button's
   centre, capped at a few pixels, and it eases back when the cursor leaves.
   CSS composes --mag-x/--mag-y with the button's existing hover lift, so this
   never fights the styles already on it.
   -------------------------------------------------------------------------- */
(function () {
  "use strict";

  // A magnet needs something to attract: no cursor, no effect.
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var btns = document.querySelectorAll(
    'a.btn[href="/kontakt/"], a.er-btn[href="/kontakt/"]'
  );
  if (!btns.length) return;

  var PULL = 0.18;  // fraction of the cursor's offset from centre
  var MAX = 6;      // px, hard cap on the shift
  var NEAR = 26;    // px of reactive margin around the button's own box

  Array.prototype.forEach.call(btns, function (b) { b.classList.add("is-magnet"); });

  var frame = 0;
  var mx = -1e4;
  var my = -1e4;

  function clamp(v) { return Math.max(-MAX, Math.min(MAX, v)); }

  function apply() {
    frame = 0;
    Array.prototype.forEach.call(btns, function (b) {
      var r = b.getBoundingClientRect();
      if (!r.width) return;

      /*
        The rect already carries whatever shift is currently applied, so the
        centre it reports is the displaced one. Subtracting the shift we asked
        for gets back to the resting centre; without this the button chases
        its own transform.
      */
      var ox = parseFloat(b.style.getPropertyValue("--mag-x")) || 0;
      var oy = parseFloat(b.style.getPropertyValue("--mag-y")) || 0;
      var dx = mx - (r.left + r.width / 2 - ox);
      var dy = my - (r.top + r.height / 2 - oy);

      if (Math.abs(dx) <= r.width / 2 + NEAR && Math.abs(dy) <= r.height / 2 + NEAR) {
        b.style.setProperty("--mag-x", clamp(dx * PULL).toFixed(2) + "px");
        b.style.setProperty("--mag-y", clamp(dy * PULL).toFixed(2) + "px");
      } else if (ox || oy) {
        b.style.removeProperty("--mag-x");
        b.style.removeProperty("--mag-y");
      }
    });
  }

  function schedule() {
    if (!frame) frame = window.requestAnimationFrame(apply);
  }

  window.addEventListener("pointermove", function (e) {
    if (e.pointerType && e.pointerType !== "mouse") return;
    mx = e.clientX;
    my = e.clientY;
    schedule();
  }, { passive: true });

  // Scrolling moves the buttons past a stationary cursor, so the shift has to
  // be recomputed even though the pointer itself has not moved.
  window.addEventListener("scroll", schedule, { passive: true });

  document.addEventListener("pointerleave", function () {
    mx = my = -1e4;
    schedule();
  });
})();

/* --------------------------------------------------------------------------
   Client logo strip -> continuous marquee.

   The seven logos move into a flex track which is then duplicated, and the
   track slides exactly one group's width before the animation repeats, so the
   loop has no visible seam. Without JS the strip stays the static grid it is
   in the markup.
   -------------------------------------------------------------------------- */
(function () {
  "use strict";

  var strips = document.querySelectorAll("[data-marquee]");
  if (!strips.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var SPEED = 42; // px per second

  Array.prototype.forEach.call(strips, function (strip) {
    var items = Array.prototype.slice.call(strip.children);
    if (items.length < 2) return;

    var track = document.createElement("div");
    track.className = "logos__track";

    var group = document.createElement("div");
    group.className = "logos__group";
    items.forEach(function (el) {
      /*
        Lazy loading has to come off here. In the static grid the whole strip
        is on screen, but in the track the later logos sit hundreds of pixels
        off to the right, so the browser defers them and they pop in blank as
        the marquee brings them round -- worst at narrow viewports, where the
        last two never loaded at all. The seven files are 113 KB together.
      */
      var img = el.tagName === "IMG" ? el : el.querySelector("img");
      if (img) img.loading = "eager";
      group.appendChild(el);
    });
    track.appendChild(group);

    // The second group exists only to fill the space the first one vacates as
    // it scrolls out. It carries no information a reader has not already had,
    // so it is hidden from assistive technology.
    var clone = group.cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    track.appendChild(clone);

    strip.appendChild(track);
    strip.classList.add("is-marquee");

    /*
      One group's width is exactly how far the track travels per cycle, so
      deriving the duration from it keeps the strip moving at the same speed
      whatever the viewport. Logo widths are fixed in CSS, so this measures
      correctly whether or not the images have decoded yet.
    */
    var w = group.getBoundingClientRect().width;
    if (w) track.style.animationDuration = (w / SPEED).toFixed(1) + "s";

    /*
      Pausing used to be a :hover rule. On a touch screen :hover latches when
      you tap and, on iOS, stays latched until you tap somewhere else -- so
      one stray touch froze the strip for good. Driving the class from pointer
      events instead gives a mouse the same hover-to-pause it had, and gives a
      finger press-and-hold, which is the only way a touch visitor has to stop
      it at all.
    */
    var pause = function () { strip.classList.add("is-paused"); };
    var resume = function () { strip.classList.remove("is-paused"); };

    strip.addEventListener("pointerenter", function (e) {
      if (e.pointerType === "mouse") pause();
    });
    strip.addEventListener("pointerleave", function (e) {
      if (e.pointerType === "mouse") resume();
    });
    strip.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse") pause();
    }, { passive: true });
    ["pointerup", "pointercancel"].forEach(function (ev) {
      strip.addEventListener(ev, function (e) {
        if (e.pointerType !== "mouse") resume();
      }, { passive: true });
    });
  });
})();

/* --------------------------------------------------------------------------
   Cursor-following background glow.

   Trails the cursor rather than tracking it exactly. It is a ground, not an
   overlay: it paints below every section's content and takes no pointer
   events, so it can never intercept a click or a selection.

   Two kinds of copy. One fixed copy behind the whole page, which shows
   wherever a section paints no ground of its own; and one clipped copy inside
   each section that does paint a ground, because an opaque background would
   otherwise hide the fixed copy completely -- which is what happened across
   the whole of /ergebnisse/ and /deep-reading-engine/, and over the homepage
   hero. Both copies move together, so the glow reads as one continuous thing
   as the cursor crosses a section boundary.
   -------------------------------------------------------------------------- */
(function () {
  "use strict";

  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  function makeSpot() {
    var el = document.createElement("div");
    el.className = "cursor-glow";
    el.setAttribute("aria-hidden", "true");
    return el;
  }

  var base = makeSpot();
  document.body.appendChild(base);

  var spots = [base];
  var grounds = [];

  Array.prototype.forEach.call(
    document.querySelectorAll("main > *, .site-footer"),
    function (el) {
      var c = window.getComputedStyle(el);
      var m = /rgba?\(([^)]+)\)/.exec(c.backgroundColor);
      var parts = m ? m[1].split(",") : null;
      var alpha = parts ? (parts[3] === undefined ? 1 : parseFloat(parts[3])) : 0;
      // Nothing to hide the fixed copy: leave this section to it.
      if (alpha < 0.9 && c.backgroundImage === "none") return;

      // Set inline and only when static, so a sticky or absolute section keeps
      // whatever positioning it already relies on.
      if (c.position === "static") el.style.position = "relative";
      el.classList.add("has-glow-ground");

      var layer = document.createElement("span");
      layer.className = "glow-ground";
      layer.setAttribute("aria-hidden", "true");
      var spot = makeSpot();
      layer.appendChild(spot);
      el.insertBefore(layer, el.firstChild);

      spots.push(spot);
      grounds.push({ el: el, spot: spot });
    }
  );

  var EASE = 0.075;  // fraction of the remaining distance covered per frame
  var tx = 0, ty = 0;   // where the cursor is
  var gx = 0, gy = 0;   // where the glow has got to
  var placed = false;
  var running = false;

  function paint() {
    /*
      Every rect is read before any transform is written. Interleaving them
      would force a layout on each ground, every frame.
    */
    var rects = grounds.map(function (g) { return g.el.getBoundingClientRect(); });
    var x = gx.toFixed(1), y = gy.toFixed(1);
    base.style.transform = "translate3d(" + x + "px," + y + "px,0)";
    for (var i = 0; i < grounds.length; i++) {
      grounds[i].spot.style.transform =
        "translate3d(" + (gx - rects[i].left).toFixed(1) + "px," +
        (gy - rects[i].top).toFixed(1) + "px,0)";
    }
  }

  function frame() {
    var dx = tx - gx;
    var dy = ty - gy;
    gx += dx * EASE;
    gy += dy * EASE;
    paint();

    // Stop once it has caught up, so an idle page schedules no frames at all.
    if (Math.abs(dx) > 0.4 || Math.abs(dy) > 0.4) {
      window.requestAnimationFrame(frame);
    } else {
      running = false;
    }
  }

  function run() {
    if (!running) {
      running = true;
      window.requestAnimationFrame(frame);
    }
  }

  window.addEventListener("pointermove", function (e) {
    if (e.pointerType && e.pointerType !== "mouse") return;
    tx = e.clientX;
    ty = e.clientY;

    if (!placed) {
      // Start where the cursor already is, rather than sliding in from 0,0.
      placed = true;
      gx = tx;
      gy = ty;
      paint();
      spots.forEach(function (s) { s.classList.add("is-on"); });
    }
    run();
  }, { passive: true });

  // Scrolling slides the grounds past a stationary cursor, so their local
  // coordinates change even though the pointer has not moved.
  window.addEventListener("scroll", run, { passive: true });

  document.addEventListener("pointerleave", function () {
    spots.forEach(function (s) { s.classList.remove("is-on"); });
  });
  document.addEventListener("pointerenter", function () {
    if (placed) spots.forEach(function (s) { s.classList.add("is-on"); });
  });
})();
