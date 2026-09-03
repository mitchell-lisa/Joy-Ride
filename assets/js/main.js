/* Joy Ride: site behaviour (no dependencies) */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header state ---------------------------------------------------------- */
  var header = document.querySelector(".header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile nav ------------------------------------------------------------ */
  var burger = document.querySelector(".burger");
  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav a").forEach(function (a) {
      a.addEventListener("click", function () { document.body.classList.remove("nav-open"); });
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") document.body.classList.remove("nav-open");
    });
  }

  /* Hero video: make sure it autoplays on mobile; the poster stands in if it cannot */
  var video = document.querySelector(".hero__media video");
  if (video) {
    if (reduceMotion) {
      video.removeAttribute("autoplay");
      video.pause();
    } else {
      video.muted = true;
      video.setAttribute("muted", "");
      var p = video.play();
      if (p && typeof p.catch === "function") { p.catch(function () {}); }
    }
  }

  /* Rate tables: on phones the middle tiers are hidden until asked for ------- */
  document.querySelectorAll(".rate-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var card = btn.closest(".rate-card");
      var open = card.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "Show fewer rates" : "Show all rates";
    });
  });

  /* Video modal (full YouTube clip) --------------------------------------- */
  var modal = document.querySelector(".modal");
  var frame = modal && modal.querySelector("iframe");
  document.querySelectorAll("[data-video]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!modal) return;
      e.preventDefault();
      frame.src = "https://www.youtube-nocookie.com/embed/" + btn.getAttribute("data-video") + "?autoplay=1&rel=0";
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
    });
  });
  function closeModal() {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    setTimeout(function () { frame.src = ""; }, 400);
  }
  if (modal) {
    modal.querySelector(".modal__close").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    window.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });
  }

  /* Location switcher ----------------------------------------------------- */
  var LS_KEY = "joyride.location";
  function getSaved() { try { return localStorage.getItem(LS_KEY); } catch (e) { return null; } }
  function save(slug) { try { localStorage.setItem(LS_KEY, slug); } catch (e) {} }

  var sw = document.querySelector(".locswitch");
  if (sw) {
    var swBtn = sw.querySelector(".locswitch__btn");
    swBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = sw.classList.toggle("is-open");
      swBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function () { sw.classList.remove("is-open"); swBtn.setAttribute("aria-expanded", "false"); });
    window.addEventListener("keydown", function (e) { if (e.key === "Escape") sw.classList.remove("is-open"); });
    sw.querySelectorAll("a[data-loc]").forEach(function (a) {
      a.addEventListener("click", function () { save(a.getAttribute("data-loc")); });
    });
  }

  /* Pages that embed every location's panel switch in place */
  var panels = document.querySelectorAll(".locpanel");
  if (panels.length) {
    var pills = document.querySelectorAll(".pill[data-loc]");
    function activate(slug, push) {
      var found = false;
      panels.forEach(function (p) { var on = p.getAttribute("data-loc") === slug; p.classList.toggle("is-active", on); if (on) found = true; });
      if (!found) return false;
      pills.forEach(function (p) { p.classList.toggle("is-active", p.getAttribute("data-loc") === slug); });
      document.querySelectorAll("[data-loc-name]").forEach(function (el) {
        var src = document.querySelector('.locpanel[data-loc="' + slug + '"]');
        if (src) el.textContent = src.getAttribute("data-name");
      });
      if (sw) {
        sw.querySelectorAll("a[data-loc]").forEach(function (a) { a.setAttribute("aria-current", a.getAttribute("data-loc") === slug ? "true" : "false"); });
        var lbl = sw.querySelector("[data-loc-label]"); var src = document.querySelector('.locpanel[data-loc="' + slug + '"]');
        if (lbl && src) lbl.textContent = src.getAttribute("data-name");
      }
      save(slug);
      if (push && history.replaceState) history.replaceState(null, "", "#" + slug);
      return true;
    }
    var initial = (location.hash || "").replace("#", "");
    if (!activate(initial, false)) {
      if (!activate(getSaved() || "", false)) activate(panels[0].getAttribute("data-loc"), false);
    }
    pills.forEach(function (p) {
      p.addEventListener("click", function (e) {
        e.preventDefault();
        activate(p.getAttribute("data-loc"), true);
        var target = document.querySelector(p.getAttribute("data-scroll") || "");
        if (target) target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      });
    });
    if (sw) {
      sw.querySelectorAll("a[data-loc]").forEach(function (a) {
        a.addEventListener("click", function (e) {
          if (a.hasAttribute("data-inplace")) { e.preventDefault(); activate(a.getAttribute("data-loc"), true); sw.classList.remove("is-open");
            var target = document.querySelector("#rates"); if (target) target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" }); }
        });
      });
    }
    window.addEventListener("hashchange", function () { activate((location.hash || "").replace("#", ""), false); });
  } else if (sw) {
    // Plain pages: reflect the remembered location in the switcher label
    var saved = getSaved();
    var current = sw.getAttribute("data-current");
    if (!current && saved) {
      var a = sw.querySelector('a[data-loc="' + saved + '"]'); var lbl = sw.querySelector("[data-loc-label]");
      if (a && lbl) { lbl.textContent = a.getAttribute("data-name"); a.setAttribute("aria-current", "true"); }
    }
  }

  /* Current year ---------------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
