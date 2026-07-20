# NeuroPlaNe Lab — website

Source of the website for the **NeuroPlaNe Lab** (Neurogenesis and Neural
Plasticity), Department of Cell Biology, Functional Biology and Physical
Anthropology, **Universitat de València**.

🔗 **Live site:** https://neuroplanelab.org

## Stack

- **[Hugo](https://gohugo.io)** (extended) static site generator, built on top of
  the Hugo Blox modules, with a **custom institutional theme** (own base template
  and styles under `layouts/`).
- Deployed on **Netlify** (automatic build on push to `main`).

## Local development

Requires Hugo **extended** and Go (Hugo Modules are fetched via Go).

```bash
hugo server            # serve locally at http://localhost:1313
hugo --gc --minify     # production build → public/
```

## Project structure

```
config/_default/     Site configuration (Hugo, params, menus, languages)
content/
  _index.md          Home
  research/          Research programme (rendered as a 2-column page)
  post/              News (each post: index.md + featured.jpg)
  publication/       Publications (imported from publications.bib)
  people/            Team page (members read from content/authors/)
  authors/           One folder per person (profile + role + weight)
  contact/           Contact page
layouts/
  _default/baseof.html   Shared base template (header, footer, styles)
  partials/np/           Shared partials: head (styles), masthead, footer, cards
  index.html             Home
  section/publication.html   Publications explorer (search + filters)
  section/post.html          News listing (search)
  ...                        Per-type templates (single, taxonomy, 404, …)
assets/images/logo.svg   Lab logo (used in the header)
publications.bib         Source for the publications list
```

## Editing content

- **News:** add a folder under `content/post/<date-slug>/` with an `index.md`
  (front matter: `title`, `date`, `summary`, `image.caption`) and a
  `featured.jpg`. Listings show an automatically normalized thumbnail; the
  article shows the full image.
- **Publications:** managed from `publications.bib` (imported via the GitHub
  workflow) or as `content/publication/<slug>/index.md`. The explorer uses the
  `np_topics` / `np_species` / `featured` fields for filtering.
- **People:** each member is a folder under `content/authors/<name>/` with an
  `_index.md` (`title`, `role`, `weight`, `user_groups`, `social`, bio). Add an
  optional `avatar.jpg` for a photo (otherwise initials are shown).

## Deployment

Push to `main` (or open a pull request for a Netlify **Deploy Preview**). Netlify
runs `hugo --gc --minify` and publishes `public/`.

## License

Site content © NeuroPlaNe Lab, Universitat de València. Built with Hugo and the
open-source Hugo Blox modules.
