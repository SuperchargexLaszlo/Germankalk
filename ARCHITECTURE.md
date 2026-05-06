# ARCHITECTURE – rechnerbox.eu

## Tech stack
- **Astro 4.x** – statikus oldalgenerátor, nulla JS alapból
- **Tailwind CSS 3.x** – utility-first CSS
- **TypeScript** – típusbiztonság
- **@astrojs/sitemap** – auto sitemap
- **@astrojs/tailwind** – Tailwind integráció

## Mappastruktúra
```
D:\DEV\Germankalk\
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro      # fő layout (SEO, head, nav, footer)
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── CalcCard.astro        # kalkulátor kártya a főoldalon
│   │   └── SchemaOrg.astro      # JSON-LD schema injektálás
│   ├── pages/
│   │   ├── index.astro           # főoldal – kalkulátor lista
│   │   ├── de/                   # Németország
│   │   │   ├── brutto-netto-rechner.astro
│   │   │   ├── paypal-gebuehren-rechner.astro
│   │   │   ├── prozent-rechner.astro
│   │   │   ├── arbeitszeit-rechner.astro
│   │   │   ├── kalorien-rechner.astro
│   │   │   ├── bmi-rechner.astro
│   │   │   ├── ssw-rechner.astro
│   │   │   ├── dreisatz-rechner.astro
│   │   │   ├── pace-rechner.astro
│   │   │   ├── buergergeld-rechner.astro
│   │   │   └── mwst-rechner.astro
│   │   ├── at/                   # Ausztria (lokalizált)
│   │   └── sitemap.xml.ts        # sitemap
│   ├── data/
│   │   └── calculators.ts        # meta, kulcsszavak, leírások
│   └── styles/
│       └── global.css
├── public/
│   ├── robots.txt
│   └── favicon.svg
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── package.json
├── CLAUDE.md
├── CHANGELOG.md
├── ARCHITECTURE.md
└── SPRINTS.md
```

## SEO architektúra
- Minden kalkulátor oldal: 1 fő kw + 3-5 LSI
- hreflang: de-DE / de-AT / de-CH
- Schema: FAQPage + WebApplication
- Meta title: 50-60 kar, kw elöl
- Meta desc: 140-160 kar, CTA-val
- Canonical: önmutató
- Sitemap: @astrojs/sitemap auto

## Piacok
| Piac | URL prefix | Valuta | Adórendszer |
|------|-----------|--------|-------------|
| DE   | /de/      | EUR    | EStG 2026   |
| AT   | /at/      | EUR    | AT-Steuer   |
| CH   | /ch/      | CHF    | Quellensteuer |
