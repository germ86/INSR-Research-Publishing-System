import sys
from pathlib import Path
path = Path(sys.argv[1] if len(sys.argv) > 1 else 'references.bib')
text = path.read_text(encoding='utf-8')
if '@' not in text or 'title' not in text.lower():
    raise SystemExit(f'Bibliography appears invalid: {path}')
print('bibliography validation passed')
