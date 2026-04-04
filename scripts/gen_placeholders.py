import os

def write_svg(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

BASE = r'c:/Hugo/Academia_Portfolio/static'

# ── Research area SVGs ─────────────────────────────────────────────────────
research = [
    ('multi-modal-learning',       '#cba6f7', 'M8,12 L12,6 L16,12 L12,18 Z M4,6 L8,0 L12,6 L8,12 Z M12,6 L16,0 L20,6 L16,12 Z', 'Multi-modal'),
    ('longitudinal-deep-learning', '#89b4fa', 'M2,18 C6,14 10,10 14,8 S20,6 22,4', 'Longitudinal'),
    ('predictive-medicine',        '#a6e3a1', 'M3,17 L7,11 L11,14 L15,7 L19,9 L21,5', 'Predictive Med'),
    ('explainable-ai-for-health',  '#f9e2af', 'M12,2 A10,7 0 1,0 12,16 A10,7 0 1,0 12,2 Z', 'Explainable AI'),
    ('agentic-ai-for-health',      '#fab387', 'M8,12 A4,4 0 1,0 16,12 A4,4 0 1,0 8,12 M5,12 L8,12 M16,12 L19,12 M12,5 L12,8 M12,16 L12,19', 'Agentic AI'),
    ('self-supervised-learning',   '#94e2d5', 'M6,12 A6,6 0 0,1 18,12 M18,8 L18,12 L14,12', 'Self-Supervised'),
    ('medical-image-analysis',     '#f38ba8', 'M3,3 H21 V15 H3 Z M8,9 A3,3 0 1,0 14,9 A3,3 0 1,0 8,9', 'Medical Imaging'),
    ('benchmark-and-challenges',   '#eba0ac', 'M12,4 L13.5,9 L19,9 L14.5,12 L16,18 L12,15 L8,18 L9.5,12 L5,9 L10.5,9 Z', 'Benchmarks'),
]

for slug, color, path_d, label in research:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120" height="80">
  <rect width="120" height="80" rx="8" fill="#313244"/>
  <g transform="translate(48, 8)">
    <path d="{path_d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="60" y="68" font-family="sans-serif" font-size="9" fill="#bac2de" text-anchor="middle">{label}</text>
</svg>"""
    write_svg(f'{BASE}/img/research/{slug}.svg', svg)

# ── Project SVGs ───────────────────────────────────────────────────────────
projects = [
    ('inkscape-svg-maker',    '#cba6f7', 'M6,18 L18,6 M10,6 H18 V14 H10', 'SVG Maker'),
    ('inkscape-mermaid',      '#89b4fa', 'M4,4 H8 V8 H4 Z M16,4 H20 V8 H16 Z M4,16 H8 V20 H4 Z M8,6 H16 M6,8 L6,16 M18,8 L18,16', 'Mermaid Ink'),
    ('inkscape-d2',           '#a6e3a1', 'M2,2 H10 V8 H2 Z M14,6 H22 V12 H14 Z M6,8 L6,9 L14,9', 'D2 Ink'),
    ('inkscape-textgen',      '#f9e2af', 'M2,6 H22 M2,10 H18 M2,14 H20 M2,18 H14', 'TextGen Ink'),
    ('inkscape-imagegen',     '#fab387', 'M2,4 H22 V18 H2 Z M2,14 L7,9 L11,13 L15,10 L22,14', 'ImageGen Ink'),
    ('inkscape-plt',          '#94e2d5', 'M2,20 L2,2 M2,20 L22,20 M2,14 L6,10 L10,13 L14,6 L18,8', 'Plt Ink'),
    ('inkscape-poster-utils', '#eba0ac', 'M2,2 H22 V4 H2 Z M2,7 H22 M2,10 H16 M2,13 H14 M2,16 H18', 'Poster Utils'),
    ('inkscape-loadrefs',     '#cba6f7', 'M4,2 H20 V22 H4 Z M7,8 H17 M7,12 H17 M7,16 H13', 'LoadRefs Ink'),
]

for slug, color, path_d, label in projects:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" width="120" height="80">
  <rect width="120" height="80" rx="8" fill="#313244"/>
  <g transform="translate(48, 8)">
    <path d="{path_d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="60" y="68" font-family="sans-serif" font-size="9" fill="#bac2de" text-anchor="middle">{label}</text>
</svg>"""
    write_svg(f'{BASE}/img/projects/{slug}.svg', svg)

print('All SVGs created.')
