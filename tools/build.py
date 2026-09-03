#!/usr/bin/env python3
"""
Joy Ride static site generator.

Every page in the site root is generated from the templates below so that the
header, footer, meta tags and JSON-LD stay identical across pages.

    python3 tools/build.py

Edit content here (or in tools/content/), re-run, commit the generated HTML.
"""
import os, html, datetime, hashlib

def asset(path):
    """Append a content hash so browsers and CDNs never serve a stale copy after a deploy."""
    full = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path.lstrip("/"))
    try:
        h = hashlib.md5(open(full, "rb").read()).hexdigest()[:10]
    except OSError:
        return path
    return f"{path}?v={h}"

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

STD_CART = [250, 190, 180, 170, 160, 150, 140]
STD_MOKE = [300, 200, 190, 170, 160, 150, 140]
TIER_LABELS = ["1 day", "2 days", "3 days", "4 to 5 days", "6 days", "7 days", "8+ days"]
DELRAY_STORE = "https://www.joyridedelray.com"

# One entry per location. Each town that runs its own Shopify store books there;
# Vero Beach and Dewey/Rehoboth book through the Delray store.
# rates: list of 7 per-day prices matching TIER_LABELS, or a single-item list
# when only the one-day price is published (the table then says "call").
LOCATIONS = [
    {"slug": "delray-beach", "shop": "joy-ride-1689.myshopify.com", "city": "Delray Beach", "short": "Delray", "state": "FL", "hq": True,
     "blurb": "Our home base on Atlantic Avenue, and the biggest fleet.",
     "areas": ["Delray Beach", "Boca Raton", "Boynton Beach", "Highland Beach", "Gulf Stream"],
     "phone": "(561) 569-2438", "tel": "+15615692438", "store": DELRAY_STORE, "site": None,
     "map": "Delray Beach, FL",
     "cart": {"url": DELRAY_STORE + "/products/one-day-golf-cart-rental", "rates": STD_CART},
     "moke": {"url": DELRAY_STORE + "/products/electric-mini-moke", "rates": STD_MOKE},
     "hourly": {"url": DELRAY_STORE + "/products/marriott-golf-cart-rental", "rates": [("2 hours", 125), ("4 hours", 150), ("6 hours", 200), ("8 hours", 250), ("10 hours", 300)]},
     "addons": [("Car seat add-on", 15, DELRAY_STORE + "/products/car-seat-add-on"), ("Damage waiver", 12, DELRAY_STORE + "/products/golf-cart-rental-liability-insurance")],
     "notes": []},
    {"slug": "palm-beach", "shop": "ef890a-8a.myshopify.com", "city": "Palm Beach", "short": "Palm Beach", "state": "FL",
     "blurb": "Island cruising from Worth Avenue to the Lake Trail.",
     "areas": ["Palm Beach", "West Palm Beach"],
     "phone": "(561) 562-7152", "tel": "+15615627152", "store": "https://www.joyridepalmbeach.com", "site": "https://www.joyridepalmbeach.com",
     "map": "Palm Beach, FL",
     "cart": {"url": "https://www.joyridepalmbeach.com/products/copy-of-golf-cart-rental-palm-beach", "rates": STD_CART,
              "extras": "Touchscreen with Apple CarPlay, Bluetooth speakers, lithium batteries, LED lights"},
     "moke": {"url": "https://www.joyridepalmbeach.com/products/moke-rental", "rates": [300]},
     "hourly": None, "addons": [("Damage waiver", 12, "https://www.joyridepalmbeach.com/products/golf-cart-rental-damage-waiver")],
     "notes": ["Ask about special event and university partnership pricing."]},
    {"slug": "pompano-beach", "shop": "16kswt-bw.myshopify.com", "city": "Pompano & Ft Lauderdale", "short": "Pompano", "state": "FL",
     "blurb": "Beach-to-boardwalk rides along the A1A corridor in Broward County.",
     "areas": ["Pompano Beach", "Fort Lauderdale", "Lauderdale-by-the-Sea", "Deerfield Beach"],
     "phone": "(561) 569-2438", "tel": "+15615692438", "store": "https://joyridepompanobeach.com", "site": "https://joyridepompanobeach.com",
     "map": "Pompano Beach, FL",
     "cart": {"url": "https://joyridepompanobeach.com/products/luxury-6-passenger-golf-cart-rental", "rates": STD_CART,
              "extras": "Speakers with touchscreen display"},
     "moke": {"url": "https://joyridepompanobeach.com/products/electric-mini-moke", "rates": [250]},
     "hourly": None, "addons": [("Damage waiver", 12, "https://joyridepompanobeach.com/products/golf-cart-rental-damage-waiver")],
     "notes": ["Free delivery within our Broward delivery range. Outside it, call for a quote."]},
    {"slug": "vero-beach", "shop": "joy-ride-1689.myshopify.com", "city": "Vero Beach", "short": "Vero", "state": "FL",
     "blurb": "Ocean Drive, the beachside village and quiet Treasure Coast streets.",
     "areas": ["Vero Beach", "Indian River Shores"],
     "phone": "(561) 569-2438", "tel": "+15615692438", "store": DELRAY_STORE, "site": None,
     "map": "Vero Beach, FL",
     "cart": {"url": DELRAY_STORE + "/products/one-day-golf-cart-rental", "rates": STD_CART},
     "moke": {"url": DELRAY_STORE + "/products/electric-mini-moke", "rates": STD_MOKE},
     "hourly": None, "addons": [("Damage waiver", 12, DELRAY_STORE + "/products/golf-cart-rental-liability-insurance")],
     "notes": ["Vero Beach rentals are booked through our Delray Beach store. Enter your Vero Beach delivery address at checkout, or call and we will set it up."]},
    {"slug": "jacksonville", "shop": "c296af-46.myshopify.com", "city": "Jacksonville & St. Augustine", "short": "Jacksonville", "state": "FL",
     "blurb": "Jax Beach, Ponte Vedra and St. Augustine with same-day delivery.",
     "areas": ["Jacksonville Beach", "Neptune Beach", "Atlantic Beach", "Ponte Vedra", "St. Augustine"],
     "phone": "(904) 834-9466", "tel": "+19048349466", "store": "https://joyridejacksonville.com", "site": "https://joyridejacksonville.com",
     "map": "Jacksonville Beach, FL",
     "cart": {"url": "https://joyridejacksonville.com/products/golf-cart-rental-jacksonville", "rates": [299, 190, 180, 170, 160, 150, 140], "range": "15 to 25 miles"},
     "moke": {"url": "https://joyridejacksonville.com/products/electric-moke-rental", "rates": [350, 225, 215, 200, 180, 160, 150]},
     "hourly": None,
     "weekly": {"label": "St. Augustine weekly golf cart", "price": 1680, "url": "https://joyridejacksonville.com/products/golf-cart-rental-st-augustine"},
     "addons": [("Damage waiver", 12, "https://joyridejacksonville.com/products/golf-cart-rental-damage-waiver")],
     "notes": ["Three-day minimum on holiday weekends.", "Same-day delivery available across the Jax Beach area."]},
    {"slug": "rehoboth-beach", "shop": "joy-ride-1689.myshopify.com", "city": "Dewey & Rehoboth Beach", "short": "Rehoboth", "state": "DE",
     "blurb": "Summer on the Delaware shore, from the boardwalk to the bay.",
     "areas": ["Rehoboth Beach", "Dewey Beach"],
     "phone": "(561) 569-2438", "tel": "+15615692438", "store": DELRAY_STORE, "site": None,
     "map": "Rehoboth Beach, DE",
     "cart": {"url": DELRAY_STORE + "/products/one-day-golf-cart-rental", "rates": STD_CART},
     "moke": {"url": DELRAY_STORE + "/products/electric-mini-moke", "rates": STD_MOKE},
     "hourly": None, "addons": [("Damage waiver", 12, DELRAY_STORE + "/products/golf-cart-rental-liability-insurance")],
     "notes": ["Delaware rentals are booked through our Delray Beach store. Enter your Dewey or Rehoboth delivery address at checkout, or call and we will set it up."]},
    {"slug": "charleston", "shop": "zpbfxf-2z.myshopify.com", "city": "Charleston", "short": "Charleston", "state": "SC",
     "blurb": "Downtown Charleston and the Isle of Palms in Lowcountry style.",
     "areas": ["Downtown Charleston", "Isle of Palms"],
     "phone": "(843) 905-2495", "tel": "+18439052495", "store": "https://joyridecharleston.com", "site": "https://joyridecharleston.com",
     "map": "Charleston, SC",
     "cart": {"url": "https://joyridecharleston.com/products/one-day-golf-cart-rental", "rates": STD_CART},
     "moke": None, "hourly": None,
     "addons": [("Damage waiver", 12, "https://joyridecharleston.com/products/golf-cart-rental-damage-waiver"), ("Isle of Palms delivery", 250, "https://joyridecharleston.com/products/delivery-isle-of-palms")],
     "notes": ["Free delivery in downtown Charleston. Isle of Palms delivery is $250 round trip."]},
    {"slug": "montauk", "shop": "k43z9t-dq.myshopify.com", "city": "Montauk", "short": "Montauk", "state": "NY",
     "blurb": "The End of Long Island, from Ditch Plains to the harbor.",
     "areas": ["Montauk"],
     "phone": "(631) 430-6653", "tel": "+16314306653", "store": "https://joyridemontauk.com", "site": "https://joyridemontauk.com",
     "map": "Montauk, NY",
     "cart": {"url": "https://joyridemontauk.com/products/one-day-golf-cart-rental", "rates": STD_CART},
     "moke": {"url": "https://joyridemontauk.com/products/electric-mini-moke", "rates": STD_MOKE},
     "hourly": None, "addons": [("Damage waiver", 12, "https://joyridemontauk.com/products/golf-cart-rental-damage-waiver")],
     "notes": []},
]
LOC = {l["slug"]: l for l in LOCATIONS}


REVIEWS = [
    ("Christos L.", "Sep 2025", "The process was quick, smooth, and hassle-free from start to finish. The staff was professional, friendly, and very accommodating."),
    ("Lisa S.", "Apr 2025", "Both Matt and Dan were so easy to deal with. Professional and efficient with the process. A seamless process."),
    ("Jonathan H.", "Jan 2025", "It was in perfect condition, packed with great features like a backup camera and speakers. The staff was super helpful and friendly."),
    ("Mark M.", "Nov 2024", "The thing about the golf cart is you get all the fresh air with some protection from the sun. In great shape and had many unexpected extras."),
    ("Ye S.", "Sep 2023", "I got a brand-new one with a backup camera, touchscreen and really good range. They were so friendly and this was such a fun experience."),
]

NAV = [("Rent", "/rentals"), ("Locations", "/locations"), ("Events", "/events"), ("Sales", "/sales"), ("Contact", "/contact")]

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
ICON_INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>'
ICON_CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
ICON_CARD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="1.5"/><path d="M2.5 9.5h19M6 15h4"/></svg>'

def stars(n=5):
    return "★" * n

# ----------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------
def locswitch(current=None, inplace=False):
    cur = LOC.get(current) if current else None
    label = cur["short"] if cur else "Choose location"
    items = ""
    for l in LOCATIONS:
        cur_attr = ' aria-current="true"' if cur and cur["slug"] == l["slug"] else ""
        inplace_attr = " data-inplace" if inplace else ""
        items += ('<a href="/%s" data-loc="%s" data-name="%s"%s%s><span>%s</span><small>%s</small></a>'
                  % (l["slug"], l["slug"], html.escape(l["short"]), inplace_attr, cur_attr, html.escape(l["city"]), l["state"]))
    return (f'<div class="locswitch" data-current="{current or ""}">'
            f'<button class="locswitch__btn" aria-haspopup="true" aria-expanded="false">{ICON_PIN}<span data-loc-label>{html.escape(label)}</span>{ICON_CHEV}</button>'
            f'<div class="locswitch__menu">{items}<a class="locswitch__all" href="/locations">All locations</a></div></div>')

def jsonld_for(location=None):
    """Home and inner pages describe the Delray Beach business, whose address and Google
    rating we can verify. A location page describes that town's service only: its own
    phone and delivery area, no borrowed street address and no borrowed review count."""
    if location:
        l = LOC[location]
        return {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": f"Joy Ride {l['city']} Golf Cart Rentals",
            "parentOrganization": {"@type": "LocalBusiness", "name": BIZ["name"], "url": SITE_URL},
            "image": SITE_URL + "/assets/img/og-image.jpg",
            "url": f"{SITE_URL}/{l['slug']}",
            "telephone": l["tel"],
            "email": BIZ["email"],
            "priceRange": "$$",
            "areaServed": [{"@type": "Place", "name": f"{a}, {l['state']}"} for a in l["areas"]],
            "sameAs": [l["site"]] if l.get("site") else [],
        }
    return {
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

FAQ = [
    ("Who can drive the cart?", "Drivers must be 21 or older with a valid driver's license. The person renting must be 25 or older."),
    ("Is there a deposit?", "Yes. We collect a $250 security deposit at delivery and refund it when the vehicle is returned in the same condition it arrived."),
    ("Why do rates differ by town?", "Each location runs its own fleet with its own costs, so a few towns price a little differently. Pick your location above to see that town's numbers, and the reserve button opens that town's checkout."),
    ("Where can I drive?", "Our vehicles are registered low-speed vehicles, legal on roads with a posted limit of 35 mph or less. That covers most of the beach communities we serve. See our <a href=\"/golf-cart-map\">Delray Beach golf cart map</a> for local tips."),
    ("What is your cancellation policy?", "Cancel free of charge up to seven days after booking. Cancellations seven or more days after the booking date incur a 3% processing charge. Full details are in our <a href=\"/refund-policy\">refund policy</a>."),
    ("How do I pay?", "All major credit cards are accepted online, or you can pay cash when we deliver."),
]

def faq_jsonld():
    import re
    strip = lambda t: re.sub(r"<[^>]+>", "", t)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ]}

def layout(*, title, description, path, body, over_hero=False, noindex=False, extra_head="", location=None, inplace=False):
    canonical = SITE_URL + ("" if path == "/" else path)
    nav_links = ""
    for label, href in NAV:
        current = ' aria-current="page"' if href == path else ""
        nav_links += '<a class="nav__link" href="%s"%s>%s</a>' % (href, current, label)
    header_cls = "header header--over" if over_hero else "header"
    year = datetime.date.today().year
    location_links = "".join(f'          <li><a href="/{l["slug"]}">{html.escape(l["city"])}</a></li>\n' for l in LOCATIONS)
    jsonld = jsonld_for(location)
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
<link rel="icon" href="{asset("/assets/logo/favicon.svg")}" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/logo/apple-touch-icon.png">
<link rel="preload" href="{asset("/assets/fonts/Italiana-Regular.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset("/assets/fonts/Jost-400.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset("/assets/css/style.css")}">
{extra_head}
<script type="application/ld+json">{json.dumps(jsonld, indent=0)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><span>Call or text to reserve: <a href="tel:{(LOC[location]['tel'] if location else BIZ['phone_tel'])}">{(LOC[location]['phone'] if location else BIZ['phone_display'])}</a></span><span class="topbar__extra">Free door-to-door delivery</span></div>
<header class="{header_cls}">
  <div class="container header__inner">
    <a class="brand" href="/" aria-label="Joy Ride home">
      <img class="brand__dark" src="{asset("/assets/logo/joyride-wordmark.svg")}" alt="Joy Ride" width="129" height="30">
      <img class="brand__light" src="{asset("/assets/logo/joyride-wordmark-white.svg")}" alt="Joy Ride" width="129" height="30">
    </a>
    {locswitch(location, inplace)}
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
    <div class="footer__grid footer__grid--5">
      <div class="footer__brand">
        <img src="/assets/logo/joyride-wordmark-white.svg" alt="Joy Ride" width="146" height="34">
        <p>Street-legal golf cart and electric Moke rentals, delivered free to your door in eight beach towns.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/rentals">Golf cart and Moke rentals</a></li>
          <li><a href="/locations">Locations</a></li>
          <li><a href="/events">Event bookings</a></li>
          <li><a href="/sales">Golf cart sales</a></li>
          <li><a href="/golf-cart-map">Delray Beach golf cart map</a></li>
          <li><a href="/affiliate">Affiliate program</a></li>
        </ul>
      </div>
      <div>
        <h4>Locations</h4>
        <ul>
{location_links}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/contact">Contact</a></li>
          <li><a href="{BIZ['google_reviews']}" target="_blank" rel="noopener">Google reviews</a></li>
          <li><a href="/refund-policy">Refund policy</a></li>
          <li><a href="/terms-of-service">Terms of service</a></li>
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
      <span>© <span data-year>{year}</span> Joy Ride, MB Meadows LLC</span>
      <span>Golf cart and Moke rentals in eight beach towns</span>
    </div>
  </div>
</footer>
<div class="modal" aria-hidden="true" role="dialog" aria-label="Joy Ride video">
  <button class="modal__close" aria-label="Close video">×</button>
  <div class="modal__box"><iframe title="Joy Ride Golf Cart Rentals video" src="" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
</div>
<script src="{asset("/assets/js/main.js")}" defer></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------
# Reusable blocks
# ----------------------------------------------------------------------------
def rate_table(prices, per="per day"):
    """Seven tiers on desktop. On phones the middle tiers sit behind a "Show all rates"
    button so a location panel does not run to three screens of table."""
    out = ['<table class="rate-table">']
    if len(prices) == 1:
        out.append(f"<tr><td>1 day</td><td>${prices[0]}<small>{per}</small></td></tr>")
        out.append('<tr><td>Multi-day</td><td class="rate-table__call">Call for rates</td></tr>')
        out.append("</table>")
        return "\n".join(out)
    last = len(prices) - 1
    for i, (label, price) in enumerate(zip(TIER_LABELS, prices)):
        classes = []
        if i == last: classes.append("is-best")
        if 0 < i < last - 1: classes.append("rate-table__more")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        out.append(f"<tr{cls}><td>{label}</td><td>${price}<small>{per}</small></td></tr>")
    out.append("</table>")
    out.append('<button class="rate-toggle" type="button" aria-expanded="false">Show all rates</button>')
    return "\n".join(out)

def note(text):
    return f'<div class="note">{ICON_INFO}<span>{html.escape(text)}</span></div>'

def location_panel(l, active=False):
    cards = []
    cards.append(f"""<div class="rate-card">
    <h3>Golf cart <span>Seats six, street legal</span></h3>
    {rate_table(l['cart']['rates'])}
    <p class="rate-note">Prices are per day. Refundable $250 security deposit at delivery.{' ' + html.escape(l['cart']['extras']) + '.' if l['cart'].get('extras') else ''}</p>
    <a class="btn btn--primary rate-cta" href="{l['cart']['url']}" target="_blank" rel="noopener">Reserve a golf cart</a>
  </div>""")
    if l.get("moke"):
        cards.append(f"""<div class="rate-card">
    <h3>Electric Moke <span>Seats four, open top</span></h3>
    {rate_table(l['moke']['rates'])}
    <p class="rate-note">Prices are per day. Refundable $250 security deposit at delivery.</p>
    <a class="btn btn--red rate-cta" href="{l['moke']['url']}" target="_blank" rel="noopener">Reserve a Moke</a>
  </div>""")
    else:
        cards.append(f"""<div class="rate-card rate-card--muted unavailable">
    <h3>Electric Moke <span>Not in this fleet</span></h3>
    <p class="rate-note">Mokes are not currently available in {html.escape(l['city'])}. Our six-seat golf carts are ready to go, or check our Florida and Montauk locations for a Moke.</p>
  </div>""")
    if l.get("hourly"):
        rows = "".join(f"<tr><td>{lbl}</td><td>${p}</td></tr>" for lbl, p in l["hourly"]["rates"])
        cards.append(f"""<div class="rate-card">
    <h3>Golf cart by the hour <span>Same day</span></h3>
    <table class="rate-table">{rows}</table>
    <p class="rate-note">For an afternoon on the Avenue.</p>
    <a class="btn btn--ghost rate-cta" href="{l['hourly']['url']}" target="_blank" rel="noopener">Book by the hour</a>
  </div>""")
    if l.get("weekly"):
        w = l["weekly"]
        cards.append(f"""<div class="rate-card">
    <h3>{html.escape(w['label'])} <span>Seven days</span></h3>
    <table class="rate-table"><tr class="is-best"><td>Weekly</td><td>${w['price']:,}<small>per week</small></td></tr></table>
    <p class="rate-note">Six-seat cart delivered to St. Augustine for the week.</p>
    <a class="btn btn--ghost rate-cta" href="{w['url']}" target="_blank" rel="noopener">Reserve weekly</a>
  </div>""")
    three = " rates--three" if len(cards) > 2 else ""
    addons = ", ".join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(n)} ${p}</a>' for n, p, u in l.get("addons", []))
    notes = "".join(note(n) for n in l.get("notes", []))
    areas = "".join(f"<span>{html.escape(a)}</span>" for a in l["areas"])
    return f"""<div class="locpanel{' is-active' if active else ''}" data-loc="{l['slug']}" data-name="{html.escape(l['short'])}">
  <div class="locpanel__head">
    <div><h3>{html.escape(l['city'])}, {l['state']}</h3><p>{html.escape(l['blurb'])} Free delivery to {html.escape(", ".join(l["areas"]))}.</p></div>
    <a class="locpanel__phone" href="tel:{l['tel']}">{l['phone']}</a>
  </div>
  <div class="rates{three}">{"".join(cards)}</div>
  <div class="notes">{notes}{note("Optional add-ons: " + ", ".join(f"{n} ${p}" for n, p, u in l.get("addons", [])) + ".") if l.get("addons") else ""}</div>
  <p class="small muted mt-2">Reservations open in our {html.escape(l['city'])} online store. Pay by card online or cash at the door. Drivers must be 21 or older, renters 25 or older.</p>
</div>"""

def location_pills(scroll="#rates", hero=False):
    pills = "".join(f'<a class="pill" href="/{l["slug"]}" data-loc="{l["slug"]}" data-scroll="{scroll}">{html.escape(l["short"])}<small>{l["state"]}</small></a>' for l in LOCATIONS)
    return f'<div class="pills{" pills--hero" if hero else ""}">{pills}</div>'

def all_panels():
    return "".join(location_panel(l, active=(i == 0)) for i, l in enumerate(LOCATIONS))


def locations_json():
    import json
    data = {l["slug"]: {"name": l["city"], "short": l["short"], "shop": l["shop"], "phone": l["phone"], "tel": l["tel"]} for l in LOCATIONS}
    return f'<script type="application/json" id="joyride-locations">{json.dumps(data)}</script>'

def availability_section(l=None, sand=False):
    """Date search backed by the booking system: pick dates, see what is free, reserve."""
    loc = l or LOC["delray-beach"]
    return f"""
<section class="section{' section--sand2' if sand else ''} avail" id="availability" data-loc="{loc['slug']}">
  <div class="container">
    <div class="section-head">
      <h2>Check availability</h2>
      <p>Pick your dates and see which vehicles are free in <span data-loc-name>{html.escape(loc['city'])}</span>. Prices update for the length of your rental.</p>
    </div>
    <form class="avail__form" novalidate>
      <label class="avail__field"><span>Start day</span><input type="date" name="start" required></label>
      <label class="avail__field"><span>End day</span><input type="date" name="end" required></label>
      <button class="btn btn--primary avail__go" type="submit">Search</button>
    </form>
    <p class="avail__msg" aria-live="polite"></p>
    <div class="avail__results" aria-live="polite"></div>
  </div>
  {locations_json()}
</section>"""

def rates_section(title="Rates by location", sand=True):
    return f"""
<section class="section{' section--sand2' if sand else ''}" id="rates">
  <div class="container">
    <div class="section-head">
      <h2>{title}</h2>
      <p>Each town runs its own fleet, so pricing and availability differ a little. Choose yours and the reserve buttons open that location's checkout.</p>
    </div>
    {location_pills()}
    <div class="mt-6">{all_panels()}</div>
  </div>
</section>"""

def reviews_block(heading="What renters say on Google"):
    cards = "".join(
        f"""<article class="review">
  <div class="stars" aria-label="5 out of 5 stars">{stars()}</div>
  <p>“{html.escape(text)}”</p>
  <footer><strong>{html.escape(name)}</strong><span>Google, {date}</span></footer>
</article>"""
        for i, (name, date, text) in enumerate(REVIEWS)
    )
    return f"""
<section class="section section--white" id="reviews">
  <div class="container">
    <div class="reviews-head">
      <div class="rating">
        <div class="rating__num">{BIZ['rating']}</div>
        <div class="rating__meta">
          <div class="rating__stars" aria-hidden="true">{stars()}</div>
          <span>{BIZ['review_count']} Google reviews</span>
          <span>Delray Beach, FL</span>
        </div>
      </div>
      <div class="section-head" style="margin-bottom:0">
        <h2>{heading}</h2>
        <p>Every review below is from our Google Business Profile, quoted as written. Read them all, or tell us how your ride went.</p>
      </div>
    </div>
    <div class="reviews">{cards}</div>
    <div class="reviews-actions">
      <a class="gbadge gbadge--dark" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> Read all {BIZ['review_count']} reviews</span></a>
      <a class="btn btn--ghost" href="{BIZ['google_write_review']}" target="_blank" rel="noopener">Leave a review</a>
    </div>
  </div>
</section>"""

def locations_grid():
    cards = []
    for i, l in enumerate(LOCATIONS):
        links = [f'<a href="/{l["slug"]}">Fleet and rates</a>', f'<a href="tel:{l["tel"]}">{l["phone"]}</a>']
        cards.append(f"""<div class="loc{' loc--hq' if l.get('hq') else ''}">
  <div class="loc__state">{l['state']}</div>
  <h3>{html.escape(l['city'])}</h3>
  <p>{html.escape(l['blurb'])} Delivering to {html.escape(", ".join(l['areas']))}.</p>
  <div class="loc__links">{' '.join(links)}</div>
</div>""")
    return '<div class="locations">' + "\n".join(cards) + "</div>"

def cta_band(l=None):
    l = l or LOC["delray-beach"]
    return f"""
<section class="section section--blue cta-band">
  <div class="container">
    <div>
      <h2>Reserve a cart</h2>
      <p>Book online, or call and we will set it up for you. Free delivery, and you can pay by card online or cash at the door.</p>
    </div>
    <div>
      <a class="cta-band__phone" href="tel:{l['tel']}">{l['phone']}</a>
      <p class="small">Call or text the {html.escape(l['city'])} line</p>
      <div class="btn-row mt-2">
        <a class="btn btn--light" href="{l['cart']['url']}" target="_blank" rel="noopener">Reserve a golf cart</a>
        {f'<a class="btn btn--outline-light" href="{l["moke"]["url"]}" target="_blank" rel="noopener">Reserve a Moke</a>' if l.get('moke') else '<a class="btn btn--outline-light" href="/locations">Other locations</a>'}
      </div>
    </div>
  </div>
</section>"""

def page_hero(eyebrow, title, lead, image=None, alt=""):
    if image:
        return f"""
<section class="page-hero page-hero--image">
  <div class="page-hero__media"><img src="{image}" srcset="{image.replace("-2048.webp", "-1400.webp")} 1400w, {image} 2048w" sizes="100vw" alt="{html.escape(alt)}" fetchpriority="high"></div>
  <div class="container">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""
    return f"""
<section class="page-hero">
  <div class="container">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""

# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_home():
    faq_items = "".join(f'<details><summary>{q}<i></i></summary><div class="faq__body"><p>{a}</p></div></details>' for q, a in FAQ)
    body = f"""
<section class="hero">
  <div class="hero__media">
    <video autoplay muted loop playsinline preload="metadata" poster="{asset("/assets/video/hero-poster.jpg")}" data-anim="{asset("/assets/video/hero.webp")}" aria-label="Joy Ride golf carts and Mokes on the road in Delray Beach">
      <source src="{asset("/assets/video/hero.mp4")}" type="video/mp4">
    </video>
  </div>
  <div class="container hero__content">
    <h1>Live like a local. Take a Joy Ride.</h1>
    <p class="hero__sub">Street-legal six-seat golf carts and open-top electric Mokes, delivered free to your door in eight beach towns from Florida to Montauk.</p>
    <div class="hero__pick">
      <p class="hero__label">Where are you riding?</p>
      {location_pills(scroll="#rates", hero=True)}
    </div>
    <div class="hero__bottom">
      <a class="gbadge" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> {BIZ['review_count']} Google reviews</span></a>
    </div>
  </div>
</section>

<section class="section" id="fleet">
  <div class="container">
    <div class="section-head">
      <h2>Six-seat golf carts and electric Mokes</h2>
      <p>Every vehicle is all-electric, street legal and fitted with seat belts, headlights, turn signals and a backup camera. Top speed 25 mph.</p>
    </div>
    <div class="fleet">
      <article class="ride">
        <div class="ride__media"><img src="/assets/img/cart-beach-1400.webp" srcset="/assets/img/cart-beach-900.webp 900w, /assets/img/cart-beach-1400.webp 1400w, /assets/img/cart-beach-2048.webp 2048w" sizes="(max-width: 760px) 100vw, 50vw" alt="White six-seat golf cart parked on the sand" loading="lazy" width="1400" height="1050"></div>
        <span class="ride__tag">Every location</span>
        <div class="ride__body">
          <div class="ride__title"><h3>Six-seat golf cart</h3><div class="ride__price">$250<small>from, per day</small></div></div>
          <p>Our lifted six-seater, with room for the whole group, Bluetooth speakers and a roof for the midday sun.</p>
          <ul class="ride__specs"><li>Seats six</li><li>25 mph, street legal</li><li>Seat belts and lights</li><li>Backup camera</li></ul>
          <div class="ride__actions">
            <a class="btn btn--primary" href="#rates">See rates by location</a>
            <a class="btn btn--ghost" href="/rentals#golf-cart">Details</a>
          </div>
        </div>
      </article>
      <article class="ride">
        <div class="ride__media"><img src="/assets/img/moke-parked-1400.webp" srcset="/assets/img/moke-parked-900.webp 900w, /assets/img/moke-parked-1400.webp 1400w, /assets/img/moke-parked-2048.webp 2048w" sizes="(max-width: 760px) 100vw, 50vw" alt="Red electric Moke parked under palm trees" loading="lazy" width="1400" height="1050"></div>
        <span class="ride__tag ride__tag--red">Florida and Montauk</span>
        <div class="ride__body">
          <div class="ride__title"><h3>Electric Moke</h3><div class="ride__price">$250<small>from, per day</small></div></div>
          <p>The open-top beach classic, now electric. Four seats, bright colors, and easy to park anywhere along the coast.</p>
          <ul class="ride__specs"><li>Seats four</li><li>25 mph, street legal</li><li>Seat belts and lights</li><li>All electric</li></ul>
          <div class="ride__actions">
            <a class="btn btn--red" href="#rates">See rates by location</a>
            <a class="btn btn--ghost" href="/rentals#moke">Details</a>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

{availability_section()}
{rates_section()}

<section class="section" id="how">
  <div class="container">
    <div class="section-head">
      <h2>How a rental works</h2>
    </div>
    <div class="steps">
      <div class="step"><h3>Reserve</h3><p>Pick your town and dates online, or call the local number. Drivers must be 21 or older, renters 25 or older.</p></div>
      <div class="step"><h3>We deliver</h3><p>Your cart arrives fully charged at your home, hotel or rental, at no charge.</p></div>
      <div class="step"><h3>Ride</h3><p>The beach, the avenue and everywhere in between, on any road posted 35 mph or under.</p></div>
      <div class="step"><h3>We pick up</h3><p>Leave it where we dropped it. Your $250 deposit is refunded on return.</p></div>
    </div>
  </div>
</section>

<section class="section section--white" id="gallery">
  <div class="container">
    <div class="section-head">
      <h2>Around town</h2>
    </div>
    <div class="gallery">
      <figure><img src="/assets/img/fleet-beach-1400.webp" srcset="/assets/img/fleet-beach-900.webp 900w, /assets/img/fleet-beach-1400.webp 1400w, /assets/img/fleet-beach-2048.webp 2048w" sizes="(max-width: 760px) 100vw, 60vw" alt="A Joy Ride golf cart and red Moke side by side at the beach" loading="lazy"><figcaption>Golf cart and Moke</figcaption></figure>
      <figure><img src="/assets/img/ride-atlantic-1400.webp" srcset="/assets/img/ride-atlantic-900.webp 900w, /assets/img/ride-atlantic-1400.webp 1400w" sizes="(max-width: 760px) 50vw, 25vw" alt="Golf cart and Moke driving through a Delray Beach intersection" loading="lazy"><figcaption>Atlantic Avenue</figcaption></figure>
      <figure><img src="/assets/img/video-still-900.webp" alt="Still from the Joy Ride video" loading="lazy"><a class="play" href="https://youtu.be/{BIZ['youtube_id']}" data-video="{BIZ['youtube_id']}" aria-label="Play the Joy Ride video"><span>{ICON_PLAY}</span></a><figcaption>Watch the video</figcaption></figure>
    </div>
  </div>
</section>

{reviews_block()}

<section class="section" id="locations">
  <div class="container">
    <div class="section-head">
      <h2>Where we deliver</h2>
      <p>We started in Delray Beach and now deliver up and down the coast. Delivery is free within each town's area, and each location books through its own store.</p>
    </div>
    {locations_grid()}
    <p class="mt-4"><a class="link" href="/locations">All locations and delivery areas</a></p>
  </div>
</section>

<section class="section section--sand2">
  <div class="container">
    <div class="trio">
      <div class="trio__item"><h3>Free delivery</h3><p>Door-to-door drop-off and pick-up anywhere in each town's delivery area. No trailer, no hitch, nothing to tow.</p></div>
      <div class="trio__item"><h3>Street legal</h3><p>Seat belts, headlights, hazards and turn signals on every vehicle, registered as low-speed vehicles.</p></div>
      <div class="trio__item"><h3>Card or cash</h3><p>All major credit cards online, or cash on delivery. The $250 deposit is refunded when we pick up.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media"><img src="/assets/img/ride-atlantic-1400.webp" srcset="/assets/img/ride-atlantic-900.webp 900w, /assets/img/ride-atlantic-1400.webp 1400w, /assets/img/ride-atlantic-2048.webp 2048w" sizes="(max-width: 860px) 100vw, 50vw" alt="Guests riding a golf cart and Moke through Delray Beach" loading="lazy" width="1400" height="1050"></div>
      <div>
        <h2>Events, and carts to keep</h2>
        <p class="lead">For weddings, corporate outings and block parties we supply fleets of carts, with or without drivers. If you would rather own one, we sell new and used Gorilla carts and service what we sell.</p>
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
    <div class="section-head">
      <h2>Common questions</h2>
    </div>
    <div class="faq">{faq_items}</div>
  </div>
</section>

{cta_band()}
"""
    import json
    return layout(title="Joy Ride | Golf Cart and Moke Rentals in Delray Beach, Palm Beach, Jacksonville, Charleston, Montauk and More",
                  description="Street-legal six-seat golf cart and electric Moke rentals delivered free to your door in Delray Beach, Palm Beach, Pompano, Vero Beach, Jacksonville, Rehoboth, Charleston and Montauk. Rated 5.0 on Google. Reserve online.",
                  path="/", body=body, over_hero=True, inplace=True,
                  extra_head='<script type="application/ld+json">' + json.dumps(faq_jsonld()) + '</script>')


def page_rentals():
    body = page_hero("Rentals", "Golf cart and Moke rentals", "Choose your ride and your town. We bring it to your door fully charged, and the reserve buttons open that location's checkout.",
                     image="/assets/img/fleet-beach-2048.webp", alt="Joy Ride golf cart and Moke at the beach")
    body += f"""
<section class="section" id="golf-cart">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media"><img src="/assets/img/cart-beach-2048.webp" srcset="/assets/img/cart-beach-900.webp 900w, /assets/img/cart-beach-1400.webp 1400w, /assets/img/cart-beach-2048.webp 2048w" sizes="(max-width: 860px) 100vw, 50vw" alt="Six-seat ICON golf cart on the sand" loading="lazy"></div>
      <div>
        <h2>Six-seat golf cart</h2>
        <p class="lead">Our lifted six-seater is the cart you see all over the beach. Street legal, with Bluetooth speakers, a backup camera and a roof for the sun. Top speed 25 mph, range 25 to 35 miles on a charge.</p>
        <ul class="ride__specs"><li>Seats six</li><li>Seat belts</li><li>Headlights and taillights</li><li>Hazards and turn signals</li><li>Backup camera</li><li>Bluetooth audio</li></ul>
        <div class="btn-row mt-4"><a class="btn btn--primary" href="#rates">See rates and reserve</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--white" id="moke">
  <div class="container">
    <div class="split-feature split-feature--flip">
      <div class="split-feature__media"><img src="/assets/img/moke-parked-2048.webp" srcset="/assets/img/moke-parked-900.webp 900w, /assets/img/moke-parked-1400.webp 1400w, /assets/img/moke-parked-2048.webp 2048w" sizes="(max-width: 860px) 100vw, 50vw" alt="Red electric Moke" loading="lazy"></div>
      <div>
        <h2>Electric Moke</h2>
        <p class="lead">Compact, open-top and hard to miss. The Moke seats four and tops out at 25 mph, which is all you need for the beachfront. Available in our Florida locations and Montauk.</p>
        <ul class="ride__specs"><li>Seats four</li><li>Seat belts</li><li>Headlamps</li><li>Hazards and turn signals</li><li>All electric</li><li>Several colors</li></ul>
        <div class="btn-row mt-4"><a class="btn btn--red" href="#rates">See rates and reserve</a></div>
      </div>
    </div>
  </div>
</section>

{availability_section()}
{rates_section()}

<section class="section">
  <div class="container">
    <div class="req">
      <div class="req__item"><span>Driver age</span><b>21 and over</b></div>
      <div class="req__item"><span>Renter age</span><b>25 and over</b></div>
      <div class="req__item"><span>Deposit</span><b>$250 refundable</b></div>
      <div class="req__item"><span>Delivery</span><b>Free</b></div>
    </div>
  </div>
</section>
{reviews_block()}
{cta_band()}
"""
    return layout(title="Golf Cart and Moke Rentals, Rates by Location | Joy Ride",
                  description="Rent a street-legal six-seat golf cart or an electric Moke. Pick your beach town to see local rates and reserve online. Free delivery, refundable deposit.",
                  path="/rentals", body=body, over_hero=True, inplace=True)

def page_locations():
    body = page_hero("Locations", "Where we deliver", "We started on Atlantic Avenue in Delray Beach and now deliver carts in beach towns from Florida to Long Island. Pick your town for its fleet, rates and local number.")
    body += f"""
<section class="section">
  <div class="container">
    {locations_grid()}
    <p class="muted small mt-4">Not sure if we deliver to your address? Call or text <a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a> and we will tell you in a minute.</p>
  </div>
</section>
<section class="section section--white">
  <div class="container">
    <div class="split-feature">
      <div>
        <h2>Delray Beach, our home base</h2>
        <p class="lead">{BIZ['address']}. Free delivery throughout Delray Beach, Boca Raton, Boynton Beach, Highland Beach and Gulf Stream.</p>
        <ul class="contact-list mt-4">
          <li>{ICON_PHONE}<div><span>Call or text</span><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
          <li>{ICON_MAIL}<div><span>Email</span><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
        </ul>
      </div>
      <div class="map-embed"><iframe title="Map of Joy Ride Delray Beach" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Joy+Ride+Delray+Beach+Golf+Cart+Rentals,+820+E+Atlantic+Ave,+Delray+Beach,+FL+33483&z=14&output=embed"></iframe></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Locations | Golf Cart Rentals in Delray Beach, Palm Beach, Jacksonville, Charleston, Montauk and More | Joy Ride",
                  description="Joy Ride delivers golf carts and Mokes in Delray Beach, Palm Beach, Ft Lauderdale/Pompano, Vero Beach, Jacksonville, Dewey/Rehoboth Beach, Charleston and Montauk.",
                  path="/locations", body=body)

def page_location(l):
    others = "".join(f'<a href="/{o["slug"]}"><b>{html.escape(o["city"])}</b><span>{o["state"]}</span></a>' for o in LOCATIONS if o["slug"] != l["slug"])
    fleet = "six-seat golf carts and electric Mokes" if l.get("moke") else "six-seat golf carts"
    body = page_hero(f"{html.escape(l['city'])}, {l['state']}", f"Golf cart rentals in {html.escape(l['city'])}",
                     f"{html.escape(l['blurb'])} Street-legal {fleet}, delivered free to {html.escape(', '.join(l['areas']))}.",
                     image="/assets/img/cart-beach-2048.webp", alt=f"Joy Ride golf cart in {l['city']}")
    body += f"""
{availability_section(l)}
<section class="section section--sand2" id="rates">
  <div class="container">
    <div class="section-head">
      <h2>Fleet and rates in {html.escape(l['city'])}</h2>
    </div>
    {location_panel(l, active=True)}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split-feature">
      <div>
        <h2>Talk to the {html.escape(l['city'])} line</h2>
        <p class="lead">Questions about a delivery address, dates or availability: call or text the local number and we will sort it out.</p>
        <ul class="contact-list mt-4">
          <li>{ICON_PHONE}<div><span>Call or text</span><a href="tel:{l['tel']}">{l['phone']}</a></div></li>
          <li>{ICON_MAIL}<div><span>Email</span><a href="mailto:{BIZ['email']}?subject={html.escape(l['city'])}%20rental">{BIZ['email']}</a></div></li>
        </ul>
        {f'<p class="small muted mt-4">Local site: <a href="{l["site"]}" target="_blank" rel="noopener" style="color:var(--blue);text-decoration:underline">{l["site"].replace("https://", "")}</a></p>' if l.get("site") else ""}
      </div>
      <div class="map-embed"><iframe title="Map of {html.escape(l['map'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={html.escape(l['map']).replace(' ', '+')}&z=13&output=embed"></iframe></div>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="container">
    <div class="section-head">
      <h2>Other locations</h2>
    </div>
    <div class="locs-compact">{others}</div>
  </div>
</section>
{reviews_block()}
{cta_band(l)}
"""
    return layout(title=f"Golf Cart and Moke Rentals in {l['city']}, {l['state']} | Joy Ride",
                  description=f"Joy Ride {l['city']}: street-legal six-seat golf cart{' and electric Moke' if l.get('moke') else ''} rentals from ${l['cart']['rates'][0]}/day with free delivery to {', '.join(l['areas'])}. Call {l['phone']} or reserve online.",
                  path=f"/{l['slug']}", body=body, over_hero=True, location=l["slug"])

def page_events():
    body = page_hero("Event bookings", "Golf carts for events", "Weddings, corporate outings, festivals and shuttles. With locations around Florida and up the coast, we can bring a fleet to your event.",
                     image="/assets/img/ride-atlantic-2048.webp", alt="Golf cart and Moke driving through Delray Beach")
    body += f"""
<section class="section">
  <div class="container">
    <div class="trio">
      <div class="trio__item"><h3>Weddings</h3><p>Move guests between the ceremony, photos and the reception. Decorated carts on request.</p></div>
      <div class="trio__item"><h3>Corporate events and festivals</h3><p>Fleets of carts to shuttle attendees from parking to the venue, with or without drivers.</p></div>
      <div class="trio__item"><h3>Private parties</h3><p>Birthdays, bachelor and bachelorette weekends, family reunions. Everyone gets around on their own schedule.</p></div>
    </div>
    <div class="section-head mt-6">
      <h2>Tell us about your event</h2>
      <p>Send the date, location and a rough head count and we will come back with a quote, usually the same day.</p>
      <div class="btn-row mt-2">
        <a class="btn btn--primary" href="mailto:{BIZ['email']}?subject=Event%20booking%20quote">Email for a quote</a>
        <a class="btn btn--ghost" href="tel:{BIZ['phone_tel']}">Call {BIZ['phone_display']}</a>
      </div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Event Bookings | Golf Cart Fleets for Weddings and Events | Joy Ride",
                  description="Golf cart fleets and shuttles for weddings, corporate events and private parties across Florida. Contact Joy Ride for a quote.",
                  path="/events", body=body, over_hero=True)

def page_sales():
    body = page_hero("Golf cart sales", "Golf cart sales", "New and used street-legal golf carts. We stock Gorilla carts and run them in our own fleet, so we are also the people who will look after yours.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="split-feature">
      <div class="split-feature__media"><img src="/assets/img/cart-beach-2048.webp" srcset="/assets/img/cart-beach-900.webp 900w, /assets/img/cart-beach-1400.webp 1400w, /assets/img/cart-beach-2048.webp 2048w" sizes="(max-width: 860px) 100vw, 50vw" alt="Street-legal six-seat golf cart" loading="lazy"></div>
      <div>
        <h2>New and used Gorilla carts</h2>
        <p class="lead">The question we like to answer is: who is going to be there for you after you purchase, when something goes wrong? We operate a fleet of Gorilla carts, so taking care of yours is no hassle.</p>
        <ul class="ride__specs"><li>New and used inventory</li><li>Street legal, titled</li><li>Local service and parts</li><li>Delivery available</li></ul>
        <div class="btn-row mt-4">
          <a class="btn btn--primary" href="mailto:{BIZ['email']}?subject=Golf%20cart%20sales%20inquiry">Ask about inventory</a>
          <a class="btn btn--ghost" href="tel:{BIZ['phone_tel']}">Call {BIZ['phone_display']}</a>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Golf Cart Sales | New and Used Gorilla Carts in Delray Beach | Joy Ride",
                  description="Buy a new or used street-legal Gorilla golf cart in Delray Beach from the team that runs them daily. Local service and support included.",
                  path="/sales", body=body)

def page_contact():
    body = page_hero("Contact", "Contact Joy Ride", "Questions, quotes or a last-minute booking: call, text or email and we will get back to you.")
    body += f"""
<section class="section">
  <div class="container contact-grid">
    <div class="contact-card">
      <ul class="contact-list">
        <li>{ICON_PHONE}<div><span>Call or text</span><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
        <li>{ICON_MAIL}<div><span>Email</span><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
        <li>{ICON_PIN}<div><span>Home base</span><b>{BIZ['address']}</b></div></li>
      </ul>
      <h4 class="label mt-6">Local numbers</h4>
      <table class="rate-table">{"".join(f'<tr><td><a href="/{l["slug"]}">{html.escape(l["city"])}, {l["state"]}</a></td><td style="font-family:var(--body);font-size:0.95rem"><a href="tel:{l["tel"]}">{l["phone"]}</a></td></tr>' for l in LOCATIONS)}</table>
      <div class="btn-row mt-4">
        <a class="btn btn--primary" href="/rentals#reserve">Reserve a ride</a>
        <a class="gbadge gbadge--dark" href="{BIZ['google_reviews']}" target="_blank" rel="noopener">{ICON_G}<span><strong>{BIZ['rating']}</strong> <span class="stars">{stars()}</span> on Google</span></a>
      </div>
    </div>
    <div class="map-embed"><iframe title="Map of Joy Ride Delray Beach" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Joy+Ride+Delray+Beach+Golf+Cart+Rentals,+820+E+Atlantic+Ave,+Delray+Beach,+FL+33483&z=15&output=embed"></iframe></div>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Contact Joy Ride | Golf Cart Rentals Delray Beach",
                  description="Contact Joy Ride golf cart rentals in Delray Beach. Call or text (561) 569-2438 or email rentals@joyridedelray.com.",
                  path="/contact", body=body)

def page_map():
    body = page_hero("Delray Beach golf cart map", "Where you can drive in Delray Beach", "Our carts are registered low-speed vehicles, legal on roads posted 35 mph or under. That covers the beach, Atlantic Avenue, Pineapple Grove and most of the neighborhoods in between.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="map-embed map-embed--wide"><iframe title="Delray Beach map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Delray+Beach,+FL&z=14&output=embed"></iframe></div>
    <div class="trio mt-6">
      <div class="trio__item"><h3>Go</h3><p>Atlantic Avenue, A1A along the beach, Pineapple Grove, the Marina District, Lake Ida and the residential streets east of I-95.</p></div>
      <div class="trio__item"><h3>Avoid</h3><p>I-95, sidewalks, and any road with a posted limit above 35 mph. Watch for signage on Federal Highway and Linton Boulevard.</p></div>
      <div class="trio__item"><h3>Park</h3><p>Any standard car space. The beach lots on A1A and the garages off Atlantic all work. Plug in overnight at home.</p></div>
    </div>
    <p class="muted small mt-4">Rules of the road change. Always follow posted signage, and ask us for the latest route tips when we deliver.</p>
  </div>
</section>
{cta_band()}
"""
    return layout(title="Delray Beach Golf Cart Map | Where You Can Drive | Joy Ride",
                  description="Where you can drive a street-legal golf cart in Delray Beach: the beach, Atlantic Avenue, Pineapple Grove and more. Tips from Joy Ride.",
                  path="/golf-cart-map", body=body)

def page_affiliate():
    body = page_hero("Affiliates", "Affiliate program", "Hotels, vacation rental hosts, concierges and locals: send guests our way and earn on every booking through our affiliate program.")
    body += f"""
<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="lead">Sign up in a couple of minutes, get a personal link, and track referrals and payouts in your dashboard.</p>
      <div class="btn-row mt-2">
        <a class="btn btn--primary" href="{BIZ['affiliate']}" target="_blank" rel="noopener">Join the affiliate program</a>
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
    body = page_hero("Policies", "Refund policy", "Terms for cancellations and refunds.")
    body += f"""
<section class="section">
  <div class="container prose">
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
    body = page_hero("Policies", "Terms of service", "Last updated November 27, 2022.")
    body += f"""
<section class="section">
  <div class="container prose">
    {frag}
  </div>
</section>
"""
    return layout(title="Terms of Service | Joy Ride", description="Terms of service for the Joy Ride website and rentals.", path="/terms-of-service", body=body)

def page_brand():
    body = page_hero("Brand", "Logo files", "The JOY RIDE wordmark, traced from the original logo into clean vector paths so it scales to any size. This is the logo in use across the site.")
    body += """
<section class="section">
  <div class="container">
    <div class="brand-grid">
      <div class="brand-card"><img src="/assets/logo/joyride-wordmark.svg" alt="Joy Ride wordmark, blue"><h3>Wordmark</h3><p>Primary. Blue #004AAD on light backgrounds.</p></div>
      <div class="brand-card brand-card--dark"><img src="/assets/logo/joyride-wordmark-white.svg" alt="Joy Ride wordmark, white"><h3>Reversed</h3><p>White on photos and blue.</p></div>
      <div class="brand-card"><img src="/assets/logo/favicon.svg" alt="Favicon" style="max-width:96px;margin:auto"><h3>Favicon</h3><p>The J on a blue disc, for browser tabs and home screens.</p></div>
    </div>
    <div class="section-head mt-6"><h2>Earlier concepts, not in use</h2><p>Kept in <code>assets/logo/concepts/</code> in case they are useful later.</p></div>
    <div class="brand-grid">
      <div class="brand-card"><img src="/assets/logo/concepts/joyride-classic.svg" alt="Classic concept"><h3>Classic, cleaned</h3></div>
      <div class="brand-card"><img src="/assets/logo/concepts/joyride-wheel.svg" alt="Wheel concept"><h3>Wheel O</h3></div>
      <div class="brand-card"><img src="/assets/logo/concepts/joyride-crest.svg" alt="Crest concept"><h3>Crest</h3></div>
    </div>
  </div>
</section>
"""
    return layout(title="Brand | Joy Ride", description="Joy Ride logo files.", path="/brand", body=body, noindex=True)

def page_404():
    body = f"""
<section class="page-hero">
  <div class="container">
    <h1>Page not found</h1>
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
for _l in LOCATIONS:
    PAGES[_l["slug"] + ".html"] = (lambda l: (lambda: page_location(l)))(_l)

def write_sitemap():
    urls = ["/", "/rentals", "/locations"] + [f"/{l['slug']}" for l in LOCATIONS] + ["/events", "/sales", "/contact", "/golf-cart-map", "/affiliate", "/refund-policy", "/terms-of-service"]
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
