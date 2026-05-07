"""
Batch-updates all Astro calculator pages in pages/de, pages/at, pages/ch
to import CalcHero and insert it before the <article> content.
"""

import re, os, sys, pathlib

ROOT = pathlib.Path(r"D:\DEV\Germankalk\src\pages")
DIRS = [ROOT / "de", ROOT / "at", ROOT / "ch"]

IMPORT_LINE = "import CalcHero from '../../components/CalcHero.astro';"
ALREADY_DONE_MARKER = "CalcHero"

def extract(content: str):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    title = re.sub(r'<[^>]+>', '', title)

    m2 = re.search(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    subtitle = ''
    if m2:
        subtitle = re.sub(r'<[^>]+>', '', m2.group(1)).strip()
        subtitle = re.sub(r'\s+', ' ', subtitle)

    m3 = re.search(r'[>\u203a]\s*(?:<[^>]+>)?\s*([^<\u203a>]+?)\s*(?:</[^>]+>)?\s*</nav>', content)
    breadcrumb = m3.group(1).strip() if m3 else ''
    if not breadcrumb:
        breadcrumb = ' '.join(title.split()[:4])

    return title, subtitle, breadcrumb

def country_info(d: pathlib.Path):
    if d.name == 'at': return 'Oesterreich', '/at/'
    if d.name == 'ch': return 'Schweiz', '/ch/'
    return 'Deutschland', '/de/'

def process_file(path: pathlib.Path):
    text = path.read_text(encoding='utf-8')

    if ALREADY_DONE_MARKER in text:
        print(f"  SKIP  {path.name}")
        return

    parts = text.split('---', 2)
    if len(parts) < 3:
        print(f"  SKIP  {path.name} (no frontmatter)")
        return

    fm, rest = parts[1], parts[2]

    if IMPORT_LINE not in fm:
        lines = fm.split('\n')
        last_import = -1
        for i, ln in enumerate(lines):
            if ln.strip().startswith('import '):
                last_import = i
        if last_import >= 0:
            lines.insert(last_import + 1, IMPORT_LINE)
        else:
            lines.append(IMPORT_LINE)
        fm = '\n'.join(lines)

    title, subtitle, breadcrumb = extract(rest)
    country_name, country_href = country_info(path.parent)

    def esc(s):
        return s.replace('"', '&quot;')

    hero_tag = (
        f'\n  <CalcHero\n'
        f'    title="{esc(title)}"\n'
        f'    subtitle="{esc(subtitle)}"\n'
        f'    breadcrumbLabel="{esc(breadcrumb)}"\n'
        f'    country="{country_name}"\n'
        f'    countryHref="{country_href}"\n'
        f'  />\n'
    )

    header_pat = re.compile(r'(<Header\s+slot="header"\s*/>)', re.IGNORECASE)
    if header_pat.search(rest):
        rest = header_pat.sub(r'\1' + hero_tag, rest, count=1)
    else:
        rest = '\n' + hero_tag + rest

    new_content = '---' + fm + '---' + rest
    path.write_text(new_content, encoding='utf-8')
    print(f"  OK    {path.name}")

if __name__ == '__main__':
    for d in DIRS:
        if not d.exists():
            continue
        files = sorted(d.glob('*.astro'))
        files = [f for f in files if f.name != 'index.astro']
        print(f"\n=== {d.name} ({len(files)} files) ===")
        for f in files:
            process_file(f)
    print("\nDone.")
