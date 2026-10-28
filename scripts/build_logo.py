"""İK Perspektif ana logo setini ("İleri Adım" konsepti) üretir.

Sembol: "İ" ve "K" tek bir figürde birleşir. İ'nin noktası baş, gövdesi beden;
K'nin kolları ileri uzanan kol ve atılan adım. Uca doğru incelen kollar perspektifi verir.
Inter fontundaki harfler vektör yola çevrilir, böylece SVG'ler font gerektirmez.
Çalıştırma: pip install fonttools && python3 scripts/build_logo.py
"""
import math
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
OUT = Path(__file__).resolve().parent.parent / "logo"

INK = "#172554"
BLUE = "#3B82F6"
AMBER = "#F59E0B"
GRAY = "#64748B"

LIGHT = {"stem": INK, "arm_from": INK, "arm_to": BLUE, "text": INK, "tag": GRAY}
DARK = {"stem": "#FFFFFF", "arm_from": "#FFFFFF", "arm_to": "#60A5FA", "text": "#FFFFFF", "tag": "#CBD5E1"}


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


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
        f'role="img" aria-label="{title}"><title>{title}</title>{body}\n</svg>\n'
    )


def tapered(x1, y1, x2, y2, w1, w2):
    """Başlangıçta kalın, uca doğru incelen (perspektifte uzaklaşan) yuvarlak uçlu çizgi."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    px, py = -dy / n, dx / n
    a = (x1 + px * w1 / 2, y1 + py * w1 / 2)
    b = (x2 + px * w2 / 2, y2 + py * w2 / 2)
    c = (x2 - px * w2 / 2, y2 - py * w2 / 2)
    d = (x1 - px * w1 / 2, y1 - py * w1 / 2)
    r1, r2 = w1 / 2, w2 / 2
    return (f"M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}L{c[0]:.2f} {c[1]:.2f}L{d[0]:.2f} {d[1]:.2f}z"
            f"M{x2 - r2:.2f} {y2}a{r2} {r2} 0 1 0 {2 * r2:.2f} 0a{r2} {r2} 0 1 0 {-2 * r2:.2f} 0z"
            f"M{x1 - r1:.2f} {y1}a{r1} {r1} 0 1 0 {2 * r1:.2f} 0a{r1} {r1} 0 1 0 {-2 * r1:.2f} 0z")


def mark(c, gid="k"):
    """64x64 sembol (defs + şekiller)."""
    defs = (f'<linearGradient id="{gid}" x1="24" y1="0" x2="56" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{c["arm_from"]}"/><stop offset="1" stop-color="{c["arm_to"]}"/>'
            '</linearGradient>')
    shapes = (f'<circle cx="20" cy="12" r="6.5" fill="{AMBER}"/>'
              f'<rect x="15.5" y="21" width="9" height="38" rx="4.5" fill="{c["stem"]}"/>'
              f'<path d="{tapered(20, 42, 53, 14, 9, 3.5)}" fill="url(#{gid})"/>'
              f'<path d="{tapered(22, 40, 52, 57, 8.5, 3.5)}" fill="url(#{gid})"/>')
    return defs, shapes


def wordmark(c, x, base, size=34, tagline=True):
    """'İK Perspektif'; İ'nin noktası vurgu renginde. (svg gövdesi, sağ kenar) döner."""
    scale = size / 2048
    i_d, i_w = text_path("I", "Inter-Bold.otf", size, x, base)
    dot = (f'<circle cx="{x + 288 * scale:.2f}" cy="{base - 1800 * scale:.2f}" '
           f'r="{165 * scale:.2f}" fill="{AMBER}"/>')
    k_d, k_w = text_path("K", "Inter-Bold.otf", size, x + i_w - 0.6 * size / 34, base)
    p_x = x + i_w + k_w + 9 * size / 34
    p_d, p_w = text_path("Perspektif", "Inter-Medium.otf", size, p_x, base, tracking=-0.6 * size / 34)
    body = f'<path fill="{c["text"]}" d="{i_d}{k_d}"/>{dot}<path fill="{c["text"]}" d="{p_d}"/>'
    if tagline:
        tag, _ = text_path("DİJİTAL İK ÇÖZÜMLERİ", "Inter-Medium.otf", 10.5 * size / 34,
                           x + size / 34, base + 16 * size / 34, tracking=2.1 * size / 34)
        body += f'<path fill="{c["tag"]}" d="{tag}"/>'
    return body, p_x + p_w


def horizontal(c, tagline=True):
    defs, shapes = mark(c)
    text, end = wordmark(c, 76, 44 if tagline else 47, tagline=tagline)
    return svg(round(end + 4), 64, f"<defs>{defs}</defs>{shapes}{text}", "İK Perspektif")


def stacked(c):
    defs, shapes = mark(c)
    _, w = wordmark(c, 0, 0, size=30)
    width = round(w + 24)
    text, _ = wordmark(c, (width - w) / 2, 110, size=30)
    return svg(width, 132, f'<defs>{defs}</defs><g transform="translate({(width - 72) / 2 - 2:.2f} 0) scale(1.125)">'
               f"{shapes}</g>{text}", "İK Perspektif")


def icon():
    defs, shapes = mark(LIGHT)
    return svg(64, 64, f"<defs>{defs}</defs>{shapes}", "İK Perspektif")


def app_icon():
    """Favicon / profil görseli: lacivert zemin üzerinde açık renk sembol."""
    defs, shapes = mark(DARK)
    return svg(64, 64, f'<defs>{defs}</defs><rect width="64" height="64" rx="14" fill="{INK}"/>'
               f'<g transform="translate(8.5 7.5) scale(0.75)">{shapes}</g>', "İK Perspektif")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {
        "ik-perspektif-logo.svg": horizontal(LIGHT),
        "ik-perspektif-logo-sade.svg": horizontal(LIGHT, tagline=False),
        "ik-perspektif-logo-koyu.svg": horizontal(DARK),
        "ik-perspektif-logo-koyu-sade.svg": horizontal(DARK, tagline=False),
        "ik-perspektif-logo-dikey.svg": stacked(LIGHT),
        "ik-perspektif-logo-dikey-koyu.svg": stacked(DARK),
        "ik-perspektif-ikon.svg": icon(),
        "favicon.svg": app_icon(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("yazıldı:", OUT / name)
