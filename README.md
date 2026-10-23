# Sequence Analytics website

Hugo site for sequence-analytics.com. No theme: layouts live in `layouts/`, styles in `assets/css/main.css`.

## Run locally

```sh
hugo server        # http://localhost:1313, live reload
hugo --minify      # build to public/
```

Needs Hugo 0.168 or later (extended not required).

## Content

| Section  | Where                                   |
|----------|-----------------------------------------|
| Home     | `content/_index.md` (hero text, "How we work" steps) |
| Services | `content/services/`, one file (or bundle) per service; `group` puts it under Measure, Experiment, Simulate or Implement (listed in `content/services/_index.md`), `weight` sets the order |
| News     | `content/news/`, one file per post; newest three show on the home page |
| About    | `content/about.md`                      |
| Contact  | `content/contact.md`; details come from `[params]` in `hugo.toml` |

New news post: `hugo new content news/my-post.md`.

Service pages keep their intro in `lead`; see "Service pages" below for the rest.

## House style

The site is **print**: Nunito Sans and the house palette, matching the reports and decks in `sequence-analytics-audit` (`R/palette.R`, `_extensions/sequence/sequence.scss`). Keep the `:root` variables in `assets/css/main.css` in step with those files.

The four coloured dashes from the logo are a brand signature, used in page heads, the footer and the service groups. On a service card the group's dash runs the full width of the card on hover.

## Service pages

Each service page has a left column with three sections, and example images stacked on the right:

- **What is it?** is the body text of the page, followed by `good_for`.
- **What we need** is the `data` list.
- **What you get** is the `get` list.

Quote a list item that contains a colon followed by a space (`- "Test design: ..."`), or YAML reads it as a key.

Examples are images in the page bundle, listed under `examples` (two or three works best). Without any, the text runs alone at reading width.

```yaml
examples:
  - src: figure.webp
    label: Example · dummy client
    title: Propensity with drive time
    sub: Predicted index by small area; 100 is the GB average per resident.
    alt: What the image shows, in a sentence or two.
    source: Dummy client data with Census 2021.
```

The media mix modelling page shows a placeholder chart until there's a real one.

## Client logos

The home page's "Our clients" strip lists logos under `clients` in `content/_index.md`. To add one, put the original in `sources/client-logos/`, add it to `LOGOS` in `scripts/client_logos.py` and run `python3 scripts/client_logos.py` (needs Pillow, numpy and Inkscape). That writes a grey, trimmed PNG to `assets/images/clients/`.

## Deploy

`.github/workflows/hugo.yml` builds and deploys to GitHub Pages on every push to `main`. In the GitHub repo, set Settings > Pages > Source to **GitHub Actions**. For a custom domain, set it in Settings > Pages and add `static/CNAME` containing the domain.
