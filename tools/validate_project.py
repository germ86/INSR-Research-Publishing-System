from pathlib import Path
import re

required = [
    '.github/workflows/latex.yml',
    'insr.cls',
    'main.tex',
    'config/project-config.tex',
    'references.bib',
    'content/manifest.tex',
    'themes/manifest.tex',
    'plugins/README.md',
    'i18n/english.tex',
    'docs/repository-audit-report.md',
    'tex/latex/insr/insr-base.sty',
    'tex/latex/insr/insr-paper.cls',
    'tex/latex/insr/insr-beamer.cls',
    'tex/latex/insr/insr-manual.cls',
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
for command in ['INSRTodoClinical', 'INSRTodoBiostats', 'INSRTodoTech', 'INSRAddAuthor', 'INSRInstitute', 'INSRORCID', 'INSRTitlePage', 'INSRKeywords', 'INSRAcknowledgements']:
    if command not in base:
        raise SystemExit(f'Missing shared command in insr-base.sty: {command}')

if '@ifclassloaded{beamer}' not in base or r'\institute' not in base:
    raise SystemExit('INSRAddAuthor must support Beamer without authblk/affil')

main = Path('main.tex').read_text(encoding='utf-8')
for token in ['\\documentclass{insr-beamer}', '\\begin{frame}', '\\titlepage', '\\end{frame}']:
    if token not in main:
        raise SystemExit(f'Missing Beamer smoke-test structure in main.tex: {token}')
if '\\maketitle' in main or '\\section{' in main:
    raise SystemExit('main.tex must remain a frame-based Beamer smoke test')

class_options = {
    'tex/latex/insr/insr-paper.cls': ['python', 'externalize', 'minted', 'review'],
    'tex/latex/insr/insr-beamer.cls': ['python', 'externalize', 'minted', 'review'],
    'tex/latex/insr/insr-manual.cls': ['python', 'externalize', 'minted', 'review'],
}
for class_file, options in class_options.items():
    text = Path(class_file).read_text(encoding='utf-8')
    for option in options:
        if f'\\DeclareOption{{{option}}}' not in text:
            raise SystemExit(f'Missing {option} option forwarding in {class_file}')

workflow = Path('.github/workflows/latex.yml').read_text(encoding='utf-8')
for job in ['static-validation:', 'root-smoke:', 'paper:', 'beamer:', 'manual:']:
    if re.search(rf'^  {re.escape(job)}', workflow, flags=re.MULTILINE) is None:
        raise SystemExit(f'Missing independent CI job: {job}')

manual = Path('doc/latex/insr/insr-latex-manual.tex').read_text(encoding='utf-8')
if '../../../references.bib' not in manual:
    raise SystemExit('Manual bibliography path must resolve from doc/latex/insr')


readme = Path('README.md').read_text(encoding='utf-8')
for token in ['Class-adaptive metadata helpers', 'INSRAddAuthor', 'root `main.tex` is a Beamer smoke test']:
    if token not in readme:
        raise SystemExit(f'Missing README documentation: {token}')

report = Path('docs/repository-audit-report.md').read_text(encoding='utf-8')
for token in ['Architectural findings and fixes', 'CI/CD and build fixes', 'Remaining limitations']:
    if token not in report:
        raise SystemExit(f'Missing audit report section: {token}')

print('project validation passed')
