# ============================================================
# Script para copiar y renombrar PDFs al formato estandarizado
# Ejecutar: python copiar-pdfs.py
# ============================================================

import csv, os, re, shutil, sys
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURACION ---
CSV_PATH = r'C:\Users\atenc\Downloads\Productos (8).csv'
PDF_SOURCE = r'C:\Users\atenc\OneDrive\Escritorio\fichastecnicas\Fichas Técnicas'
PDF_DEST = r'C:\Users\atenc\Claude\fichas-tecnicas\pdfs'

os.makedirs(PDF_DEST, exist_ok=True)

# --- MAPEO MANUAL para casos especiales ---
MANUAL_MAP = {
    'FT- Agrimycu 100, 041022.03.pdf': 'agrimy-cu-100',
    'FT- Agrimycu 500, 041022.03.pdf': 'agrimy-cu-500',
    'FT- Anibac Cítrico, 280125.05.pdf': 'anibac-citrico',
    'FT- Bio-Die, 300925.10.pdf': 'bio-die',
    'FT- Bio-Stick, 301024.07.pdf': 'bio-stick',
    'FT- Cu-Back, 131022.04.pdf': 'cu-back',
    'FT- Progranic Insect Out, 130325.05.pdf': 'progranic-insect-out',
    'FT- Progranic Insect Out, Jardinería, 290323.01.pdf': 'progranic-insect-out-jardineria',
    'FT- Progranic Mix-Top, 120822.07.pdf': 'progranic-mix-top',
    'FT- Progranic Neemacar, 180324.10.pdf': 'progranic-neemacar-ce',
    'FT- Progranic Neemacar, Jardinería, 290323.02.pdf': 'progranic-neemacar-ce-jardineria',
    'FT- Progranic NeemAcar, Urbano, 110423.03.pdf': 'progranic-neemacar-ce-urbano',
    'FT- Prowet Ovi-Die, 20260109.06.pdf': 'prowet-ovi-die',
    'FT- Prowet Ovi-Die, Coad, 270824.01.pdf': 'prowet-ovi-die-coadyuvante',
    'FT- Spectrum MicoRadix, 140823.03.pdf': 'spectrum-mico-radix',
    'FT- Spectrum Trico-Bio, 270922.05.pdf': 'spectrum-trico-bio',
    'FT- Prowet Bio pH, 250723.03.pdf': 'prowet-bio-ph',
    'FT- Prolux, 280723.06.pdf': 'prolux',
    'FT- Prolux Vulcano, 20260415.01.pdf': 'prolux-vulcano',
    'FT- Prolux Adherente, 280723.06.pdf': 'prolux-adherente',
    'FT- Promyl, 061022.04.pdf': 'promyl',
    'FT- Prontius, 260822.04.pdf': 'prontius',
    'FT- Prontius 500 SC, 010922.03.pdf': 'prontius-500-sc',
    'FT- Prontius ACHC, 20260304.02.pdf': 'prontius-achc',
    'FT- Prontius CA, 030223.01.pdf': 'prontius-ca',
    'FT- Prontius IO, 20260424.04.pdf': 'prontius-io',
    'FT- Prontius MG, 030223.01.pdf': 'prontius-mg',
    'FT- Prontius NI, 040223.01.pdf': 'prontius-ni',
    'FT- Nutripro-Bio Quitina, 20260226.01.pdf': 'nutripro-bio-quitina',
    'FT- Progranic Cimax, 121022.05.pdf': 'progranic-cimax',
    'FT- PTIStrobin, 20260604.03.pdf': 'ptistrobin-25-ce',
    'FT-Ultrabin, 20260604.04.pdf': 'ultrabin-25-sc',
    'FT-Anibac Plus, 270125.04.pdf': 'anibac-plus-v2',
    'FT- Prolux Adherente ECO, 20260226.01.pdf': 'prolux-adherente-eco',
    # PDFs sin producto en Wix - se incluyen con slug descriptivo
    'FT- Agayafinn, 251022.01.pdf': 'agayafinn',
    'FT- AgriCu5%, 251022.01.pdf': 'agricu-5',
    'FT- Aquackeck, 050224.01.pdf': 'aquackeck',
    'FT- Bio-Bacter, 251022.01.pdf': 'bio-bacter',
    'FT- Biocinnamon, USA, 20251127.01.pdf': 'biocinnamon-usa',
    'FT- Biodie, Jardinería, 290323.01.pdf': 'bio-die-jardineria',
    'FT- Bioshot USA, 20240321.01.pdf': 'bio-shot-usa',
    'FT- Cinnacar USA, 20240321.03.pdf': 'progranic-cinnacar-usa',
    'FT- EcoUrban, Urbano, 170423.02.pdf': 'eco-urban-urbano',
    'FT- Isaria javanica, 170624.06.pdf': 'isaria-javanica',
    'FT- Pro Canela, 070923.02.pdf': 'pro-canela',
    'FT- Pyraclostrobin 250 g.L EC, 260325.01.pdf': 'pyraclostrobin-250',
    'FT- Sigatoker, 240423.03.pdf': 'sigatoker',
    'FT- Star Acar, Urbano, 180124.01.pdf': 'star-acar-urbano',
    'FT- Star Neem CE 80, Urbano, 180124.01.pdf': 'star-neem-ce80-urbano',
    'FT- Star Neemacar CE, Urbano, 180124.01.pdf': 'star-neemacar-ce-urbano',
    'FT- Star Orgánico, Urbano, 120423.01.pdf': 'star-organico-urbano',
    'FT- Stick Potásico, 060223.01.pdf': 'stick-potasico',
    'FT- Tiofanato, 070923.03.pdf': 'tiofanato',
    'FT- Ultralite Bea B, Urbano, 180124.01.pdf': 'ultralite-bea-b-urbano',
    'FT- Ultralite Meta A, Urbano, 180124.01.pdf': 'ultralite-meta-a-urbano',
    'FT- Ultrazoxy, 251022.01.pdf': 'ultrazoxy',
    # Productos que el matching automático no encontró
    'FT- Anibac 580, 280125.05.pdf': 'anibac-580',
    'FT- Anibac Plus, 261022.03.pdf': 'anibac-plus',
    'FT- Bio Punch, 261023.01.pdf': 'bio-punch',
    'FT- Bio Shot, Jardinería, 210423.01.pdf': 'bio-shot-jardineria',
    'FT- Bio Urban, Urbano, 210423.01.pdf': 'bio-urban-urbano',
    'FT- Brasuma, 041124.03.pdf': 'brasuma',
    'FT- Citroil, 040822.07.pdf': 'citroil',
    'FT- Contronat, 20260224.02.pdf': 'contronat',
    'FT- Curistin, 041022.03.pdf': 'curistin',
    'FT- Mexagral 100, 251022.01.pdf': 'mexagral100',
    'FT- Molus Die, 250925.03.pdf': 'molus-die',
    'FT- Molus Die, Guatemala, 110923.01.pdf': 'molus-die-guatemala',
    'FT- Nato Maxx, 251022.01.pdf': 'natomaxx',
    'FT- Natuargem Supper, 280922.01.pdf': 'natuargem-supper',
    'FT- Nutripro Bio, 20251031.03.pdf': 'nutripro-bio',
    'FT- Pro Activ, 202022.02.pdf': 'pro-activ',
    'FT- Probac BS, 250822.02.pdf': 'probac-bs',
    'FT- Probac BS, Calidad, 070823.01.pdf': 'probac-bs-calidad',
    'FT- Progranic Cinnacar, 130722.06.pdf': 'progranic-cinnacar',
    'FT- Progranic Cinnacar, Jardinería, 290323.03.pdf': 'progranic-cinnacar-jardineria',
    'FT- Progranic Cinnacar, Urbano, 290323.03.pdf': 'progranic-cinnacar-urbano',
    'FT- Progreen Nema-Die, 110822.02.pdf': 'progreen-nema-die',
    'FT- Progrow 20 NPK, 160525.01.pdf': 'progrow-20npk',
    'FT- Progrow 500 F, 131022.02.pdf': 'progrow-500-f',
    'FT- Progrow Activador, 040925.03.pdf': 'progrow-activador',
    'FT- Progrow Enraizador, 230523.02.pdf': 'progrow-enraizador',
    'FT- Progrow P37, 160525.01.pdf': 'progrow-p37',
    'FT- Progrow ZN Especial, 160525.01.pdf': 'progrow-zn-especial',
    'FT- Prolux Plus pH, 280723.06.pdf': 'prolux-plus-ph',
    'FT- Prowet CL, 280723.05.pdf': 'prowet-cl',
    'FT- Prowet Pine Oil, 250723.04.pdf': 'prowet-pine-oil',
    'FT- Prowet SA, 280723.05.pdf': 'prowet-sa',
    'FT- Robust R, 061022.03.pdf': 'robust-r',
    'FT- Terra 5% Cu, 131022.03.pdf': 'terra-5-cu',
    'FT- Thiophanate Methyl, 120625.01.pdf': 'thiophanate-methyl',
    'FT- Tural, 20260204.01.pdf': 'tural',
    'FT- Tural, Coadyuvante, 020623.01.pdf': 'tural-coadyuvante',
    'FT- Ultralux N, 060325.04.pdf': 'ultralux-n',
    'FT- Naturacide Omega, Jardineria, 170124.01.pdf': 'naturacide-omega-jardineria',
}

# --- LOAD PRODUCTS FROM CSV ---
products = {}
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, quoting=csv.QUOTE_ALL)
    for row in reader:
        name = row.get('Producto', '').strip()
        slug_raw = row.get('Productos (NOMBRE DE PRODUCTO)', '').strip()
        status = row.get('Status', '').strip()
        if name and slug_raw:
            slug = unquote(slug_raw.replace('/productos/', '').strip('/'))
            slug = slug.replace('\u00ae', '').replace('%C2%AE', '')
            slug = re.sub(r'-+', '-', slug).strip('-')
            name_clean = re.sub(r'[^A-Z0-9]', '', name.upper())
            products[name_clean] = {'name': name, 'slug': slug, 'status': status}

# --- MATCHING FUNCTION ---
def make_key(s):
    s = s.upper()
    for old, new in [('\u00cd', 'I'), ('\u00c1', 'A'), ('\u00c9', 'E'), ('\u00d3', 'O'), ('\u00da', 'U')]:
        s = s.replace(old, new)
    for v in ['JARDINERIA', 'URBANO', 'USA', 'GUATEMALA', 'COADYUVANTE', 'CALIDAD', 'COAD']:
        s = s.replace(v, '')
    return re.sub(r'[^A-Z0-9]', '', s)

def extract_key(pdf):
    name = pdf.replace('.pdf', '')
    name = re.sub(r'^FT-\s*', '', name)
    name = re.sub(r',\s*[\d.]+$', '', name)
    name = re.sub(r'\s+\d{6,}[\d.]*$', '', name)
    return name.strip()

def detect_variant(key):
    kl = key.lower()
    for name, slug in [('jardinería', 'jardineria'), ('jardineria', 'jardineria'),
                        ('urbano', 'urbano'), ('usa', 'usa'), ('guatemala', 'guatemala'),
                        ('coadyuvante', 'coadyuvante'), ('calidad', 'calidad'), ('coad', 'coadyuvante')]:
        if name in kl:
            return slug
    return ''

def find_match(pdf):
    key = extract_key(pdf)
    variant = detect_variant(key)
    mk = make_key(key)

    best = None
    best_score = 0

    for pmk, pdata in products.items():
        if mk == pmk:
            best = pdata
            break
        if mk in pmk or pmk in mk:
            score = min(len(mk), len(pmk))
            if score > best_score:
                best_score = score
                best = pdata
        if len(mk) > 3 and len(pmk) > 3:
            prefix_len = min(len(mk), len(pmk), 8)
            if mk[:prefix_len] == pmk[:prefix_len]:
                score = prefix_len + sum(1 for c in mk if c in pmk)
                if score > best_score:
                    best_score = score
                    best = pdata

    if best and best_score >= 5:
        slug = best['slug']
        if variant:
            slug = f'{slug}-{variant}'
        return slug
    return None

# --- COPY AND RENAME ---
pdfs = sorted([f for f in os.listdir(PDF_SOURCE) if f.endswith('.pdf')])
copied = 0
skipped = 0
used_slugs = {}

print('=' * 70)
print('COPIANDO Y RENOMBRANDO PDFs')
print('=' * 70)

for pdf in pdfs:
    # Check manual map first
    if pdf in MANUAL_MAP:
        slug = MANUAL_MAP[pdf]
    else:
        slug = find_match(pdf)

    if not slug:
        print(f'  [SKIP] {pdf} - sin match')
        skipped += 1
        continue

    # Handle duplicates
    if slug in used_slugs:
        print(f'  [DUP]  {slug}.pdf ya existe (de: {used_slugs[slug]}), saltando: {pdf}')
        continue

    src = os.path.join(PDF_SOURCE, pdf)
    dst = os.path.join(PDF_DEST, f'{slug}.pdf')

    shutil.copy2(src, dst)
    used_slugs[slug] = pdf
    copied += 1
    print(f'  [OK]   {slug}.pdf  <--  {pdf}')

print()
print('=' * 70)
print(f'Copiados: {copied} | Saltados: {skipped} | Duplicados ignorados: {len(pdfs) - copied - skipped}')
print(f'Destino: {PDF_DEST}')
print('=' * 70)

# --- GENERATE MAPPING CSV ---
mapping_path = os.path.join(os.path.dirname(PDF_DEST), 'mapping.csv')
with open(mapping_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['slug', 'archivo_original', 'url_descarga'])
    for slug, orig in sorted(used_slugs.items()):
        writer.writerow([slug, orig, f'pdfs/{slug}.pdf'])

print(f'\nMapping guardado en: {mapping_path}')
print('Usa este CSV para actualizar la columna "Fichas Tecnicas" en Wix')
