from pathlib import Path

required = [
    'insr.cls',
    'main.tex',
    'config/project-config.tex',
    'references.bib',
    'content/manifest.tex',
    'themes/manifest.tex',
    'plugins/README.md',
    'i18n/english.tex',
]
missing = [p for p in required if not Path(p).is_file()]
if missing:
    raise SystemExit(f'Missing required files: {missing}')

root_class = Path('insr.cls').read_text(encoding='utf-8')
for token in ['config/project-config.tex', 'adapters/insr-adapter', 'INSRContentUnit', 'INSRAltFigure', 'INSRLoadPlugin']:
    if token not in root_class:
        raise SystemExit(f'Missing token in insr.cls: {token}')

base = Path('tex/latex/insr/insr-base.sty').read_text(encoding='utf-8')
for option in ['python', 'externalize', 'minted', 'review']:
    if f'\\DeclareOption{{{option}}}' not in base:
        raise SystemExit(f'Missing insr-base option: {option}')
for command in ['INSRTodoClinical', 'INSRTodoBiostats', 'INSRTodoTech']:
    if command not in base:
        raise SystemExit(f'Missing review helper command in insr-base.sty: {command}')

for class_file in ['tex/latex/insr/insr-paper.cls', 'tex/latex/insr/insr-beamer.cls', 'tex/latex/insr/insr-manual.cls']:
    text = Path(class_file).read_text(encoding='utf-8')
    for option in ['python', 'minted', 'review']:
        if f'\\DeclareOption{{{option}}}' not in text:
            raise SystemExit(f'Missing {option} option forwarding in {class_file}')

print('project validation passed')
