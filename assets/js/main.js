/* Joy Ride — site behaviour (no dependencies) */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("js");

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

  /* Split headline into words for the reveal ----------------------------- */
  document.querySelectorAll(".split").forEach(function (el) {
    var html = "";
    el.childNodes.forEach(function (node) {
      if (node.nodeType === 3) {
        node.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { html += " "; return; }
          html += '<span class="w"><span>' + part + "</span></span>";
        });
      } else if (node.nodeType === 1) {
        if (node.tagName === "BR") { html += "<br>"; return; }
        html += '<span class="w"><span>' + node.outerHTML + "</span></span>";
      }
    });
    el.innerHTML = html;
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add("in"); }); });
  });

  /* Reveal on scroll ------------------------------------------------------ */
  var targets = document.querySelectorAll(".reveal, .steps");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("in"); });
  }

  /* Hero video: guarantee autoplay on mobile, fall back to the GIF -------- */
  var video = document.querySelector(".hero__media video");
  if (video) {
    if (reduceMotion) {
      video.removeAttribute("autoplay");
      video.pause();
    } else {
      video.muted = true;               // iOS requires the property, not only the attribute
      video.setAttribute("muted", "");
      var p = video.play();
      if (p && typeof p.catch === "function") {
        p.catch(function () { swapToGif(video); });
      }
      video.addEventListener("error", function () { swapToGif(video); }, true);
    }
  }
  function swapToGif(v) {
    var gif = v.getAttribute("data-gif");
    if (!gif) return;
    var img = document.createElement("img");
    img.src = gif; img.alt = v.getAttribute("aria-label") || "";
    v.replaceWith(img);
  }

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

  /* Marquee: duplicate content so the loop is seamless -------------------- */
  document.querySelectorAll(".marquee__track").forEach(function (track) {
    track.innerHTML = track.innerHTML + track.innerHTML;
  });

  /* Current year ---------------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
