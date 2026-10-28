# İK Perspektif — Site İnceleme ve Geliştirme Raporu
_İnceleme tarihi: 2026-10-28 · Kapsam: ana sayfa + 12 merkez + 33 uygulama sayfası, ortak JS, HTTP başlıkları_

Site, 12 merkez altında toplanan bir İK uygulama kataloğu (performans/OKR, bordro, PDKS,
kişilik envanteri, ücret, organizasyon, analitik…) ve `calisan-organizasyon/api.php` üzerinden
çok kiracılı (multi-tenant) bir backend kullanıyor. Sayfalar ağırlıkla istemcide (JS) render ediliyor.

## 🔴 Kritik
1. **KVKK / gizlilik uyumu görünmüyor.** Gerçek personel verisi işlenirken (bordro, PDKS, maaş,
   kişilik envanteri) aydınlatma metni, gizlilik/çerez politikası ve çerez banner'ı yok.
   `ai-mulakat` sesi ElevenLabs'e metin gönderiyor → yurt dışı veri aktarımı aydınlatması gerekir.
2. **Arama motorlarında görünmezlik.** `robots.txt` ve `sitemap.xml` yok (404). Sayfalar tamamen
   JS ile render olduğundan ham HTML boş ("Uygulama açılıyor…"). Çoğu sayfada meta description,
   Open Graph, canonical ve JSON-LD yok; favicon yok.
3. **Güvenlik başlıkları eksik.** HSTS, CSP, X-Frame-Options, X-Content-Type-Options,
   Referrer-Policy yok. `X-Powered-By: PleskLin` yığını ifşa ediyor. (Ayrıntı: GUVENLIK.md)

## 🟠 Yüksek
4. **H1/başlık yapısı tutarsız.** Birçok sayfada H1 yok (aday-degerlendirme, ai-mulakat, bordro,
   is-degerleme, personel-butcesi, ucret-odul, yerleske-egitim, yerleske-ik, kanarya);
   `yonetici-gorusme-kocu`'da 10 H1. `<title>` biçimi her sayfada farklı
   (`X | İK Perspektif`, `İK Perspektif | X`, `İK Perspektif · X`, `X · İK Perspektif`, çıplak `X`).
   → Tek şablon: **"Sayfa Adı | İK Perspektif"**. Sayfa bazlı öneriler: `templates/sayfa-meta-onerileri.csv`.
5. **Senkron XMLHttpRequest.** `tenant-session.js` her sayfa başında bloklayıcı senkron XHR yapıyor
   (`x.open('POST',endpoint,false)`) ve `Storage.prototype`'ı global override ediyor. Donma/UX riski;
   asenkron bir yükleme kapısına çevrilmeli. Ölçülen TTFB ~0.8–1.7s; `/projeler/yerleske/` bir kez 25s timeout verdi.
6. **Kırık/eksik kaynaklar.** `yonetici-gorusme-kocu/growth.js` → 404 (konsol hatası).
   `/projeler/toplanti-asistani/` → 401 Basic Auth olmasına rağmen katalogda normal uygulama gibi listeli.

## 🟡 Orta
7. **Yarım/demo içerik canlıda.** "Pilot 1.0", "Demo/yerel çalışma", "henüz tamamlanmadı" (intranet)
   modülleri son kullanıcıya aynı listede. `catalog.js`'deki `mode`/`note` alanlarını kartlarda
   bir durum rozetine dönüştürün (Canlı / Pilot / Demo / Yakında).
8. **Kiracıya özel içerik genel alanda.** `teknopark-*`, `yerleske-*` sayfaları (Teknopark İstanbul'a
   ait) herkese açık katalogda. Kiracı alanına taşıyın.
9. **Marka/dil tutarlılığı.** Header'da "İK **p**erspektif", başka yerde "İK **P**erspektif".
   Plesk hata sayfaları İngilizce (`lang="en"`). → Markalı Türkçe 404/401/500 (bkz. `deploy/404.html`).

## 🟢 İyileştirme / cila
- Favicon + apple-touch-icon (bkz. `deploy/favicon.svg`).
- Tek, hash tabanlı cache-busting (şu an `?v=...` her dosyada elle ve farklı).
- Erişilebilirlik: `aria-live` ve parola göster/gizle iyi; JS kapalıyken `<noscript>` mesajı ekleyin.
- Markalı 404 + ana sayfaya yönlendirme.

## Bu repodaki hazır dosyalar
| Dosya | Amaç | Nereye |
|---|---|---|
| `deploy/robots.txt` | Arama motoru + sitemap bildirimi | Site kökü `/robots.txt` |
| `deploy/sitemap.xml` | 42 URL'lik site haritası | Site kökü `/sitemap.xml` |
| `deploy/favicon.svg` | Markalı favicon | Site kökü `/favicon.svg` |
| `deploy/.htaccess` | Güvenlik başlıkları, HTTPS zorlama, hata sayfaları, cache | Site kökü (birleştirin) |
| `deploy/404.html` | Markalı Türkçe hata sayfası | Site kökü `/404.html` |
| `templates/head-snippet.html` | Her sayfanın `<head>`'ine meta/OG/JSON-LD | Şablon |
| `templates/sayfa-meta-onerileri.csv` | Sayfa bazlı title/description + H1 sorun listesi | Çalışma listesi |
| `GUVENLIK.md` | Güvenlik gözlemleri ve sağlamlaştırma | Belge |
