# İK Perspektif — Logo Seti

**Konsept:** Sembol, perspektif ızgarasından oluşan bir gövde ve başı olan bir insan figürüdür.
Izgara çizgileri başa doğru daralır; baş aynı zamanda perspektifin *kaçış noktasıdır*.
Mesaj: **insanı merkeze alan dijital bir bakış açısı** — dijital İK projeleri.

## Dosyalar

| Dosya | Kullanım |
|---|---|
| `ik-perspektif-logo.svg` | Ana logo (slogan ile) — açık zemin |
| `ik-perspektif-logo-koyu.svg` | Koyu zemin versiyonu |
| `ik-perspektif-logo-sade.svg` | Slogansız yatay logo — site başlığı (header) |
| `ik-perspektif-logo-dikey.svg` | Dikey/ortalı logo |
| `ik-perspektif-ikon.svg` | Sadece sembol |
| `favicon.svg` | Favicon / uygulama & sosyal medya profil ikonu |
| `png/` | PNG çıktılar (favicon-32, apple-touch-icon 180, ikon 512, yüksek çözünürlüklü logolar) |

Yazılar vektöre çevrilmiştir, font yüklemeye gerek yoktur (font: Inter, OFL lisanslı).

## Renkler

| Ad | HEX |
|---|---|
| Lacivert (İndigo) | `#1E2A78` |
| Turkuaz | `#14B8A6` |
| Gri (slogan) | `#64748B` |
| Turkuaz — koyu zemin | `#5EEAD4` |

## Siteye ekleme

```html
<link rel="icon" type="image/svg+xml" href="/logo/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/logo/png/favicon-32.png">
<link rel="apple-touch-icon" href="/logo/png/apple-touch-icon.png">

<a href="/" class="logo">
  <img src="/logo/ik-perspektif-logo-sade.svg" alt="İK Perspektif" height="40">
</a>
```

Yeniden üretmek için: `pip install fonttools && python3 scripts/build_logo.py`

## Alternatif konseptler (`alternatifler/`)

`karsilastirma.png` üç alternatifi yan yana gösterir. Her biri için yatay logo ve ikon (favicon) var.

1. **Mercek** — Göz şeklinde bir mercek, irisinde insan silüeti: "insana odaklanan bakış açısı". Mor → pembe, küçük harfli modern yazı.
2. **Monogram** — Kalın bir "P"; iç boşluğundaki turuncu nokta odaktaki insanı, köşedeki kare dijital pikseli temsil eder. Lacivert + turuncu, büyük harfli kurumsal yazı.
3. **Ekip** — Öne doğru büyüyen üç figür: perspektif + ekip + insan. Yeşil → mavi.

Yeniden üretmek için: `python3 scripts/build_alternatives.py`
