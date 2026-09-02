#!/usr/bin/env python3
"""
Joy Ride static site generator.

Every page in the site root is generated from the templates below so that the
header, footer, meta tags and JSON-LD stay identical across pages.

    python3 tools/build.py

Edit content here (or in tools/content/), re-run, commit the generated HTML.
"""
import os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://www.joyridedelray.com"

# ----------------------------------------------------------------------------
# Business facts (single source of truth)
# ----------------------------------------------------------------------------
BIZ = {
    "name": "Joy Ride Delray Beach Golf Cart Rentals",
    "short": "Joy Ride",
    "phone_display": "(561) 569-2438",
    "phone_tel": "+15615692438",
    "email": "rentals@joyridedelray.com",
    "address": "820 E Atlantic Ave, Delray Beach, FL 33483",
    "street": "820 E Atlantic Ave", "city": "Delray Beach", "state": "FL", "zip": "33483",
    "lat": 26.4615, "lng": -80.0648,
    "rating": "5.0", "review_count": 57,
    # Google Business Profile. Replace with the exact Place ID link when handy:
    # https://search.google.com/local/writereview?placeid=YOUR_PLACE_ID
    "google_reviews": "https://www.google.com/maps/search/?api=1&query=Joy+Ride+Delray+Beach+Golf+Cart+Rentals+820+E+Atlantic+Ave+Delray+Beach+FL",
    "google_write_review": "https://www.google.com/maps/search/?api=1&query=Joy+Ride+Delray+Beach+Golf+Cart+Rentals+820+E+Atlantic+Ave+Delray+Beach+FL",
    "book_cart": "https://www.joyridedelray.com/products/one-day-golf-cart-rental",
    "book_moke": "https://www.joyridedelray.com/products/electric-mini-moke",
    "youtube_id": "SMVaJwEa5kc",
    "affiliate": "https://joy-ride-1689.jaka.app",
}

LOCATIONS = [
    {"city": "Delray Beach", "state": "FL", "hq": True,
     "blurb": "Our home base on Atlantic Avenue. Free delivery across Delray Beach, Boca Raton, Boynton Beach, Highland Beach and Gulf Stream.",
     "phone": BIZ["phone_display"], "tel": BIZ["phone_tel"], "site": None},
    {"city": "Palm Beach", "state": "FL",
     "blurb": "Island cruising from Worth Avenue to the Lake Trail, delivered to your door.",
     "phone": "(561) 562-7152", "tel": "+15615627152", "site": "https://www.joyridepalmbeach.com"},
    {"city": "Ft Lauderdale & Pompano Beach", "state": "FL",
     "blurb": "Beach-to-boardwalk rides along the A1A corridor in Broward County.",
     "phone": BIZ["phone_display"], "tel": BIZ["phone_tel"], "site": "https://joyridepompanobeach.com"},
    {"city": "Vero Beach", "state": "FL",
     "blurb": "Ocean Drive, the beachside village and quiet Treasure Coast streets.",
     "phone": BIZ["phone_display"], "tel": BIZ["phone_tel"], "site": None},
    {"city": "Jacksonville", "state": "FL",
     "blurb": "Jacksonville Beach, Ponte Vedra and St. Augustine with same-day delivery.",
     "phone": "(904) 834-9466", "tel": "+19048349466", "site": "https://joyridejacksonville.com"},
    {"city": "Dewey & Rehoboth Beach", "state": "DE",
     "blurb": "Summer on the Delaware shore, from the boardwalk to the bay.",
     "phone": BIZ["phone_display"], "tel": BIZ["phone_tel"], "site": None},
    {"city": "Charleston", "state": "SC",
     "blurb": "Folly Beach, Sullivan's Island and the Isle of Palms in Lowcountry style.",
     "phone": "(843) 905-2495", "tel": "+18439052495", "site": "https://joyridecharleston.com"},
    {"city": "Montauk", "state": "NY",
     "blurb": "The End of Long Island, from Ditch Plains to the harbor.",
     "phone": "(631) 430-6653", "tel": "+16314306653", "site": "https://joyridemontauk.com"},
]

CART_RATES = [("1 day", 250), ("2 days", 190), ("3 days", 180), ("4–5 days", 170), ("6 days", 160), ("7 days", 150), ("8+ days", 140)]
MOKE_RATES = [("1 day", 300), ("2 days", 200), ("3 days", 190), ("4–5 days", 170), ("6 days", 160), ("7 days", 150), ("8+ days", 140)]

REVIEWS = [
    ("Christos L.", "Sep 2025", "The process was quick, smooth, and hassle-free from start to finish. The staff was professional, friendly, and very accommodating."),
    ("Lisa S.", "Apr 2025", "Both Matt and Dan were so easy to deal with. Professional and efficient with the process. A seamless process."),
    ("Jonathan H.", "Jan 2025", "It was in perfect condition, packed with great features like a backup camera and speakers. The staff was super helpful and friendly."),
    ("Mark M.", "Nov 2024", "The thing about the golf cart is you get all the fresh air with some protection from the sun. In great shape and had many unexpected extras."),
    ("Ye S.", "Sep 2023", "I got a brand-new one with a backup camera, touchscreen and really good range. They were so friendly and this was such a fun experience."),
]

NAV = [("Rent", "/rentals"), ("Locations", "/locations"), ("Events", "/events"), ("Sales", "/sales"), ("Map", "/golf-cart-map"), ("Contact", "/contact")]

# ----------------------------------------------------------------------------
# Small SVG icons (inline, currentColor)
# ----------------------------------------------------------------------------
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_WHEEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/><path d="M12 6.5v-4M12 21.5v-4M6.5 12h-4M21.5 12h-4M8.1 8.1 5.3 5.3M18.7 18.7l-2.8-2.8M15.9 8.1l2.8-2.8M5.3 18.7l2.8-2.8"/></svg>'
ICON_G = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.7-2.4 3.6v3h3.9c2.3-2.1 3.5-5.2 3.5-8.8z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.2v3.1C3.2 21.3 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.3 14.3c-.5-1.5-.5-3.1 0-4.6V6.6H1.2c-1.6 3.2-1.6 7 0 10.2l4.1-2.5z"/><path fill="#EA4335" d="M12 4.7c1.7 0 3.3.6 4.5 1.8l3.4-3.4C17.9 1.2 15.1 0 12 0 7.3 0 3.2 2.7 1.2 6.6l4.1 3.1C6.2 6.8 8.9 4.7 12 4.7z"/></svg>'
ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l12-7.5z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3 7 9 6 9-6"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_TRUCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M12 2.5 4 5.5v6c0 5 3.5 8.5 8 10 4.5-1.5 8-5 8-10v-6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>'
ICON_CARD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="1.5"/><path d="M2.5 9.5h19M6 15h4"/></svg>'

def stars(n=5):
    return "★" * n

# ----------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------
def layout(*, title, description, path, body, over_hero=False, noindex=False, extra_head=""):
    canonical = SITE_URL + ("" if path == "/" else path)
    nav_links = ""
    for label, href in NAV:
        current = ' aria-current="page"' if href == path else ""
        nav_links += '<a class="nav__link" href="%s"%s>%s</a>' % (href, current, label)
    header_cls = "header header--over" if over_hero else "header"
    year = datetime.date.today().year
    jsonld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BIZ["name"],
        "image": SITE_URL + "/assets/img/og-image.jpg",
        "url": SITE_URL,
        "telephone": BIZ["phone_tel"],
        "email": BIZ["email"],
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"], "addressRegion": BIZ["state"], "postalCode": BIZ["zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": BIZ["rating"], "reviewCount": BIZ["review_count"]},
        "areaServed": [f"{l['city']}, {l['state']}" for l in LOCATIONS],
        "sameAs": [l["site"] for l in LOCATIONS if l["site"]],
    }
    import json
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
{'<meta name="robots" content="noindex,nofollow">' if noindex else ''}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Joy Ride">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#004aad">
<link rel="icon" href="/assets/logo/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="/assets/fonts/Italiana-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
{extra_head}
<script type="application/ld+json">{json.dumps(jsonld, indent=0)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><span>Call or text to reserve: <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></span><span class="topbar__extra">&nbsp;·&nbsp; Free door-to-door delivery</span></div>
<header class="{header_cls}">
  <div class="container header__inner">
    <a class="brand" href="/" aria-label="Joy Ride home">
      <img class="brand__dark" src="/assets/logo/joyride-lockup.svg" alt="Joy Ride" width="192" height="46">
      <img class="brand__light" src="/assets/logo/joyride-lockup-white.svg" alt="Joy Ride" width="192" height="46">
    </a>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Primary">
      {nav_links}
      <a class="btn btn--primary nav__cta" href="/rentals#reserve">Reserve</a>
      <a class="nav__phone" href="tel:{BIZ['phone_tel']}">Call or text {BIZ['phone_display']}</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="/assets/logo/joyride-lockup-white.svg" alt="Joy Ride" width="233" height="56">
        <p>Street-legal golf cart and electric Moke rentals, delivered free to your door. Live like a local and take a Joy Ride.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/rentals">Golf Cart &amp; Moke Rentals</a></li>
          <li><a href="/locations">Locations</a></li>
          <li><a href="/events">Event Bookings</a></li>
          <li><a href="/sales">Golf Cart Sales</a></li>
          <li><a href="/golf-cart-map">Delray Beach Golf Cart Map</a></li>
          <li><a href="/affiliate">Become an Affiliate</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/contact">Contact</a></li>
          <li><a href="{BIZ['google_reviews']}" target="_blank" rel="noopener">Google Reviews</a></li>
          <li><a href="/refund-policy">Refund Policy</a></li>
          <li><a href="/terms-of-service">Terms of Service</a></li>
        </ul>
      </div>
      <div class="footer__contact">
        <h4>Get in touch</h4>
        <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a>
        <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
        <p class="small" style="margin-top:12px">{BIZ['address']}</p>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>{year}</span> Joy Ride · MB Meadows LLC</span>
      <span>Delray Beach · Palm Beach · Pompano · Vero · Jacksonville · Rehoboth · Charleston · Montauk</span>
    </div>
  </div>
</footer>
<div class="modal" aria-hidden="true" role="dialog" aria-label="Joy Ride video">
  <button class="modal__close" aria-label="Close video">×</button>
  <div class="modal__box"><iframe title="Joy Ride Golf Cart Rentals video" src="" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------
# Reusable blocks
# ----------------------------------------------------------------------------
def rate_table(rows):
    best = rows[-1][0]
    out = ['<table class="rate-table">']
    for label, price in rows:
        cls = ' class="is-best"' if label == best else ""
        out.append(f"<tr{cls}><td>{label}</td><td>${price}<small>/ day</small></td></tr>")
    out.append("</table>")
    return "\n".join(out)

def rates_block():
    return f"""
<div class="rates">
  <div class="rate-card reveal" data-delay="1">
    <h3>Golf Cart <span>6 seats · street legal</span></h3>
    {rate_table(CART_RATES)}
    <p class="rate-note">Multi-day rates are per day. A refundable $250 security deposit is collected at delivery.</p>
    <a class="btn btn--primary mt-2" href="{BIZ['book_cart']}" target="_blank" rel="noopener">Reserve a golf cart {ICON_ARROW}</a>
  </div>
  <div class="rate-card reveal" data-delay="2">
    <h3>Electric Moke <span>4 seats · open top</span></h3>
    {rate_table(MOKE_RATES)}
    <p class="rate-note">Multi-day rates are per day. A refundable $250 security deposit is collected at delivery.</p>
    <a class="btn btn--red mt-2" href="{BIZ['book_moke']}" target="_blank" rel="noopener">Reserve a Moke {ICON_ARROW}</a>
  </div>
</div>"""

def reviews_block(heading="Riders love it. So does Google."):
    cards = "".join(
        f"""<article class="review reveal" data-delay="{(i % 3) + 1}">
  <div class="stars" aria-label="5 out of 5 stars">{stars()}</div>
  <p>“{html.escape(text)}”</p>
  <footer><strong>{html.escape(name)}</strong><span>{date} · Google</span></footer>
</article>"""
        for i, (name, date, text) in enumerate(REVIEWS)
    )
    return f"""
<section class="section section--white" id="reviews">
  <div class="container">
    <div class="reviews-head">
      <div class="rating reveal">
        <div class="rating__num">{BIZ['rating']}</div>
        <div class="rating__meta">
          <div class="rating__stars" aria-hidden="true">{stars()}</div>
          <span>{BIZ['review_count']} Google reviews</span>
          <span>Delray Beach, FL</span>
        </div>
      </div>
      <div class="section-head reveal" data-delay="1" style="margin-bottom:0">
        <div class="eyebrow">Google Reviews</div>
        <h2>{heading}</h2>
        <p>Every review below is from our Google Business Profile. Read them all, or tell us how your ride went.</p>
      </div>
    </div>
    <div class="reviews">{cards}</div>
    <div class="reviews-actions reveal">
      <a class="gbadge gbadge--dark" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> · Read all {BIZ['review_count']} reviews</span></a>
      <a class="btn btn--ghost" href="{BIZ['google_write_review']}" target="_blank" rel="noopener">Leave a review {ICON_ARROW}</a>
    </div>
  </div>
</section>"""

def locations_grid():
    cards = []
    for i, l in enumerate(LOCATIONS):
        links = [f'<a href="tel:{l["tel"]}">{l["phone"]}</a>']
        if l["site"]:
            links.append(f'<a href="{l["site"]}" target="_blank" rel="noopener">Local site</a>')
        else:
            links.append('<a href="/rentals#reserve">Reserve</a>')
        cards.append(f"""<div class="loc{' loc--hq' if l.get('hq') else ''} reveal" data-delay="{(i % 4) + 1}">
  <div class="loc__state">{l['state']}</div>
  <h3>{html.escape(l['city'])}</h3>
  <p>{html.escape(l['blurb'])}</p>
  <div class="loc__links">{' '.join(links)}</div>
</div>""")
    return '<div class="locations">' + "\n".join(cards) + "</div>"

def cta_band():
    return f"""
<section class="section section--blue cta-band">
  <img class="wheel-bg" src="/assets/logo/wheel-white.svg" alt="" aria-hidden="true">
  <div class="container">
    <div class="reveal">
      <div class="eyebrow">Ready to ride?</div>
      <h2>Your cart is one call away.</h2>
      <p>Reserve online in two minutes, or call and we will set it up for you. Free delivery, cash or card at the door.</p>
    </div>
    <div class="reveal" data-delay="1">
      <a class="cta-band__phone" href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a>
      <p class="small">Call or text, 7 days a week</p>
      <div class="btn-row mt-2">
        <a class="btn btn--light" href="{BIZ['book_cart']}" target="_blank" rel="noopener">Reserve a golf cart</a>
        <a class="btn btn--outline-light" href="{BIZ['book_moke']}" target="_blank" rel="noopener">Reserve a Moke</a>
      </div>
    </div>
  </div>
</section>"""

def page_hero(eyebrow, title, lead, image=None, alt=""):
    if image:
        return f"""
<section class="page-hero page-hero--image">
  <div class="page-hero__media"><img src="{image}" alt="{html.escape(alt)}" fetchpriority="high"></div>
  <div class="container">
    <div class="eyebrow reveal">{eyebrow}</div>
    <h1 class="split">{title}</h1>
    <p class="lead reveal" data-delay="2">{lead}</p>
  </div>
</section>"""
    return f"""
<section class="page-hero">
  <div class="container">
    <div class="eyebrow reveal">{eyebrow}</div>
    <h1 class="split">{title}</h1>
    <p class="lead reveal" data-delay="2">{lead}</p>
  </div>
</section>"""

# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_home():
    marquee_items = "".join(f'<span class="marquee__item">{ICON_WHEEL}{html.escape(l["city"])}, {l["state"]}</span>' for l in LOCATIONS)
    body = f"""
<section class="hero">
  <div class="hero__media">
    <video autoplay muted loop playsinline preload="metadata" poster="/assets/video/hero-poster.jpg" data-gif="/assets/video/hero.gif" aria-label="Joy Ride golf carts and Mokes cruising Delray Beach">
      <source src="/assets/video/hero.webm" type="video/webm">
      <source src="/assets/video/hero.mp4" type="video/mp4">
      <img src="/assets/video/hero.gif" alt="Joy Ride golf carts and Mokes cruising Delray Beach">
    </video>
  </div>
  <div class="container hero__content">
    <div class="eyebrow hero__eyebrow reveal">Delray Beach · Est. 2022</div>
    <h1 class="split">Live like a local. Take a Joy Ride.</h1>
    <p class="hero__sub reveal" data-delay="2">Street-legal six-seat golf carts and open-top electric Mokes, delivered free to your door in Delray Beach and seven more beach towns.</p>
    <div class="btn-row reveal" data-delay="3">
      <a class="btn btn--primary" href="{BIZ['book_cart']}" target="_blank" rel="noopener">Rent a golf cart {ICON_ARROW}</a>
      <a class="btn btn--outline-light" href="{BIZ['book_moke']}" target="_blank" rel="noopener">Rent a Moke {ICON_ARROW}</a>
    </div>
    <div class="hero__bottom reveal" data-delay="4">
      <a class="gbadge" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> · {BIZ['review_count']} Google reviews</span></a>
      <a class="hero__scroll" href="#fleet"><i></i>Scroll</a>
    </div>
  </div>
</section>

<div class="marquee" aria-label="Locations"><div class="marquee__track">{marquee_items}</div></div>

<section class="section" id="fleet">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">The fleet</div>
      <h2>Two ways to ride.</h2>
      <p>Every vehicle is all-electric, street legal and fitted with seat belts, headlights, turn signals and a backup camera. Top speed 25 mph, range of 25 to 35 miles.</p>
    </div>
    <div class="fleet">
      <article class="ride reveal" data-delay="1">
        <div class="ride__media"><img src="/assets/img/cart-beach-1600.webp" srcset="/assets/img/cart-beach-900.webp 900w, /assets/img/cart-beach-1600.webp 1600w" sizes="(max-width: 760px) 100vw, 50vw" alt="White six-seat ICON golf cart on the beach in Delray Beach" loading="lazy"></div>
        <span class="ride__tag">Most popular</span>
        <div class="ride__body">
          <div class="ride__title"><h3>Six-Seat Golf Cart</h3><div class="ride__price">$250<small>from / day</small></div></div>
          <p>Our signature lifted ICON six-seater. Room for the whole crew, Bluetooth speakers, and a roof for the midday sun.</p>
          <ul class="ride__specs"><li>Seats 6</li><li>25 mph street legal</li><li>Seat belts &amp; lights</li><li>Backup camera</li></ul>
          <div class="ride__actions">
            <a class="btn btn--primary" href="{BIZ['book_cart']}" target="_blank" rel="noopener">Reserve</a>
            <a class="btn btn--ghost" href="/rentals#golf-cart">Details</a>
          </div>
        </div>
      </article>
      <article class="ride reveal" data-delay="2">
        <div class="ride__media"><img src="/assets/img/moke-parked-1600.webp" srcset="/assets/img/moke-parked-900.webp 900w, /assets/img/moke-parked-1600.webp 1600w" sizes="(max-width: 760px) 100vw, 50vw" alt="Red electric Moke parked under palm trees" loading="lazy"></div>
        <span class="ride__tag ride__tag--red">Turns heads</span>
        <div class="ride__body">
          <div class="ride__title"><h3>Electric Moke</h3><div class="ride__price">$300<small>from / day</small></div></div>
          <p>The open-top beach classic, reborn electric. Bright colors, four seats and pure vacation energy along A1A.</p>
          <ul class="ride__specs"><li>Seats 4</li><li>25 mph street legal</li><li>Seat belts &amp; lights</li><li>All electric</li></ul>
          <div class="ride__actions">
            <a class="btn btn--red" href="{BIZ['book_moke']}" target="_blank" rel="noopener">Reserve</a>
            <a class="btn btn--ghost" href="/rentals#moke">Details</a>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--sand2" id="rates">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">Daily rates</div>
      <h2>The longer you ride, the less you pay.</h2>
      <p>Simple per-day pricing that drops every day you keep the cart. No hidden fees, and delivery is always free.</p>
    </div>
    {rates_block()}
  </div>
</section>

<section class="section" id="how">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">How it works</div>
      <h2>Booked to beach in four easy steps.</h2>
    </div>
    <div class="steps">
      <div class="step reveal" data-delay="1"><h3>Reserve</h3><p>Pick your dates online or call us. Drivers must be 21+, renters 25+.</p></div>
      <div class="step reveal" data-delay="2"><h3>We deliver</h3><p>Your cart arrives fully charged at your home, hotel or rental, free of charge.</p></div>
      <div class="step reveal" data-delay="3"><h3>Ride</h3><p>Cruise the beach, Atlantic Avenue and everywhere in between like a local.</p></div>
      <div class="step reveal" data-delay="4"><h3>We pick up</h3><p>Leave it where we dropped it. Your $250 deposit is refunded on return.</p></div>
    </div>
  </div>
</section>

<section class="section section--white" id="gallery">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">Out and about</div>
      <h2>Delray, seen from a Joy Ride.</h2>
    </div>
    <div class="gallery reveal">
      <figure><img src="/assets/img/fleet-beach-1600.webp" srcset="/assets/img/fleet-beach-900.webp 900w, /assets/img/fleet-beach-1600.webp 1600w" sizes="(max-width: 760px) 100vw, 60vw" alt="A Joy Ride golf cart and red Moke side by side at the beach" loading="lazy"><figcaption>Golf cart &amp; Moke</figcaption></figure>
      <figure><img src="/assets/img/ride-atlantic-900.webp" alt="Golf cart and Moke driving through a Delray Beach intersection" loading="lazy"><figcaption>Atlantic Avenue</figcaption></figure>
      <figure><img src="/assets/img/video-still-900.webp" alt="Still from the Joy Ride video" loading="lazy"><a class="play" href="https://youtu.be/{BIZ['youtube_id']}" data-video="{BIZ['youtube_id']}" aria-label="Play the Joy Ride video"><span>{ICON_PLAY}</span></a><figcaption>Watch the video</figcaption></figure>
    </div>
  </div>
</section>

{reviews_block()}

<section class="section" id="locations">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">Locations</div>
      <h2>Eight beach towns. One Joy Ride.</h2>
      <p>We started in Delray Beach and now deliver up and down the coast. Same carts, same free delivery, same easy booking.</p>
    </div>
    {locations_grid()}
    <p class="mt-4 reveal"><a class="link" href="/locations">All locations &amp; delivery areas {ICON_ARROW}</a></p>
  </div>
</section>

<section class="section section--sand2">
  <div class="container">
    <div class="trio">
      <div class="trio__item reveal" data-delay="1">{ICON_TRUCK}<h3>Free delivery</h3><p>Door-to-door drop-off and pick-up anywhere in our delivery area. No trailer, no hassle.</p></div>
      <div class="trio__item reveal" data-delay="2">{ICON_SHIELD}<h3>Safe &amp; street legal</h3><p>Seat belts, headlights, hazards and turn signals on every vehicle. Fully insured and registered.</p></div>
      <div class="trio__item reveal" data-delay="3">{ICON_CARD}<h3>Easy payment</h3><p>All major credit cards online, or cash on delivery. Refundable $250 deposit at the door.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media reveal"><img src="/assets/img/ride-atlantic-1600.webp" srcset="/assets/img/ride-atlantic-900.webp 900w, /assets/img/ride-atlantic-1600.webp 1600w" sizes="(max-width: 860px) 100vw, 50vw" alt="Guests riding a golf cart and Moke through Delray Beach" loading="lazy"></div>
      <div class="reveal" data-delay="1">
        <div class="eyebrow">Events &amp; sales</div>
        <h2>Weddings, shuttles, and carts to keep.</h2>
        <p class="lead">Planning a wedding, corporate outing or block party? We supply fleets of carts and drivers anywhere in Florida. Fell in love with your rental? We sell new and used Gorilla carts and service what we sell.</p>
        <div class="btn-row mt-2">
          <a class="btn btn--primary" href="/events">Event bookings</a>
          <a class="btn btn--ghost" href="/sales">Golf cart sales</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--white" id="faq">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">Good to know</div>
      <h2>Questions, answered.</h2>
    </div>
    <div class="faq reveal">
      <details><summary>Who can drive the cart?<i></i></summary><div class="faq__body"><p>Drivers must be 21 or older with a valid driver's license. The person renting must be 25 or older.</p></div></details>
      <details><summary>Is there a deposit?<i></i></summary><div class="faq__body"><p>Yes. We collect a $250 security deposit at delivery and refund it when the vehicle is returned in the same condition it arrived.</p></div></details>
      <details><summary>Where can I drive?<i></i></summary><div class="faq__body"><p>Our vehicles are registered low-speed vehicles, legal on roads with a posted limit of 35 mph or less. That covers most of Delray Beach and the beach communities we serve. See our <a href="/golf-cart-map">golf cart map</a> for local tips.</p></div></details>
      <details><summary>What is your cancellation policy?<i></i></summary><div class="faq__body"><p>Cancel free of charge up to seven days after booking. Cancellations seven or more days after the booking date incur a 3% processing charge. Full details in our <a href="/refund-policy">refund policy</a>.</p></div></details>
      <details><summary>How do I pay?<i></i></summary><div class="faq__body"><p>All major credit cards are accepted online, or you can pay cash when we deliver.</p></div></details>
      <details><summary>How far can I go on a charge?<i></i></summary><div class="faq__body"><p>Roughly 25 to 35 miles on a full charge, which is plenty for a day around town. Plug it into any standard outlet overnight and it is ready to go again.</p></div></details>
    </div>
  </div>
</section>

{cta_band()}
"""
    return layout(title="Joy Ride | Golf Cart & Moke Rentals in Delray Beach, FL",
                  description="Street-legal six-seat golf cart and electric Moke rentals in Delray Beach, Boca Raton, Boynton Beach and beyond. Free door-to-door delivery. 5-star rated on Google. Reserve online or call (561) 569-2438.",
                  path="/", body=body, over_hero=True)

def page_rentals():
    body = page_hero("Rentals", "Golf carts &amp; Mokes, delivered.", "Choose your ride, pick your dates, and we bring it to your door fully charged. Reserve online or call and we will handle it for you.",
                     image="/assets/img/fleet-beach-1600.webp", alt="Joy Ride golf cart and Moke at the beach")
    body += f"""
<section class="section" id="golf-cart">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media reveal"><img src="/assets/img/cart-beach-1600.webp" alt="Six-seat ICON golf cart on the sand" loading="lazy"></div>
      <div class="reveal" data-delay="1">
        <div class="eyebrow">Six-seat golf cart</div>
        <h2>The signature Joy Ride.</h2>
        <p class="lead">Our lifted ICON six-seater is the cart you see all over Delray. Street legal with every safety feature built in, plus Bluetooth speakers, a backup camera and a roof for the sun. Top speed 25 mph, range 25 to 35 miles.</p>
        <ul class="ride__specs"><li>Seats 6</li><li>Seat belts</li><li>Headlights &amp; taillights</li><li>Hazards &amp; blinkers</li><li>Backup camera</li><li>Bluetooth audio</li></ul>
        <div class="btn-row mt-4"><a class="btn btn--primary" href="{BIZ['book_cart']}" target="_blank" rel="noopener">Reserve a golf cart {ICON_ARROW}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--white" id="moke">
  <div class="container">
    <div class="split-feature split-feature--flip">
      <div class="split-feature__media reveal"><img src="/assets/img/moke-parked-1600.webp" alt="Red electric Moke" loading="lazy"></div>
      <div class="reveal" data-delay="1">
        <div class="eyebrow">Electric Moke</div>
        <h2>The beach classic, gone electric.</h2>
        <p class="lead">Compact, open-top and impossible to miss. The Moke seats four, tops out at 25 mph and is perfect for cruising the beachfront with the sea breeze in your hair.</p>
        <ul class="ride__specs"><li>Seats 4</li><li>Seat belts</li><li>Headlamps</li><li>Hazards &amp; blinkers</li><li>All electric</li><li>Bright colors</li></ul>
        <div class="btn-row mt-4"><a class="btn btn--red" href="{BIZ['book_moke']}" target="_blank" rel="noopener">Reserve a Moke {ICON_ARROW}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand2" id="reserve">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow">Daily rates</div>
      <h2>Pick your dates. Watch the rate drop.</h2>
      <p>Reserve online and pay securely by card, or call us and pay cash at the door.</p>
    </div>
    {rates_block()}
    <div class="req mt-6">
      <div class="req__item reveal" data-delay="1"><span>Driver age</span><b>21+</b></div>
      <div class="req__item reveal" data-delay="2"><span>Renter age</span><b>25+</b></div>
      <div class="req__item reveal" data-delay="3"><span>Deposit</span><b>$250 refundable</b></div>
      <div class="req__item reveal" data-delay="4"><span>Delivery</span><b>Free</b></div>
    </div>
  </div>
</section>
{reviews_block("Five stars, every time.")}
{cta_band()}
"""
    return layout(title="Golf Cart & Moke Rentals | Rates & Reservations | Joy Ride Delray Beach",
                  description="Rent a street-legal six-seat golf cart from $140/day or an electric Moke from $140/day in Delray Beach. Free delivery, refundable deposit, reserve online.",
                  path="/rentals", body=body, over_hero=True)

def page_locations():
    body = page_hero("Locations", "Eight beach towns, one Joy Ride.", "We started on Atlantic Avenue in Delray Beach and now deliver carts in beach towns from Florida to Long Island. Find your town below.")
    body += f"""
<section class="section">
  <div class="container">
    {locations_grid()}
    <p class="muted small mt-4 reveal">Not sure if we deliver to your address? Call or text <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a> and we will tell you in a minute.</p>
  </div>
</section>
<section class="section section--white">
  <div class="container">
    <div class="split-feature">
      <div class="reveal">
        <div class="eyebrow">Headquarters</div>
        <h2>Delray Beach, Florida.</h2>
        <p class="lead">{BIZ['address']}. Free delivery throughout Delray Beach, Boca Raton, Boynton Beach, Highland Beach and Gulf Stream.</p>
        <ul class="contact-list mt-4">
          <li>{ICON_PHONE}<div><span>Call or text</span><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
          <li>{ICON_MAIL}<div><span>Email</span><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
        </ul>
      </div>
      <div class="map-embed reveal" data-delay="1"><iframe title="Map of Joy Ride Delray Beach" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Joy+Ride+Delray+Beach+Golf+Cart+Rentals,+820+E+Atlantic+Ave,+Delray+Beach,+FL+33483&z=14&output=embed"></iframe></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Locations | Golf Cart Rentals in Delray Beach, Palm Beach, Jacksonville, Charleston, Montauk & More | Joy Ride",
                  description="Joy Ride delivers golf carts and Mokes in Delray Beach, Palm Beach, Ft Lauderdale/Pompano, Vero Beach, Jacksonville, Dewey/Rehoboth Beach, Charleston and Montauk.",
                  path="/locations", body=body)

def page_events():
    body = page_hero("Event bookings", "Carts for the big day.", "Weddings, corporate outings, festivals and shuttles. With locations around Florida we can cater your event wherever and whenever you need it.",
                     image="/assets/img/ride-atlantic-1600.webp", alt="Golf cart and Moke driving through Delray Beach")
    body += f"""
<section class="section">
  <div class="container">
    <div class="trio">
      <div class="trio__item reveal" data-delay="1"><h3>Weddings</h3><p>Move guests between the ceremony, photos and the reception in style. Decorated carts on request.</p></div>
      <div class="trio__item reveal" data-delay="2"><h3>Corporate &amp; festivals</h3><p>Fleets of carts to shuttle attendees from parking to the venue, with or without drivers.</p></div>
      <div class="trio__item reveal" data-delay="3"><h3>Private parties</h3><p>Birthdays, bachelor and bachelorette weekends, family reunions. Let everyone shuttle themselves in style.</p></div>
    </div>
    <div class="section-head mt-6 reveal">
      <h2>Tell us about your event.</h2>
      <p>Send the date, location and a rough head count and we will come back with a quote, usually the same day.</p>
      <div class="btn-row mt-2">
        <a class="btn btn--primary" href="mailto:{BIZ['email']}?subject=Event%20booking%20quote">Email for a quote {ICON_ARROW}</a>
        <a class="btn btn--ghost" href="tel:{BIZ['phone_tel']}">Call {BIZ['phone_display']}</a>
      </div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Event Bookings | Golf Cart Fleets for Weddings & Events | Joy Ride",
                  description="Golf cart fleets and shuttles for weddings, corporate events and private parties across Florida. Contact Joy Ride for a quote.",
                  path="/events", body=body, over_hero=True)

def page_sales():
    body = page_hero("Golf cart sales", "Own the Joy Ride.", "Purchase your new or used luxury street-legal golf cart today. We stock Gorilla carts and, because we run them in our own fleet, we are the people who will look after yours.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media reveal"><img src="/assets/img/gorilla-cart-900.webp" alt="Gorilla street-legal golf cart" loading="lazy"></div>
      <div class="reveal" data-delay="1">
        <div class="eyebrow">Gorilla carts</div>
        <h2>Bought from people who drive them every day.</h2>
        <p class="lead">The question we like to answer is: who is going to be there for you after you purchase, when something goes wrong? We operate a fleet of Gorilla carts, so taking care of yours is no hassle.</p>
        <ul class="ride__specs"><li>New &amp; used inventory</li><li>Street legal, titled</li><li>Local service &amp; parts</li><li>Delivery available</li></ul>
        <div class="btn-row mt-4">
          <a class="btn btn--primary" href="mailto:{BIZ['email']}?subject=Golf%20cart%20sales%20inquiry">Ask about inventory {ICON_ARROW}</a>
          <a class="btn btn--ghost" href="tel:{BIZ['phone_tel']}">Call {BIZ['phone_display']}</a>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Golf Cart Sales | New & Used Gorilla Carts in Delray Beach | Joy Ride",
                  description="Buy a new or used street-legal Gorilla golf cart in Delray Beach from the team that runs them daily. Local service and support included.",
                  path="/sales", body=body)

def page_contact():
    body = page_hero("Contact", "Say hello.", "Questions, quotes or a last-minute booking: call, text or email us any time and a real person will get back to you.")
    body += f"""
<section class="section">
  <div class="container contact-grid">
    <div class="contact-card reveal">
      <ul class="contact-list">
        <li>{ICON_PHONE}<div><span>Call or text</span><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
        <li>{ICON_MAIL}<div><span>Email</span><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
        <li>{ICON_PIN}<div><span>Headquarters</span><b>{BIZ['address']}</b></div></li>
        <li>{ICON_CLOCK}<div><span>Hours</span><b>7 days a week</b></div></li>
      </ul>
      <div class="btn-row mt-4">
        <a class="btn btn--primary" href="/rentals#reserve">Reserve a ride {ICON_ARROW}</a>
        <a class="gbadge gbadge--dark" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> on Google</span></a>
      </div>
    </div>
    <div class="map-embed reveal" data-delay="1"><iframe title="Map of Joy Ride Delray Beach" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Joy+Ride+Delray+Beach+Golf+Cart+Rentals,+820+E+Atlantic+Ave,+Delray+Beach,+FL+33483&z=15&output=embed"></iframe></div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Contact Joy Ride | Golf Cart Rentals Delray Beach",
                  description="Contact Joy Ride golf cart rentals in Delray Beach. Call or text (561) 569-2438 or email rentals@joyridedelray.com.",
                  path="/contact", body=body)

def page_map():
    body = page_hero("Delray Beach golf cart map", "Where to ride in Delray.", "Our carts are registered low-speed vehicles, legal on roads posted 35 mph or under. That covers the beach, Atlantic Avenue, Pineapple Grove and most of the neighborhoods in between.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="map-embed map-embed--wide reveal"><iframe title="Delray Beach map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Delray+Beach,+FL&z=14&output=embed"></iframe></div>
    <div class="trio mt-6">
      <div class="trio__item reveal" data-delay="1"><h3>Go</h3><p>Atlantic Avenue, A1A along the beach, Pineapple Grove, the Marina District, Lake Ida and the residential streets east of I-95.</p></div>
      <div class="trio__item reveal" data-delay="2"><h3>Avoid</h3><p>I-95, sidewalks, and any road with a posted limit above 35 mph. Watch for signage on Federal Highway and Linton Boulevard.</p></div>
      <div class="trio__item reveal" data-delay="3"><h3>Park</h3><p>Any standard car space. The beach lots on A1A and the garages off Atlantic all work. Plug in overnight at home.</p></div>
    </div>
    <p class="muted small mt-4 reveal">Rules of the road change. Always follow posted signage, and ask us for the latest route tips when we deliver.</p>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Delray Beach Golf Cart Map | Where You Can Drive | Joy Ride",
                  description="Where you can drive a street-legal golf cart in Delray Beach: the beach, Atlantic Avenue, Pineapple Grove and more. Tips from Joy Ride.",
                  path="/golf-cart-map", body=body)

def page_affiliate():
    body = page_hero("Affiliates", "Earn with every referral.", "Hotels, vacation rental hosts, concierges and locals: send guests our way and earn on every booking through our affiliate program.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <p class="lead">Sign up in a couple of minutes, get a personal link, and track referrals and payouts in your dashboard.</p>
      <div class="btn-row mt-2">
        <a class="btn btn--primary" href="{BIZ['affiliate']}" target="_blank" rel="noopener">Join the affiliate program {ICON_ARROW}</a>
        <a class="btn btn--ghost" href="mailto:{BIZ['email']}?subject=Affiliate%20program">Ask a question</a>
      </div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Become an Affiliate | Joy Ride Delray Beach",
                  description="Refer guests to Joy Ride golf cart rentals and earn on every booking. Join the affiliate program.",
                  path="/affiliate", body=body)

def page_refund():
    body = page_hero("Policies", "Refund policy.", "Plain-English terms for cancellations and refunds.")
    body += f"""
<section class="section">
  <div class="container prose reveal">
    <h2>Refunds</h2>
    <p>All refunds for bookings are at no cost until seven days after the booking date. Seven days or more after the booking date any cancellations will incur a 3% charge.</p>
    <p>We will notify you once we've received and inspected your return, and let you know if the refund was approved or not. If approved, you'll be automatically refunded on your original payment method within 10 business days. Please remember it can take some time for your bank or credit card company to process and post the refund too.</p>
    <p>If more than 15 business days have passed since we've approved your return, please contact us at <a href="mailto:mbrauser@joyridedelray.com">mbrauser@joyridedelray.com</a>.</p>
  </div>
</section>
"""
    return layout(title="Refund Policy | Joy Ride", description="Joy Ride golf cart rental refund and cancellation policy.", path="/refund-policy", body=body)

def page_terms():
    frag = open(os.path.join(ROOT, "tools", "content", "terms-fragment.html"), encoding="utf-8").read()
    body = page_hero("Policies", "Terms of service.", "Last updated November 27, 2022.")
    body += f"""
<section class="section">
  <div class="container prose">
    {frag}
  </div>
</section>
"""
    return layout(title="Terms of Service | Joy Ride", description="Terms of service for the Joy Ride website and rentals.", path="/terms-of-service", body=body)

def page_brand():
    body = page_hero("Brand", "Logo concepts.", "The original wordmark, traced into clean vector art, with three ways to finish it. Every file here is an SVG that scales to any size.")
    body += """
<section class="section">
  <div class="container">
    <div class="brand-grid">
      <div class="brand-card reveal" data-delay="1"><img src="/assets/logo/joyride-classic.svg" alt="Classic logo"><h3>A. Classic, cleaned</h3><p>Same layout as today. The palm trees are redrawn as clean vector silhouettes with no watermark, and the wordmark is traced from the original so the letterforms are unchanged.</p></div>
      <div class="brand-card reveal" data-delay="2"><img src="/assets/logo/joyride-wheel.svg" alt="Wheel logo"><h3>B. The wheel O</h3><p>The O in JOY becomes an off-road cart wheel: tire, rim and five spokes. It reads as “Joy Ride” instantly and works small, as a favicon or embroidered on a polo.</p></div>
      <div class="brand-card reveal" data-delay="3"><img src="/assets/logo/joyride-crest.svg" alt="Crest logo"><h3>C. The crest</h3><p>Palms and a wheel on the horizon line, sitting above the wordmark. Used for the site header lockup and the favicon.</p></div>
    </div>
    <div class="brand-grid mt-4">
      <div class="brand-card reveal"><img src="/assets/logo/joyride-lockup.svg" alt="Horizontal lockup"><h3>Horizontal lockup</h3><p>Header and footer version.</p></div>
      <div class="brand-card brand-card--dark reveal" data-delay="1"><img src="/assets/logo/joyride-lockup-white.svg" alt="Horizontal lockup, white"><h3>Reversed</h3><p>For photos and blue backgrounds.</p></div>
      <div class="brand-card reveal" data-delay="2"><img src="/assets/logo/joyride-mark.svg" alt="Mark" style="max-width:200px;margin:auto"><h3>Mark &amp; favicon</h3><p>Stands alone for social avatars and app icons.</p></div>
    </div>
  </div>
</section>
"""
    return layout(title="Brand | Joy Ride", description="Joy Ride logo concepts.", path="/brand", body=body, noindex=True)

def page_404():
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="eyebrow">404</div>
    <h1 class="split">Wrong turn.</h1>
    <p class="lead">That page has rolled off the map. Head back home or give us a call.</p>
    <div class="btn-row mt-4"><a class="btn btn--primary" href="/">Back home</a><a class="btn btn--ghost" href="tel:{BIZ['phone_tel']}">Call {BIZ['phone_display']}</a></div>
  </div>
</section>
"""
    return layout(title="Page not found | Joy Ride", description="Page not found.", path="/404", body=body, noindex=True)

PAGES = {
    "index.html": page_home,
    "rentals.html": page_rentals,
    "locations.html": page_locations,
    "events.html": page_events,
    "sales.html": page_sales,
    "contact.html": page_contact,
    "golf-cart-map.html": page_map,
    "affiliate.html": page_affiliate,
    "refund-policy.html": page_refund,
    "terms-of-service.html": page_terms,
    "brand.html": page_brand,
    "404.html": page_404,
}

def write_sitemap():
    urls = ["/", "/rentals", "/locations", "/events", "/sales", "/contact", "/golf-cart-map", "/affiliate", "/refund-policy", "/terms-of-service"]
    today = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f"  <url><loc>{SITE_URL}{'' if u == '/' else u}</loc><lastmod>{today}</lastmod></url>")
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /brand\nSitemap: {SITE_URL}/sitemap.xml\n")

def main():
    for name, fn in PAGES.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
    write_sitemap()
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    main()
