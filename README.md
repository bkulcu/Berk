# İK Perspektif — Geliştirme Paketi

`https://ikperspektif.com` sitesinin incelemesi ve uygulamaya hazır düzeltmeleri.

- **GELISTIRME.md** — Tam inceleme raporu (öncelikli geliştirme alanları).
- **GUVENLIK.md** — Güvenlik gözlemleri ve sağlamlaştırma önerileri.
- **deploy/** — Site köküne yüklenecek hazır dosyalar.
- **templates/** — Her sayfaya uygulanacak şablonlar ve sayfa bazlı öneri listesi.

## Hızlı kurulum
1. `deploy/robots.txt`, `deploy/sitemap.xml`, `deploy/favicon.svg`, `deploy/404.html`
   dosyalarını **site kök dizinine** yükleyin.
2. `deploy/.htaccess` içeriğini kökteki `.htaccess` ile birleştirin (veya Plesk > Apache
   ayarlarına ekleyin). **CSP'yi önce `Report-Only` ile test edin**, konsolda ihlal kalmayınca açın.
3. `templates/head-snippet.html`'i her sayfanın `<head>`'ine uyarlayın; `{{...}}` alanlarını
   `templates/sayfa-meta-onerileri.csv`'deki önerilerle doldurun. JSON-LD yalnızca ana sayfada.
4. Google Search Console'a `https://ikperspektif.com/sitemap.xml` adresini gönderin.

## Notlar
- Favicon için SVG verildi; `favicon-32.png`, `apple-touch-icon.png` ve 1200×630 `og-image.png`
  görsellerini ayrıca üretmeniz gerekir (istenirse hazırlayabilirim).
- Sitemap'teki kiracıya özel/demo sayfalarını (teknopark-*, yerleske-*) herkese açık tutmak
  istemiyorsanız ilgili satırları silin.
