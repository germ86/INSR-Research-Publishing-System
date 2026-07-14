import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'references.bib')
text = path.read_text(encoding='utf-8')
entries = re.findall(r'@([a-zA-Z]+)\s*\{([^,]+),(.*?)\n\}', text, flags=re.DOTALL)
if not entries:
    raise SystemExit(f'Bibliography appears invalid: {path}')

required_by_type = {
    'article': ['author', 'title', 'journaltitle', 'year'],
    'book': ['author', 'title', 'year'],
    'incollection': ['author', 'title', 'booktitle', 'year'],
}
for entry_type, key, body in entries:
    fields = {m.group(1).lower() for m in re.finditer(r'\n\s*([a-zA-Z]+)\s*=', body)}
    missing = [field for field in required_by_type.get(entry_type.lower(), ['title']) if field not in fields]
    if missing:
        raise SystemExit(f'Bibliography entry {key} is missing required APA fields: {missing}')
    if 'doi' in body.lower() and re.search(r'doi\s*=\s*\{https?://', body, flags=re.IGNORECASE):
        raise SystemExit(f'Bibliography entry {key} should store DOI values without URL prefixes')

print('bibliography validation passed')
