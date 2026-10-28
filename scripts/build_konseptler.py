"""İK Perspektif için 3 yeni konsept (2. tur) üretir.

Ortak fikir: Türkçeye özgü noktalı "İ". Noktası insanın başı; İK = İnsan Kaynakları.
Yazıda da "İ"nin noktası vurgu rengindedir.
Çalıştırma: pip install fonttools && python3 scripts/build_konseptler.py
"""
from build_logo import OUT, svg, tapered, text_path

KONSEPT_OUT = OUT / "konseptler"
INK = "#172554"
GRAY = "#64748B"


KONSEPTLER = {
    # 1) İK harfleri tek bir figürde: İ'nin noktası baş, gövdesi beden;
    #    K'nin kolları ileri uzanan kol ve atılan adım. Uçlara doğru incelme = perspektif.
    "ileri-adim": {
        "accent": "#F59E0B",
        "bg": INK,
        "defs": ('<linearGradient id="k" x1="24" y1="0" x2="56" y2="0" gradientUnits="userSpaceOnUse">'
                 f'<stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="#3B82F6"/></linearGradient>'),
        "mark": (f'<circle cx="20" cy="12" r="6.5" fill="#F59E0B"/>'
                 f'<rect x="15.5" y="21" width="9" height="38" rx="4.5" fill="{INK}"/>'
                 f'<path d="{tapered(20, 42, 53, 14, 9, 3.5)}" fill="url(#k)"/>'
                 f'<path d="{tapered(22, 40, 52, 57, 8.5, 3.5)}" fill="url(#k)"/>'),
    },
    # 2) İki bakış açısı: çalışan ve işveren. Bakışlarının kesiştiği yer ortak görüş.
    "kesisen-bakis": {
        "accent": "#0D9488",
        "bg": "#1E1B4B",
        "defs": '<clipPath id="sol"><path d="M12 32 47 18V46z"/></clipPath>',
        "mark": ('<path d="M12 32 47 18V46z" fill="#2DD4BF" stroke="#2DD4BF" stroke-width="3" stroke-linejoin="round"/>'
                 '<path d="M52 32 17 18V46z" fill="#A78BFA" stroke="#A78BFA" stroke-width="3" stroke-linejoin="round"/>'
                 '<path d="M52 32 17 18V46z" fill="#312E81" clip-path="url(#sol)"/>'
                 '<circle cx="6.5" cy="32" r="6" fill="#0D9488"/><circle cx="57.5" cy="32" r="6" fill="#7C3AED"/>'),
    },
    # 3) Kariyer yolu: perspektifte ufka uzanan yol "İ"nin gövdesi, ufuktaki nokta hedef/insan.
    "kariyer-yolu": {
        "accent": "#F97316",
        "bg": "#134E4A",
        "defs": ('<linearGradient id="y" x1="0" y1="1" x2="0" y2="0">'
                 '<stop offset="0" stop-color="#0F766E"/><stop offset="1" stop-color="#5EEAD4"/></linearGradient>'),
        "mark": ('<circle cx="32" cy="10" r="7" fill="#F97316"/>'
                 '<path d="M29.6 23h4.8a1.5 1.5 0 0 1 1.5 1.3l5.4 33a1.5 1.5 0 0 1-1.5 1.7H24.2a1.5 1.5 0 0 1-1.5-1.7l5.4-33a1.5 1.5 0 0 1 1.5-1.3z" fill="url(#y)"/>'
                 '<path d="M32 26.5v3M32 34v4.5M32 44v6.5" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'),
    },
}


def wordmark(accent, x, base, size=34):
    """'İK Perspektif'; İ'nin noktası vurgu renginde ayrı bir daire olarak çizilir."""
    scale = size / 2048
    i_d, i_w = text_path("I", "Inter-Bold.otf", size, x, base)
    dot = (f'<circle cx="{x + 288 * scale:.2f}" cy="{base - 1800 * scale:.2f}" '
           f'r="{165 * scale:.2f}" fill="{accent}"/>')
    k_d, k_w = text_path("K", "Inter-Bold.otf", size, x + i_w - 0.6, base)
    p_x = x + i_w + k_w + 9
    p_d, p_w = text_path("Perspektif", "Inter-Medium.otf", size, p_x, base, tracking=-0.6)
    tag, _ = text_path("DİJİTAL İK ÇÖZÜMLERİ", "Inter-Medium.otf", 10.5, x + 1, base + 16, tracking=2.1)
    body = (f'<path fill="{INK}" d="{i_d}{k_d}"/>{dot}<path fill="{INK}" d="{p_d}"/>'
            f'<path fill="{GRAY}" d="{tag}"/>')
    return body, p_x + p_w


def horizontal(k):
    text, end = wordmark(k["accent"], 76, 44)
    return svg(int(end + 4), 64, f'<defs>{k["defs"]}</defs>{k["mark"]}{text}', "İK Perspektif")


def app_icon(k):
    return svg(64, 64, f'<defs>{k["defs"]}</defs><rect width="64" height="64" rx="14" fill="#fff"/>'
               f'<g transform="translate(9 9) scale(0.72)">{k["mark"]}</g>', "İK Perspektif")


if __name__ == "__main__":
    KONSEPT_OUT.mkdir(parents=True, exist_ok=True)
    for i, (name, k) in enumerate(KONSEPTLER.items(), 1):
        for suffix, content in (("logo", horizontal(k)), ("ikon", app_icon(k))):
            path = KONSEPT_OUT / f"{i}-{name}-{suffix}.svg"
            path.write_text(content, encoding="utf-8")
            print("yazıldı:", path)
