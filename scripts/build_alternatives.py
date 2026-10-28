"""İK Perspektif için 3 alternatif logo konsepti üretir.

Çalıştırma: pip install fonttools && python3 scripts/build_alternatives.py
"""
from build_logo import OUT, svg, text_path

ALT_OUT = OUT / "alternatifler"


def figure(x, y, s, fill, stroke=None):
    """Baş + omuz silüeti; (x, y) omuz tabanının ortası."""
    edge = f' stroke="{stroke}" stroke-width="{2.4 / s:.2f}" paint-order="stroke"' if stroke else ""
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{fill}"{edge}>'
            '<circle cx="0" cy="-15" r="5.2"/><path d="M-10 0C-10-10.5 10-10.5 10 0z"/></g>')


ALTERNATIVES = {
    # 1) Göz / mercek: bakış açısının merkezinde insan var.
    "mercek": {
        "defs": ('<linearGradient id="a" x1="4" y1="20" x2="60" y2="44" gradientUnits="userSpaceOnUse">'
                 '<stop offset="0" stop-color="#7C3AED"/><stop offset="1" stop-color="#EC4899"/></linearGradient>'
                 '<clipPath id="iris"><circle cx="32" cy="32" r="11.5"/></clipPath>'),
        "mark": ('<path d="M5 32C15 15.5 49 15.5 59 32 49 48.5 15 48.5 5 32z" fill="none" stroke="url(#a)" '
                 'stroke-width="4" stroke-linejoin="round"/>'
                 '<circle cx="32" cy="32" r="11.5" fill="url(#a)"/>'
                 '<g clip-path="url(#iris)" fill="#fff"><circle cx="32" cy="28.6" r="3.8"/>'
                 '<path d="M23.5 45C23.5 36 40.5 36 40.5 45z"/></g>'),
        "bg": "#4C1D95",
        "words": [("ik", "Inter-ExtraBold.otf", "#7C3AED"), ("perspektif", "Inter-Medium.otf", "#3B0764")],
        "tagline": ("dijital ik çözümleri", "#9333EA"),
    },
    # 2) Monogram: P harfi; iç boşluğundaki turuncu nokta = odaktaki insan, kare = dijital piksel.
    "monogram": {
        "defs": "",
        "mark": ('<path d="M19 56V15h14a12.5 12.5 0 0 1 0 25h-9" fill="none" stroke="#0F172A" '
                 'stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
                 '<circle cx="33" cy="27.5" r="4.6" fill="#F97316"/>'
                 '<rect x="44" y="45" width="9" height="9" rx="2" fill="#F97316"/>'),
        "bg": "#0F172A",
        "words": [("İK", "Inter-ExtraBold.otf", "#F97316"), ("PERSPEKTİF", "Inter-Bold.otf", "#0F172A")],
        "tracking": 2.2,
        "tagline": ("DİJİTAL İK ÇÖZÜMLERİ", "#64748B"),
    },
    # 3) Ekip: yaklaştıkça büyüyen üç figür; perspektif + insan + ekip.
    "ekip": {
        "defs": ('<linearGradient id="c" x1="0" y1="0" x2="1" y2="1">'
                 '<stop offset="0" stop-color="#10B981"/><stop offset="1" stop-color="#0284C7"/></linearGradient>'),
        "mark": (figure(14, 50, 0.72, "#A7F3D0", "#fff") + figure(27, 52, 0.98, "#34D399", "#fff")
                 + figure(43, 56, 1.36, "url(#c)", "#fff")),
        "bg": "#065F46",
        "words": [("İK", "Inter-ExtraBold.otf", "#059669"), ("Perspektif", "Inter-SemiBold.otf", "#0C4A6E")],
        "tagline": ("Dijital İK Çözümleri", "#0284C7"),
    },
}


def horizontal(alt):
    tracking = alt.get("tracking", -0.6)
    size = 30 if tracking > 0 else 34
    x = 76
    parts = [f"<defs>{alt['defs']}</defs>", alt["mark"]]
    for text, font, color in alt["words"]:
        d, w = text_path(text, font, size, x, 44, tracking=tracking)
        parts.append(f'\n  <path fill="{color}" d="{d}"/>')
        x += w + (12 if tracking > 0 else 10)
    tag_text, tag_color = alt["tagline"]
    tag, _ = text_path(tag_text, "Inter-Medium.otf", 11, 77, 60, tracking=1.6)
    parts.append(f'\n  <path fill="{tag_color}" d="{tag}"/>')
    return svg(int(x + 2), 64, "".join(parts), "İK Perspektif")


def app_icon(alt):
    """Zemin rengi üzerinde beyaz sembol (favicon / profil görseli)."""
    mark = alt["mark"]
    for old in ("url(#a)", "url(#c)", "#0F172A", "#A7F3D0", "#34D399"):
        mark = mark.replace(old, "#FFFFFF")
    mark = mark.replace('stroke="#fff"', f'stroke="{alt["bg"]}"').replace(
        'fill="#fff"><circle cx="32" cy="28.6"', f'fill="{alt["bg"]}"><circle cx="32" cy="28.6"')
    return svg(64, 64, f'<defs>{alt["defs"]}</defs><rect width="64" height="64" rx="14" fill="{alt["bg"]}"/>'
               f'<g transform="translate(8 8) scale(0.75)">{mark}</g>', "İK Perspektif")


if __name__ == "__main__":
    ALT_OUT.mkdir(parents=True, exist_ok=True)
    for i, (name, alt) in enumerate(ALTERNATIVES.items(), 1):
        for suffix, content in (("logo", horizontal(alt)), ("ikon", app_icon(alt))):
            path = ALT_OUT / f"{i}-{name}-{suffix}.svg"
            path.write_text(content, encoding="utf-8")
            print("yazıldı:", path)
