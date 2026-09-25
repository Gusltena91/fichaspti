import os
import json

PDFS_DIR = "pdfs"
HDS_DIR = "pdfs/hds"

ft_slugs = set()
for f in os.listdir(PDFS_DIR):
    if f.endswith('.pdf'):
        ft_slugs.add(f.replace('.pdf', ''))

hds_slugs = set()
for f in os.listdir(HDS_DIR):
    if f.endswith('.pdf'):
        hds_slugs.add(f.replace('.pdf', ''))

all_slugs = sorted(ft_slugs | hds_slugs)

CATEGORIES = {
    "Bactericidas": ["agrimy-cu-100", "agrimy-cu-500", "anibac-580", "anibac-citrico", "anibac-plus", "anibac-plus-v2"],
    "Fungicidas": ["coraza-720-s", "cu-back", "curistin", "promyl", "prontius", "prontius-500-sc", "prontius-achc", "prontius-ca", "prontius-io", "prontius-mg", "prontius-ni", "prozycar-50-ph", "prozycar-500-f", "ptistrobin-25-ce", "pyraclostrobin-250", "robust-r", "sigatoker", "terra-5-cu", "thiophanate-methyl", "tiofanato", "ultrazoxy", "pull-75-wg"],
    "Insecticidas": ["bio-die", "bio-die-jardineria", "bio-punch", "citroil", "fanato-lxx", "molus-die", "molus-die-guatemala", "natural-king", "progranic-cinnacar", "progranic-cinnacar-jardineria", "progranic-cinnacar-urbano", "progranic-cinnacar-usa", "progranic-gamma", "progranic-gamma-jardineria", "progranic-insect-out", "progranic-insect-out-jardineria", "progranic-mega", "progranic-mega-jardineria", "progranic-neemacar-ce", "progranic-neemacar-ce-jardineria", "progranic-neemacar-ce-urbano", "progranic-nimicide-80", "progranic-nimicide-80-jardineria", "progranic-nimicide-80-urbano", "progranic-oil-premium", "progranic-omega", "progranic-omega-jardineria", "progranic-piretro", "progranic-alfa", "progranic-cimax", "progranic-citrus", "progranic-delphinus", "progranic-mix-top", "progranic-sigma", "progreen-nema-die", "progreen-jardineria", "ataque-sulfoamex"],
    "Bioestimulantes": ["aminofit-xtra", "aminofit-kborca", "nutripro-bio", "nutripro-bio-quitina", "nutripro-brassinal", "nutripro-cab", "nutripro-energy", "nutripro-forte", "nutripro-kmg", "nutripro-mag", "nutripro-mix", "nutripro-trihormonal", "nutripro-xtra-alga", "progrow-20npk", "progrow-500-f", "progrow-activador", "progrow-enraizador", "progrow-p37", "progrow-zn-especial", "pro-activ", "pro-canela", "natuargem-supper", "natomaxx"],
    "Coadyuvantes": ["prolux", "prolux-adherente", "prolux-adherente-eco", "prolux-plus-ph", "prolux-ultra", "prolux-vulcano", "prowet-bio-adher", "prowet-bio-ph", "prowet-biodyna", "prowet-cl", "prowet-ovi-die", "prowet-ovi-die-coadyuvante", "prowet-pine-oil", "prowet-sa", "tural", "tural-coadyuvante", "stick-potasico"],
    "Biológicos": ["bio-stick", "bio-bacter", "contronat", "isaria-javanica", "probac-bs", "probac-bs-calidad", "spectrum-bea-b", "spectrum-bea-b-urbano", "spectrum-meta-a", "spectrum-meta-a-urbano", "spectrum-mico-radix", "spectrum-pae-l", "spectrum-trico-bio"],
    "Nutrición": ["ultralux-n", "ultralux-s", "ultrabin-25-sc", "agricu-5", "mexagral100", "brasuma"],
    "Jardinería": ["bio-shot-jardineria", "bio-urban-urbano", "eco-urban-urbano", "naturacide-gamma-jardineria", "naturacide-mega-jardineria", "naturacide-neem-ce-80-jardineria", "naturacide-neemacar-jardineria", "naturacide-omega-jardineria", "progranic-cinnacar-jardineria", "star-acar-urbano", "star-neem-ce80-urbano", "star-neemacar-ce-urbano", "star-organico-urbano", "ultralite-bea-b-urbano", "ultralite-meta-a-urbano"],
    "Exportación": ["bio-shot-usa", "biocinnamon-usa", "progranic-cinnacar-usa"],
    "Otros": ["agayafinn", "aquackeck"],
}

categorized = set()
for slugs in CATEGORIES.values():
    categorized.update(slugs)

uncategorized = [s for s in all_slugs if s not in categorized]
if uncategorized:
    CATEGORIES["Sin categoría"] = uncategorized

def slug_to_name(slug):
    name_map = {
        "agrimy-cu-100": "AGRIMY CU® 100",
        "agrimy-cu-500": "AGRIMY CU® 500",
        "aminofit-xtra": "AMINOFIT® XTRA",
        "aminofit-kborca": "AMINOFIT® KBorCa",
        "anibac-580": "ANIBAC® 580",
        "anibac-citrico": "ANIBAC® CITRICO",
        "anibac-plus": "ANIBAC® PLUS",
        "anibac-plus-v2": "ANIBAC® PLUS V2",
        "bio-die": "BIO-DIE®",
        "bio-punch": "Bio Punch®",
        "bio-stick": "BIO-Stick®",
        "citroil": "CITROIL®",
        "contronat": "ControNat",
        "coraza-720-s": "CORAZA® 720 S",
        "cu-back": "CU-BACK®",
        "curistin": "CURISTIN®",
        "fanato-lxx": "FANATO LXX®",
        "molus-die": "MOLUS® DIE",
        "natural-king": "NATURAL KING",
        "nutripro-bio": "NUTRIPRO® BIO",
        "nutripro-bio-quitina": "NUTRIPRO® BIO QUITINA",
        "nutripro-brassinal": "NUTRIPRO® BRASSINAL",
        "nutripro-cab": "NUTRIPRO® CaB",
        "nutripro-energy": "NUTRIPRO® ENERGY",
        "nutripro-forte": "NUTRIPRO® FORTE",
        "nutripro-kmg": "NUTRIPRO® KMg",
        "nutripro-mag": "NUTRIPRO® MAG",
        "nutripro-mix": "NUTRIPRO® MIX",
        "nutripro-trihormonal": "NUTRIPRO® TRIHORMONAL",
        "nutripro-xtra-alga": "NUTRIPRO® XTRA ALGA",
        "probac-bs": "PROBAC BS",
        "progranic-alfa": "PROGRANIC® ALFA",
        "progranic-cinnacar": "PROGRANIC® CINNACAR",
        "progranic-citrus": "PROGRANIC® CITRUS",
        "progranic-delphinus": "PROGRANIC® DELPHINUS",
        "progranic-gamma": "PROGRANIC® GAMMA",
        "progranic-insect-out": "PROGRANIC® INSECT-OUT",
        "progranic-mega": "PROGRANIC® MEGA",
        "progranic-mix-top": "PROGRANIC® MIX-TOP",
        "progranic-neemacar-ce": "PROGRANIC® NEEMACAR CE",
        "progranic-nimicide-80": "PROGRANIC® NIMICIDE 80",
        "progranic-oil-premium": "PROGRANIC® OIL PREMIUM",
        "progranic-omega": "PROGRANIC® OMEGA",
        "progranic-piretro": "PROGRANIC® PIRETRO",
        "progranic-sigma": "PROGRANIC® SIGMA",
        "progreen-nema-die": "PROGREEN® NEMA-DIE",
        "progrow-20npk": "PROGROW® 20 NPK",
        "progrow-activador": "PROGROW® ACTIVADOR",
        "progrow-enraizador": "PROGROW® ENRAIZADOR",
        "progrow-p37": "PROGROW® P37",
        "progrow-zn-especial": "PROGROW® ZN ESPECIAL",
        "prolux": "PROLUX®",
        "prolux-adherente": "PROLUX® ADHERENTE",
        "prolux-adherente-eco": "PROLUX® ADHERENTE ECO",
        "prolux-plus-ph": "PROLUX® PLUS PH",
        "prolux-ultra": "PROLUX® ULTRA",
        "promyl": "PROMYL®",
        "prontius": "PRONTIUS®",
        "prontius-500-sc": "PRONTIUS® 500 SC",
        "prowet-bio-adher": "PROWET® BIO ADHER",
        "prowet-bio-ph": "PROWET® BIO-pH",
        "prowet-biodyna": "PROWET® Biodyna",
        "prowet-cl": "PROWET® CL",
        "prowet-ovi-die": "PROWET® OVI-DIE",
        "prowet-pine-oil": "PROWET® PINE OIL",
        "prowet-sa": "PROWET® SA",
        "prozycar-50-ph": "PROZYCAR® 50 PH",
        "prozycar-500-f": "PROZYCAR® 500 F",
        "ptistrobin-25-ce": "PTIStrobin 25 CE",
        "robust-r": "ROBUST R®",
        "spectrum-bea-b": "SPECTRUM® BEA B",
        "spectrum-meta-a": "SPECTRUM® META A",
        "spectrum-mico-radix": "SPECTRUM® MICO RADIX",
        "spectrum-pae-l": "SPECTRUM® PAE L",
        "spectrum-trico-bio": "SPECTRUM® TRICO-BIO",
        "terra-5-cu": "TERRA 5% CU",
        "tural": "TURAL",
        "ultrabin-25-sc": "ULTRABIN 25 SC",
        "ultralux-n": "ULTRALUX N",
        "ultralux-s": "ULTRALUX S",
    }
    if slug in name_map:
        return name_map[slug]
    return slug.replace('-', ' ').title()

slug_to_cat = {}
for cat, slugs in CATEGORIES.items():
    for s in slugs:
        slug_to_cat[s] = cat

catalog = []
for slug in all_slugs:
    has_ft = slug in ft_slugs
    has_hds = slug in hds_slugs
    catalog.append({
        "slug": slug,
        "name": slug_to_name(slug),
        "category": slug_to_cat.get(slug, "Otros"),
        "ft": has_ft,
        "hds": has_hds,
    })

with open("catalogo.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"Catálogo generado: {len(catalog)} productos")
cats = {}
for p in catalog:
    cats[p['category']] = cats.get(p['category'], 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")
