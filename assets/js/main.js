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
      var swapped = false;
      /* iOS Low Power Mode and some data-saver settings refuse video autoplay
         outright. Animated images are exempt, so fall back to one. */
      function swapToAnimated() {
        if (swapped) return;
        swapped = true;
        var anim = video.getAttribute("data-anim");
        if (!anim) return;
        var img = document.createElement("img");
        img.src = anim;
        img.alt = video.getAttribute("aria-label") || "";
        img.decoding = "async";
        video.replaceWith(img);
      }
      var p = video.play();
      if (p && typeof p.catch === "function") { p.catch(swapToAnimated); }
      /* Belt and braces: data is buffered, nothing is playing, and no error fired */
      setTimeout(function () { if (video.isConnected && video.paused && !video.ended && video.readyState >= 2) swapToAnimated(); }, 4000);
      video.addEventListener("error", swapToAnimated, true);
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
      document.dispatchEvent(new CustomEvent("joyride:location", { detail: slug }));
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


  /* Availability search --------------------------------------------------- */
  /* Talks to the same booking system the checkout uses (izyRent). The API
     returns only the vehicles that are free for the searched dates, with
     stock, per-day bookings and the price table for each rental length. */
  var avail = document.querySelector(".avail");
  if (avail) {
    var API = "https://izyrent.speaz.com/front/get_availabilities";
    var LOCS = {};
    try { LOCS = JSON.parse(document.getElementById("joyride-locations").textContent); } catch (e) {}
    var form = avail.querySelector(".avail__form");
    var startIn = form.querySelector('[name="start"]');
    var endIn = form.querySelector('[name="end"]');
    var msg = avail.querySelector(".avail__msg");
    var results = avail.querySelector(".avail__results");
    var goBtn = form.querySelector(".avail__go");

    function pad(n) { return (n < 10 ? "0" : "") + n; }
    function iso(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
    function slash(s) { return s.replace(/-/g, "/"); }
    function parse(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function pretty(s) { return parse(s).toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
    function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
    function escapeHtml(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

    var today = iso(new Date());
    startIn.min = today; endIn.min = today;
    startIn.addEventListener("change", function () { if (startIn.value) { endIn.min = startIn.value; if (endIn.value && endIn.value < startIn.value) endIn.value = startIn.value; } });

    function currentSlug() {
      var active = document.querySelector(".locpanel.is-active");
      return (active && active.getAttribute("data-loc")) || avail.getAttribute("data-loc") || "delray-beach";
    }
    function currentLoc() { return LOCS[currentSlug()] || LOCS["delray-beach"] || { name: "Delray Beach", shop: "joy-ride-1689.myshopify.com" }; }

    function dayCount(a, b) { return Math.round((parse(b) - parse(a)) / 86400000) + 1; }

    /* Price for N days from the booking system's table; falls back to its "from" string. */
    function priceFor(product, days) {
      var vs = product.variantStock || {};
      var keys = Object.keys(vs).filter(function (k) { return k !== "product" && vs[k] && vs[k].prices; });
      for (var i = 0; i < keys.length; i++) {
        var rows = vs[keys[i]].prices;
        var exact = rows.filter(function (r) { return +r.days === days; })[0];
        if (exact) return { total: +exact.price, perDay: +exact.price / days };
        var ranged = rows.filter(function (r) { return typeof r.days === "number" && r.to && days >= r.days && days <= r.to; })[0];
        if (ranged) return { total: +ranged.price, perDay: +ranged.price / days };
      }
      return null;
    }

    /* Units free across the range: stock minus the busiest day's bookings. */
    function unitsFree(product, a, b) {
      var stock = parseInt(product.variantStock && product.variantStock.product && product.variantStock.product.stock, 10);
      if (isNaN(stock) || stock < 0) return null;
      var busiest = 0, d = parse(a), end = parse(b);
      while (d <= end) {
        var k = d.getFullYear() + "/" + pad(d.getMonth() + 1) + "/" + pad(d.getDate());
        var bk = product.bookings && product.bookings[k];
        if (bk && bk.count > busiest) busiest = bk.count;
        d.setDate(d.getDate() + 1);
      }
      return Math.max(0, stock - busiest);
    }

    function render(list, a, b) {
      var loc = currentLoc(); var days = dayCount(a, b);
      var vehicles = list.filter(function (p) { return !(/hourly/i.test(p.title) && days > 1); });
      if (!vehicles.length) {
        msg.textContent = "";
        results.innerHTML = '<div class="avail__empty"><p>Nothing is free in ' + escapeHtml(loc.name) + " for " + pretty(a) + " to " + pretty(b) + '. Try different dates, or call <a href="tel:' + escapeHtml(loc.tel) + '">' + escapeHtml(loc.phone) + "</a> and we will see what we can do.</p></div>";
        return;
      }
      msg.textContent = vehicles.length + (vehicles.length === 1 ? " vehicle" : " vehicles") + " available in " + loc.name + " for " + pretty(a) + " to " + pretty(b) + " (" + days + (days === 1 ? " day" : " days") + ").";
      var dates = slash(a) + "-" + slash(b);
      results.innerHTML = vehicles.map(function (p) {
        var free = unitsFree(p, a, b);
        var price = priceFor(p, days);
        var status = free === null ? "Available" : (free === 1 ? "Only 1 left for these dates" : free + " available");
        var low = free !== null && free <= 1;
        var priceHtml = price
          ? '<div class="vehicle__price">' + money(price.total) + "<small>" + money(price.perDay) + " per day, " + days + (days === 1 ? " day" : " days") + "</small></div>"
          : '<div class="vehicle__price">' + escapeHtml(p.price || "") + "</div>";
        var img = p.featuredImage ? '<img src="' + escapeHtml(p.featuredImage) + '" alt="' + escapeHtml(p.title) + '" loading="lazy">' : "";
        var url = (p.onlineStoreUrl || "#") + "?dates=" + encodeURIComponent(dates);
        return '<article class="vehicle"><div class="vehicle__media">' + img + '</div><div class="vehicle__body">' +
          '<h3 class="vehicle__title">' + escapeHtml(p.title) + "</h3>" +
          '<span class="vehicle__status' + (low ? " is-low" : "") + '">' + status + "</span>" +
          priceHtml +
          '<p class="vehicle__note">Refundable $250 deposit at delivery. Free delivery in ' + escapeHtml(loc.name) + ".</p>" +
          '<a class="btn btn--primary" href="' + escapeHtml(url) + '" target="_blank" rel="noopener">Reserve these dates</a>' +
          "</div></article>";
      }).join("");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var a = startIn.value, b = endIn.value;
      msg.classList.remove("is-error");
      if (!a || !b) { msg.classList.add("is-error"); msg.textContent = "Choose a start day and an end day."; return; }
      if (b < a) { msg.classList.add("is-error"); msg.textContent = "The end day is before the start day."; return; }
      var loc = currentLoc();
      goBtn.disabled = true; goBtn.textContent = "Checking";
      msg.textContent = "Checking " + loc.name + " for " + pretty(a) + " to " + pretty(b) + "...";
      results.innerHTML = "";
      fetch(API, { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ shop: loc.shop, searchDates: slash(a) + " - " + slash(b), currentCarts: "", filters: { idCollection: false, tags: [], sortBy: "" } }) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (list) { render(Array.isArray(list) ? list : [], a, b); })
        .catch(function () { msg.classList.add("is-error"); msg.textContent = "We could not reach the booking system. Call " + loc.phone + " and we will check for you."; })
        .then(function () { goBtn.disabled = false; goBtn.textContent = "Search"; });
    });

    document.addEventListener("joyride:location", function () {
      results.innerHTML = ""; msg.textContent = ""; msg.classList.remove("is-error");
    });
  }

  /* Current year ---------------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
