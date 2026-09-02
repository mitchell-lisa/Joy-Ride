# Joy Ride — joyridedelray.com redesign

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
| `assets/logo/` | New vector logo files (SVG) — see below |
| `assets/video/` | Autoplay hero loop: `hero.mp4`, `hero.webm`, `hero.gif` fallback, `hero-poster.jpg` |
| `tools/build.py` | Generates every page from one template so header/footer/meta stay in sync |

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

The hero uses a muted, inline `<video autoplay muted loop playsinline>` which autoplays on iOS and Android exactly like a GIF but at a fraction of the file size. `hero.gif` is only used if a browser refuses to play the video.

The current loop was built from the brand photos. To use the real Joy Ride film (YouTube `SMVaJwEa5kc`), export it and replace the files with the same names:

```bash
ffmpeg -i source.mp4 -t 15 -an -vf "scale=1280:-2" -c:v libx264 -crf 24 -movflags +faststart assets/video/hero.mp4
ffmpeg -i source.mp4 -t 15 -an -vf "scale=1280:-2" -c:v libvpx-vp9 -crf 34 -b:v 0 assets/video/hero.webm
ffmpeg -i source.mp4 -t 12 -vf "fps=8,scale=400:-1,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse" assets/video/hero.gif
ffmpeg -i source.mp4 -ss 2 -frames:v 1 assets/video/hero-poster.jpg
```

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
