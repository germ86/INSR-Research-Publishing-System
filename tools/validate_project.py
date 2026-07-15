from pathlib import Path
import re

required = [
    '.github/workflows/latex.yml', 'insr.cls', 'main.tex', 'config/project-config.tex',
    'references.bib', 'content/manifest.tex', 'themes/manifest.tex', 'plugins/README.md',
    'i18n/english.tex', 'docs/CONFIGURATION_REFERENCE.md', 'docs/THEME_DEVELOPER_GUIDE.md',
    'docs/PALETTE_DEVELOPER_GUIDE.md', 'docs/TEMPLATE_DEVELOPER_GUIDE.md',
    'docs/TESTING_GUIDE.md', 'docs/OVERLEAF_GUIDE.md',
    'docs/IMPLEMENTATION_REPORT_v4_FOUNDATION.md', 'tex/latex/insr/insr-base.sty',
    'tools/overleaf_doctor.py', 'tests/test_overleaf_doctor.py',
]
insr_class_copies = [str(p) for p in Path('.').rglob('insr.cls') if '.git' not in p.parts]
if insr_class_copies != ['insr.cls']:
    raise SystemExit(f'Expected exactly one authoritative insr.cls, found: {insr_class_copies}')

missing = [p for p in required if not Path(p).is_file()]
if missing:
    raise SystemExit(f'Missing required files: {missing}')

main = Path('main.tex').read_text(encoding='utf-8')
expected_main = '\\documentclass{insr}\n\n\\begin{document}\n\n\\INSRMakeTitle\n\\INSRRenderDocument\n\n\\end{document}\n'
if main != expected_main:
    raise SystemExit('main.tex must remain the stable v4 public entry document')
if '\\begin{frame}' in main or '\\documentclass{insr-manual}' in main:
    raise SystemExit('main.tex must not contain class-incompatible Beamer/manual merge artefacts')

config = Path('config/project-config.tex').read_text(encoding='utf-8')
for token in ['\\INSRConfigure', 'document/type', 'design/theme', 'design/palette', 'design/font']:
    if token not in config:
        raise SystemExit(f'Missing configuration token: {token}')

cls = Path('insr.cls').read_text(encoding='utf-8')
required_packages = ['insr-core','insr-config','insr-metadata','insr-content','insr-adapters','insr-bibliography','insr-localization','insr-typography','insr-colors','insr-layout','insr-boxes','insr-accessibility','insr-neuro','insr-utils']
for package in required_packages:
    path = Path(f'tex/latex/insr/{package}.sty')
    if not path.is_file():
        raise SystemExit(f'Missing modular package: {path}')
    if f'\\ProvidesPackage{{{package}}}' not in path.read_text(encoding='utf-8'):
        raise SystemExit(f'Missing ProvidesPackage declaration in {path}')

order = ['\\RequirePackage{expl3}', 'insr-core.sty', 'insr-config.sty', 'insr-metadata.sty', 'config/project-config.tex', '\\ProcessOptions', '\\insr_resolve_document_type:', '\\LoadClass', 'insr-adapters.sty']
pos = []
for token in order:
    i = cls.find(token)
    if i < 0:
        raise SystemExit(f'Missing bootstrap token: {token}')
    pos.append(i)
if pos != sorted(pos):
    raise SystemExit('insr.cls bootstrap order does not match v4 package bootstrap requirements')
if len(cls.splitlines()) > 250:
    raise SystemExit('insr.cls must remain a thin bootstrap class')
for implementation_token in ['NewDocumentEnvironment { INSRContentUnit }', 'RequirePackage[backend=biber', 'tcbuselibrary', 'newacronym']:
    if implementation_token in cls:
        raise SystemExit(f'Implementation detail remains in insr.cls: {implementation_token}')

if 'config/load-project=false' not in cls or cls.find('config/load-project=false') > cls.find('config/project-config.tex'):
    raise SystemExit('insr.cls must detect config/load-project=false before reading project config')

package_text = '\n'.join(Path(f'tex/latex/insr/{package}.sty').read_text(encoding='utf-8') for package in required_packages)
if '\\__insr_load_adapter:' not in package_text or 'INSR #2:' not in package_text:
    raise SystemExit('Dedicated adapter loader or runtime file banner is missing')
if '\\exp_args:NV \\selectlanguage' not in package_text:
    raise SystemExit('Language selection must expand the configured token list')
if 'pdftitle={\\g_insr_' in package_text or 'pdfauthor={\\g_insr_' in package_text:
    raise SystemExit('PDF metadata must not receive internal token-list variables directly')
for forbidden in ['fancyhdr', 'inputenc', 'beginR', 'endR', 'beginL', 'endL', 'rlbabel.def', 'ivritex']:
    if forbidden in cls or forbidden in package_text:
        raise SystemExit(f'Forbidden runtime package/primitive found: {forbidden}')

# Guard against the Overleaf root-cause class of errors: raw LaTeX2e @ internals
# in normal runtime modules are tokenized incorrectly unless protected by
# makeatletter. Legacy compatibility code is exempted because it is wrapped.
for runtime_path in list(Path('tex/latex/insr').glob('insr-*.sty')) + list(Path('themes').glob('*.tex')) + list(Path('framework/adapters').glob('*.tex')):
    if runtime_path.name == 'insr-base.sty':
        continue
    text = runtime_path.read_text(encoding='utf-8')
    if re.search(r'\\@(ifclassloaded|ifpackageloaded|ifundefined|ifnextchar)', text):
        raise SystemExit(f'Unsafe raw LaTeX2e @ conditional in runtime file: {runtime_path}')
if r'\\alert' in Path('tex/latex/insr/insr-content.sty').read_text(encoding='utf-8'):
    raise SystemExit('insr-content.sty must not contain generic Beamer-only \\alert rendering')
for theme_path in Path('themes').glob('*.tex'):
    if theme_path.name == 'manifest.tex':
        continue
    text = theme_path.read_text(encoding='utf-8')
    if any(token in text for token in [r'\usetheme', r'\setbeamercolor', r'\setbeamertemplate', 'beamercolorbox']) and r'\str_if_eq:VnTF \g_insr_base_class_tl { beamer }' not in text:
        raise SystemExit(f'Theme contains unguarded Beamer commands: {theme_path}')
for legacy_token in ['INSRContentUnit', 'INSRAltFigure', 'INSRLoadPlugin']:
    if legacy_token not in package_text:
        raise SystemExit(f'Missing legacy compatibility/public token in modular packages: {legacy_token}')

config_pkg = Path('tex/latex/insr/insr-config.sty').read_text(encoding='utf-8')
required_types = ['article','paper','position-paper','whitepaper','report','book','monograph','thesis','slides','handout','poster','letter','grant','protocol','clinical-trial-protocol','rct','systematic-review','narrative-review','technical-documentation','developer-documentation','manual']
for doc_type in required_types:
    if f'{{ {doc_type} }}' not in config_pkg and f'{{{doc_type}}}' not in config_pkg:
        raise SystemExit(f'Document type is not resolved in insr-config.sty: {doc_type}')
    profile = Path(f'profiles/documents/{doc_type}.profile.tex')
    if not profile.is_file():
        raise SystemExit(f'Missing document profile: {profile}')

for adapter in ['article','paper','report','book','slides','poster','letter','manual']:
    path = Path(f'framework/adapters/{adapter}.tex')
    if not path.is_file():
        raise SystemExit(f'Missing adapter: {path}')
    text = path.read_text(encoding='utf-8')
    for command in ['__insr_adapter_make_title', '__insr_adapter_chapter', '__insr_adapter_bibliography']:
        if command not in text:
            raise SystemExit(f'Missing adapter command {command} in {path}')

early_api_pos = Path('tex/latex/insr/insr-core.sty').read_text(encoding='utf-8').find('\\DeclareRobustCommand{\\INSRMakeTitle}')
if early_api_pos < 0:
    raise SystemExit('INSRMakeTitle must be exported by insr-core.sty')
for command in ['INSRMakeTitle','INSRRenderDocument','INSRShowResolvedConfiguration','ResearchQuestion','KeyFinding','SafetyStatement']:
    if command not in package_text:
        raise SystemExit(f'Missing public/semantic command in modular packages: {command}')

definition_count = 0
for package in required_packages:
    definition_count += len(re.findall(r'\\(?:NewDocumentCommand|DeclareRobustCommand)\s*\{?\\INSRMakeTitle\}?', Path(f'tex/latex/insr/{package}.sty').read_text(encoding='utf-8')))
if definition_count != 1:
    raise SystemExit(f'INSRMakeTitle must have exactly one authoritative definition, found {definition_count}')

base = Path('tex/latex/insr/insr-base.sty').read_text(encoding='utf-8')
for option in ['python', 'externalize', 'minted', 'review']:
    if f'\\DeclareOption{{{option}}}' not in base:
        raise SystemExit(f'Missing legacy wrapper option in insr-base.sty: {option}')
for command in ['INSRTodoClinical', 'INSRTodoBiostats', 'INSRTodoTech']:
    if command not in base:
        raise SystemExit(f'Missing review helper command in insr-base.sty: {command}')
for class_file in ['tex/latex/insr/insr-paper.cls', 'tex/latex/insr/insr-beamer.cls', 'tex/latex/insr/insr-manual.cls']:
    text = Path(class_file).read_text(encoding='utf-8')
    if 'deprecated wrapper' not in text or '\\LoadClass{insr}' not in text:
        raise SystemExit(f'{class_file} must be a thin deprecated wrapper delegating to insr.cls')

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

for fixture in ['tests/fixtures/position-paper-editorial-content-unit.tex', 'tests/fixtures/slides-editorial-content-unit.tex']:
    if not Path(fixture).is_file():
        raise SystemExit(f'Missing LuaLaTeX regression fixture: {fixture}')

for entrypoint in __import__('subprocess').check_output(['python3', 'tools/overleaf_doctor.py', 'list-entrypoints', '--plain'], text=True).splitlines():
    if entrypoint != 'main.tex':
        text = Path(entrypoint).read_text(encoding='utf-8')
        if 'config/load-project=false' not in text:
            raise SystemExit(f'Official example does not opt out of productive config: {entrypoint}')

for content_path in ['content/manifest.tex', 'content/insr-position-paper/00-title.tex', 'content/insr-position-paper/01-abstract.tex', 'content/insr-position-paper/19-declarations.tex']:
    if not Path(content_path).is_file():
        raise SystemExit(f'Missing single-source content file: {content_path}')
if 'How can INSR maintain one source' in cls or 'Changing \\texttt{config/project-config.tex}' in cls:
    raise SystemExit('insr.cls must not contain hard-coded demonstrator prose')
for api in ['INSRContentUnit', 'INSRFullText', 'INSRSummary', 'INSRKeyMessage', 'INSROnlyFor', 'INSRExceptFor']:
    if api not in package_text:
        raise SystemExit(f'Missing content API in modular packages: {api}')

workflow = Path('.github/workflows/latex.yml').read_text(encoding='utf-8')
for job in ['static-validation:', 'root-smoke:', 'paper-examples:', 'slides-examples:', 'manual-examples:', 'focused-example-matrix:']:
    if re.search(rf'^  {re.escape(job)}', workflow, flags=re.MULTILINE) is None:
        raise SystemExit(f'Missing independent CI job: {job}')

for path in Path('.').rglob('*'):
    if path.is_file() and path.suffix in {'.tex', '.py', '.md', '.yml', '.yaml', '.sh', '.ps1'}:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if any(marker in text for marker in ['<' * 7, '=' * 7, '>' * 7]):
            raise SystemExit(f'Merge conflict marker left in {path}')

readme = Path('README.md').read_text(encoding='utf-8')
for token in ['INSR v4.0 public entry model', 'config/project-config.tex', 'document/type', 'Package architecture', 'Deprecated compatibility wrappers', 'config/load-project=false', 'content/insr-position-paper']:
    if token not in readme:
        raise SystemExit(f'Missing README documentation: {token}')
for stale in ['Beamer smoke test for CI', '\\documentclass{insr-paper}', 'The repository root `main.tex` is a Beamer smoke test']:
    if stale in readme:
        raise SystemExit(f'Stale README architecture guidance remains: {stale}')
if readme.count('\\documentclass{insr}') < 1:
    raise SystemExit('README must show the canonical v4 documentclass')

print('project validation passed')
