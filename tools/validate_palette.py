from pathlib import Path
text = Path('insr.cls').read_text(encoding='utf-8')
for value in ['0A2342', '17A2B8', 'FFC107', 'F8F9FA']:
    if value not in text:
        raise SystemExit(f'Missing palette value: {value}')
print('palette validation passed')
