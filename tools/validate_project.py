from pathlib import Path
required = ['insr.cls', 'main.tex', 'config/project-config.tex', 'references.bib', 'content/manifest.tex', 'themes/manifest.tex', 'plugins/README.md', 'i18n/english.tex', 'tests/fixtures/add-author-compat.tex']
missing = [p for p in required if not Path(p).is_file()]
if missing:
    raise SystemExit(f'Missing required files: {missing}')
text = Path('insr.cls').read_text(encoding='utf-8')
for token in ['config/project-config.tex', 'adapters/insr-adapter', 'INSRContentUnit', 'INSRAltFigure', 'INSRLoadPlugin', 'INSRAddAuthor']:
    if token not in text:
        raise SystemExit(f'Missing token in insr.cls: {token}')
print('project validation passed')

fixture = Path('tests/fixtures/add-author-compat.tex').read_text(encoding='utf-8')
if '\\INSRAddAuthor[1]{INSR Research Consortium}' not in fixture:
    raise SystemExit('compat fixture missing historical INSRAddAuthor syntax')
print('compatibility fixture validation passed')
