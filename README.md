# Joy Ride: joyridedelray.com redesign

A fast, static redesign of the Joy Ride golf cart & Moke rental site. No framework, no build tooling required to deploy: every page is plain HTML + one CSS file + one small JS file.

## What's here

| Path | Purpose |
| --- | --- |
| `index.html` | Home: autoplaying hero, fleet, rates, how it works, gallery, Google reviews, all eight locations, FAQ |
| `rentals.html` | Golf cart & Moke details, rate tables, requirements, reserve buttons |
| `locations.html` | All locations with phone numbers and delivery areas |
| `delray-beach.html`, `palm-beach.html`, `pompano-beach.html`, `vero-beach.html`, `jacksonville.html`, `rehoboth-beach.html`, `charleston.html`, `montauk.html` | One page per location with its own fleet, rates, local number and booking links |
| `events.html`, `sales.html`, `contact.html`, `golf-cart-map.html`, `affiliate.html` | Inner pages |
| `refund-policy.html`, `terms-of-service.html` | Policies carried over from the current site |
| `brand.html` | Logo concepts (noindex) |
| `assets/logo/` | New vector logo files (SVG): see below |
| `assets/video/` | Autoplay hero loop: `hero.mp4` (720p, 10 s, about 1.4 MB) and `hero-poster.jpg` |
| `tools/build.py` | Generates every page from one template so header/footer/meta stay in sync |
| `tools/source-img/` | Full-size JPG originals. Not served; the `assets/img/*.webp` sizes are made from these |
| `assets/fonts/` | Italiana and Jost, self-hosted as woff2. No Google Fonts request |

## One site, eight locations

The eight local Shopify stores stay as they are for checkout, but visitors only ever see this one site. A location switcher in the header (and pills on the home and rentals pages) picks the town; the fleet, rates, notes, phone number and reserve buttons update for that location, and the reserve buttons open that town's own Shopify product page. The choice is remembered in the browser.

Each location also has its own static page (`/delray-beach`, `/jacksonville`, ...) so Google can index "golf cart rentals in <town>" separately.

Everything per location lives in the `LOCATIONS` list at the top of `tools/build.py`: phone, delivery areas, cart/Moke/hourly/weekly product URLs and per-day rate tiers, add-ons and notes. Vero Beach and Dewey/Rehoboth have no store of their own and book through the Delray store. Palm Beach and Pompano only publish a one-day Moke price, so their Moke tables say "call for multi-day rates" until those tiers are added.

## Editing content

All copy, rates, locations, reviews and contact details live at the top of `tools/build.py`. Change them there, then regenerate:

```bash
python3 tools/build.py
```

Commit the regenerated HTML. (Editing the HTML directly also works if you don't want the generator.)

## Running locally

```bash
npx http-server -p 8080 --ext html .
# open http://localhost:8080
```

## Deploying

The site is static. `vercel.json` enables clean URLs (`/rentals` instead of `/rentals.html`) and long cache headers for assets. GitHub Pages and Netlify serve the same files without changes.

To point `www.joyridedelray.com` at this site, keep the Shopify store running on a subdomain (for example `shop.joyridedelray.com`) and update the two booking links in `tools/build.py`.

## Hero video

The hero uses a muted, inline `<video autoplay muted loop playsinline>` with a JPG poster. If a browser refuses to autoplay, the poster shows and nothing else changes. To swap in the real Joy Ride film (YouTube `SMVaJwEa5kc`), export it and replace the two files with the same names:

```bash
ffmpeg -i source.mp4 -t 10 -an -vf "scale=1280:-2,fps=24" -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -movflags +faststart assets/video/hero.mp4
ffmpeg -i source.mp4 -ss 1 -frames:v 1 -vf "scale=1600:-2" -q:v 6 assets/video/hero-poster.jpg
```

Keep the mp4 under about 1.5 MB. The whole home page should stay under 2.5 MB with every image loaded.

## Facts the owner still has to confirm

Anything not on joyridedelray.com or a Joy Ride product page today is either omitted or listed here. Before this replaces the live site, confirm: the founding year (removed from the site until confirmed), insurance wording (removed), hours of operation (nothing is shown), that Pompano, Vero Beach and Dewey/Rehoboth really use the Delray number, the multi-day Moke rates for Palm Beach and Pompano, the 25 mph top speed and 25 to 35 mile range, the 21 and 25 age minimums, the $250 deposit, and the current Google rating and review count.

## Logo

The site uses the JOY RIDE wordmark only. It was traced from the original logo into vector paths, so the letterforms are identical to today.

| File | Use |
| --- | --- |
| `joyride-wordmark.svg` / `joyride-wordmark-white.svg` / `joyride-wordmark-ink.svg` | Header, footer, print |
| `favicon.svg`, `apple-touch-icon.png` | The J on a blue disc |
| `concepts/` | Earlier palm/wheel explorations, not in use |

Preview at `/brand`.

## Google reviews

The reviews section links to the Google Business Profile. To make "Leave a review" open the review dialog directly, paste the Place ID into `BIZ["google_write_review"]` in `tools/build.py` as `https://search.google.com/local/writereview?placeid=...` and update `BIZ["rating"]` / `BIZ["review_count"]` when they change.
