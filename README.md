# Joy Ride — joyridedelray.com redesign

A fast, static redesign of the Joy Ride golf cart & Moke rental site. No framework, no build tooling required to deploy: every page is plain HTML + one CSS file + one small JS file.

## What's here

| Path | Purpose |
| --- | --- |
| `index.html` | Home: autoplaying hero, fleet, rates, how it works, gallery, Google reviews, all eight locations, FAQ |
| `rentals.html` | Golf cart & Moke details, rate tables, requirements, reserve buttons |
| `locations.html` | All locations with phone numbers and links to the sister sites |
| `events.html`, `sales.html`, `contact.html`, `golf-cart-map.html`, `affiliate.html` | Inner pages |
| `refund-policy.html`, `terms-of-service.html` | Policies carried over from the current site |
| `brand.html` | Logo concepts (noindex) |
| `assets/logo/` | New vector logo files (SVG) — see below |
| `assets/video/` | Autoplay hero loop: `hero.mp4`, `hero.webm`, `hero.gif` fallback, `hero-poster.jpg` |
| `tools/build.py` | Generates every page from one template so header/footer/meta stay in sync |

Reservations still go through the existing Shopify product pages, so checkout, availability and payments are unchanged. Links are set in `tools/build.py` (`BIZ["book_cart"]`, `BIZ["book_moke"]`).

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

The wordmark was traced from the original logo into vector paths, so the letterforms are identical to today. The palm trees were redrawn as clean silhouettes (the originals carried a Canva watermark).

| File | Use |
| --- | --- |
| `joyride-classic.svg` | Original layout, cleaned |
| `joyride-wheel.svg` | The O in JOY replaced by a cart wheel |
| `joyride-crest.svg` | Palms + wheel crest above the wordmark |
| `joyride-lockup.svg` / `joyride-lockup-white.svg` | Horizontal header/footer lockup |
| `joyride-mark.svg`, `favicon.svg`, `apple-touch-icon.png` | Mark, favicon, iOS icon |

Preview all of them at `/brand`.

## Google reviews

The reviews section links to the Google Business Profile. To make "Leave a review" open the review dialog directly, paste the Place ID into `BIZ["google_write_review"]` in `tools/build.py` as `https://search.google.com/local/writereview?placeid=...` and update `BIZ["rating"]` / `BIZ["review_count"]` when they change.
