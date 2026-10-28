"""İK Perspektif logo üretici.

Inter fontundaki harfleri vektör yola (path) çevirerek font bağımsız SVG
logolar üretir. Çalıştırma: pip install fonttools && python3 scripts/build_logo.py
"""
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
OUT = Path(__file__).resolve().parent.parent / "logo"

INDIGO = "#1E2A78"
TEAL = "#14B8A6"
SLATE = "#64748B"


def text_path(text, font_file, size, x, y, tracking=0.0):
    """Metni verilen konumda SVG path verisine çevirir; (d, genişlik) döner."""
    font = TTFont(FONT_DIR / font_file)
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(glyphs)
    cursor = 0.0
    for ch in text:
        name = cmap[ord(ch)]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x + cursor, y))
        glyphs[name].draw(tpen)
        cursor += glyphs[name].width * scale + tracking
    return pen.getCommands(), cursor - tracking


def gradient(gid):
    return (
        f'<linearGradient id="{gid}" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{INDIGO}"/></linearGradient>'
    )


def mark(gid, grid="#FFFFFF", simple=False):
    """64x64 sembol: perspektif ızgarasından oluşan gövde + baş = insan figürü.

    Baş aynı zamanda ızgara çizgilerinin birleştiği kaçış noktasıdır:
    'insanı merkeze alan dijital bakış açısı'.
    """
    return f"""
  <circle cx="32" cy="14" r="7.5" fill="url(#{gid})"/>
  <path d="M24.6 26h14.8a3 3 0 0 1 2.7 1.7l12.6 25.4A2 2 0 0 1 52.9 56H11.1a2 2 0 0 1-1.8-2.9l12.6-25.4a3 3 0 0 1 2.7-1.7z" fill="url(#{gid})"/>
  <g stroke="{grid}" stroke-width="{2.6 if simple else 1.6}" stroke-linecap="round" opacity="0.85" fill="none">
    {'<path d="M16.5 37.5h31M12.3 46.5h39.4"/>' if simple else '<path d="M18.6 33.5h26.8M15.4 40.5h33.2M11.6 48h40.8"/>'}
    {"" if simple else '<path d="M28.4 27.5 24 54.5M35.6 27.5 40 54.5"/>'}
  </g>"""


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{title}"><title>{title}</title>{body}\n</svg>\n'
    )


def horizontal(dark=False, tagline=True):
    ik_col = "#FFFFFF" if dark else INDIGO
    per_col = "#5EEAD4" if dark else TEAL
    tag_col = "#CBD5E1" if dark else SLATE
    base = 44 if tagline else 46
    ik, ik_w = text_path("İK", "Inter-ExtraBold.otf", 34, 74, base, tracking=-0.6)
    per, per_w = text_path("Perspektif", "Inter-SemiBold.otf", 34, 74 + ik_w + 10, base, tracking=-0.6)
    width = int(74 + ik_w + 10 + per_w + 6)
    parts = [f"<defs>{gradient('g')}</defs>", mark("g", "#0F172A" if dark else "#FFFFFF"),
             f'\n  <path fill="{ik_col}" d="{ik}"/>', f'\n  <path fill="{per_col}" d="{per}"/>']
    h = 64
    if tagline:
        tag, _ = text_path("DİJİTAL İK ÇÖZÜMLERİ", "Inter-Medium.otf", 10.5, 75, 60, tracking=2.1)
        parts.append(f'\n  <path fill="{tag_col}" d="{tag}"/>')
    return svg(width, h, "".join(parts), "İK Perspektif")


def stacked():
    ik, ik_w = text_path("İK", "Inter-ExtraBold.otf", 30, 0, 0, tracking=-0.5)
    per, per_w = text_path("Perspektif", "Inter-SemiBold.otf", 30, 0, 0, tracking=-0.5)
    total = ik_w + 8 + per_w
    width = int(total + 20)
    x0 = (width - total) / 2
    ik, _ = text_path("İK", "Inter-ExtraBold.otf", 30, x0, 112, tracking=-0.5)
    per, _ = text_path("Perspektif", "Inter-SemiBold.otf", 30, x0 + ik_w + 8, 112, tracking=-0.5)
    body = (f"<defs>{gradient('g')}</defs>"
            f'<g transform="translate({(width - 72) / 2} 0) scale(1.125)">{mark("g")}</g>'
            f'\n  <path fill="{INDIGO}" d="{ik}"/>\n  <path fill="{TEAL}" d="{per}"/>')
    return svg(width, 124, body, "İK Perspektif")


def icon():
    body = (f"<defs>{gradient('g')}</defs>"
            f'<g transform="translate(4 4) scale(0.875)">{mark("g")}</g>')
    return svg(64, 64, body, "İK Perspektif")


def app_icon():
    """Favicon / sosyal medya profil görseli: gradyan zemin üzerinde beyaz sembol."""
    body = (f"<defs>{gradient('g')}</defs>"
            '<rect width="64" height="64" rx="14" fill="url(#g)"/>'
            '<g transform="translate(9 8) scale(0.72)">'
            + mark("w", "#1E2A78", simple=True).replace("url(#w)", "#FFFFFF") + "</g>")
    return svg(64, 64, body, "İK Perspektif")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {
        "ik-perspektif-logo.svg": horizontal(),
        "ik-perspektif-logo-sade.svg": horizontal(tagline=False),
        "ik-perspektif-logo-koyu.svg": horizontal(dark=True),
        "ik-perspektif-logo-dikey.svg": stacked(),
        "ik-perspektif-ikon.svg": icon(),
        "favicon.svg": app_icon(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("yazıldı:", OUT / name)
