# local restaurant menus

Static-ish Django site that serves local restaurant menus as fast-loading inline
WebP pages with a downloadable PDF. Each restaurant gets its own page at
`/<slug>/`. The canonical entry points are QR codes printed at the restaurant
that deep-link to the restaurant's page; the homepage is intentionally minimal
and `noindex`.

## Architecture

- Django 4.2, no DB-backed restaurant model. Restaurants live in
  `localrestaurantmenus_project/restaurants.py` as a Python dict.
- WebP for inline display (~150 KB/page), PDF for download (~2 MB total).
- WhiteNoise serves static assets in-process with hashed filenames + far-future
  `Cache-Control`, so menu assets are cached aggressively by browsers and any
  CDN in front of Cloud Run.
- Single Cloud Run service, gunicorn + WhiteNoise, no separate object store.

## Adding a new restaurant

1. Generate web assets:
   ```bash
   # from the source PNGs
   python -c "from PIL import Image; import glob, os; \
       imgs = sorted(glob.glob('/path/to/source/*.png')); \
       [Image.open(p).convert('RGB').save(f'static/menus/<slug>/{os.path.splitext(os.path.basename(p))[0]}.webp', 'WEBP', quality=82, method=6) for p in imgs]"
   # bundled PDF
   python -c "from PIL import Image; import glob; \
       imgs = sorted(glob.glob('/path/to/source/*.png')); \
       pages = [Image.open(p).convert('RGB') for p in imgs]; \
       pages[0].save('static/menus/<slug>/<slug>.pdf', 'PDF', save_all=True, append_images=pages[1:], resolution=150.0, quality=88)"
   ```
2. Add an entry to `RESTAURANTS` in `localrestaurantmenus_project/restaurants.py`.
3. Commit. The Cloud Build trigger picks it up.

## Local dev

```bash
make run
```

Opens at http://127.0.0.1:8000/. Visit `/ehsanis-hot-kabob/` for the menu page.

## Tests

```bash
make test
```

## Deploy

Push to `main`. Cloud Build builds the Dockerfile and deploys to Cloud Run.
The service must allow unauthenticated invocations.
