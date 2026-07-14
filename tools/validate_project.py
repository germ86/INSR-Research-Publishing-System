from pathlib import Path
import re

required = [
    '.github/workflows/latex.yml', 'insr.cls', 'main.tex', 'config/project-config.tex',
    'references.bib', 'docs/CONFIGURATION_REFERENCE.md', 'docs/THEME_DEVELOPER_GUIDE.md',
    'docs/PALETTE_DEVELOPER_GUIDE.md', 'docs/TEMPLATE_DEVELOPER_GUIDE.md',
    'docs/TESTING_GUIDE.md', 'docs/OVERLEAF_GUIDE.md', 'docs/IMPLEMENTATION_REPORT_v4_FOUNDATION.md', 'tex/latex/insr/insr-base.sty'
]
missing = [p for p in required if not Path(p).is_file()]
if missing:
    raise SystemExit(f'Missing required files: {missing}')

main = Path('main.tex').read_text(encoding='utf-8')
expected_main = '\\documentclass{insr}\n\n\\begin{document}\n\n\\INSRMakeTitle\n\\INSRRenderDocument\n\n\\end{document}\n'
if main != expected_main:
    raise SystemExit('main.tex must remain the stable v4 public entry document')

config = Path('config/project-config.tex').read_text(encoding='utf-8')
for token in ['\\INSRConfigure', 'document/type', 'design/theme', 'design/palette', 'design/font']:
    if token not in config:
        raise SystemExit(f'Missing configuration token: {token}')

cls = Path('insr.cls').read_text(encoding='utf-8')
order = ['\\RequirePackage{expl3}', '\\InputIfFileExists{config/project-config.tex}', '\\ProcessOptions', '\\insr_resolve_document_type:', '\\LoadClass', 'framework/adapters/']
pos = []
for token in order:
    i = cls.find(token)
    if i < 0:
        raise SystemExit(f'Missing bootstrap token: {token}')
    pos.append(i)
if pos != sorted(pos):
    raise SystemExit('insr.cls bootstrap order does not match v4 two-phase requirements')

required_types = ['article','paper','position-paper','whitepaper','report','book','monograph','thesis','slides','handout','poster','letter','grant','protocol','clinical-trial-protocol','rct','systematic-review','narrative-review','technical-documentation','developer-documentation','manual']
for doc_type in required_types:
    if f'{{ {doc_type} }}' not in cls and f'{{{doc_type}}}' not in cls:
        raise SystemExit(f'Document type is not resolved in insr.cls: {doc_type}')
    profile = Path(f'profiles/documents/{doc_type}.profile.tex')
    if not profile.is_file():
        raise SystemExit(f'Missing document profile: {profile}')

for adapter in ['article','paper','report','book','slides','poster','letter','manual']:
    path = Path(f'framework/adapters/{adapter}.tex')
    if not path.is_file():
        raise SystemExit(f'Missing adapter: {path}')
    text = path.read_text(encoding='utf-8')
    for command in ['insr_adapter_make_title', 'insr_adapter_chapter', 'insr_adapter_bibliography']:
        if command not in text:
            raise SystemExit(f'Missing adapter command {command} in {path}')

for command in ['INSRMakeTitle','INSRRenderDocument','INSRShowResolvedConfiguration','ResearchQuestion','KeyFinding','SafetyStatement']:
    if command not in cls:
        raise SystemExit(f'Missing public/semantic command in insr.cls: {command}')

for palette in ['neuroclinical','clinical','research','editorial','ocean','forest','slate','graphite','monochrome','high-contrast','colourblind-safe','print','warm-clinical','calm-trauma','neurodiversity','academic-blue','biomedical','public-health','digital-health','midnight','light-minimal']:
    if not Path(f'palettes/{palette}.tex').is_file():
        raise SystemExit(f'Missing palette: {palette}')

for theme in ['insr-default','clinical','research','editorial','technical','minimal','dark','protocol','consortium','conference','documentation','accessible']:
    if not Path(f'themes/{theme}.tex').is_file():
        raise SystemExit(f'Missing theme: {theme}')

for font in ['libertinus','stix-two','ibm-plex','inter','source-serif-sans','noto','latin-modern']:
    if not Path(f'typography/{font}.tex').is_file():
        raise SystemExit(f'Missing typography preset: {font}')

for example in ['minimal-paper','minimal-slides','position-paper','clinical-manual','clinical-protocol','rct-protocol','systematic-review','thesis','conference-poster','grant-proposal','technical-documentation','custom-theme','custom-palette','theme-gallery']:
    path = Path(f'examples/{example}/main.tex')
    if not path.is_file():
        raise SystemExit(f'Missing focused example: {example}')

workflow = Path('.github/workflows/latex.yml').read_text(encoding='utf-8')
for job in ['static-validation:', 'root-smoke:', 'paper:', 'beamer:', 'manual:']:
    if re.search(rf'^  {re.escape(job)}', workflow, flags=re.MULTILINE) is None:
        raise SystemExit(f'Missing independent CI job: {job}')

readme = Path('README.md').read_text(encoding='utf-8')
for token in ['INSR v4.0 public entry model', 'config/project-config.tex', 'document/type']:
    if token not in readme:
        raise SystemExit(f'Missing README documentation: {token}')

print('project validation passed')
