from pathlib import Path

required = ['Primary','Secondary','Accent','Background','Surface','SurfaceAlt','Text','TextMuted','Rule','Link','Success','Warning','Danger','Info','Evidence','Clinical','Research','Method','Result','Limitation','Safety']
for path in Path('palettes').glob('*.tex'):
    text = path.read_text(encoding='utf-8')
    for token in required:
        if f'INSR{token}' not in text:
            raise SystemExit(f'Missing palette token {token} in {path}')
print('palette validation passed')
