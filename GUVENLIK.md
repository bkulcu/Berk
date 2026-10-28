# İK Perspektif — Güvenlik İnceleme Notları

> Kapsam: Yalnızca **herkese açık** HTML, JavaScript ve HTTP yanıt başlıkları incelendi.
> Saldırgan/aktif güvenlik taraması (gizli dosya-dizin denemesi, açık/yük testi, kimlik
> doğrulama kırma vb.) **yapılmadı**. Kapsamı sizinle netleştirilmiş, izinli bir test
> isterseniz ayrıca yapabilirim. Aşağıdakiler savunma amaçlı sağlamlaştırma önerileridir.

## İyi yapılmış (korunması gerekenler)
- `tenant-session.js` başında **"Backend permissions remain authoritative"** notu var; yetkinin
  sunucuda tutulduğu doğru yaklaşım.
- `api.php` çağrılarında **CSRF token** kullanılıyor (`csrf` alanı).
- `localStorage`/`sessionStorage` kiracı+kullanıcı bazında **ad alanıyla izole** ediliyor
  (`iktenant:v1:<tenant>:<user>:`), böylece aynı tarayıcıda kiracılar karışmıyor.
- Oturum bağlamı; odak, sekme görünürlüğü ve 30 sn aralıkla **yeniden doğrulanıyor**
  (`X-IK-Context` kontrolü, 401'de portала yönlendirme).
- Bazı demo sayfalarında **"gerçek aday/personel verisi girmeyin"** uyarısı var.

## Sağlamlaştırma önerileri (öncelik sırasıyla)
1. **HTTP güvenlik başlıkları** eksik: HSTS, CSP, X-Content-Type-Options, X-Frame-Options,
   Referrer-Policy yok. → `deploy/.htaccess` ile ekleyin. `X-Powered-By: PleskLin` başlığını kapatın.
2. **Sunucu tarafı yetki her istekte doğrulanmalı.** İstemcideki rol/grant kontrolleri yalnızca
   arayüzü yönlendirir; `api.php`'nin her `action`'da oturumu, kiracıyı ve yetkiyi (read/write)
   bağımsız doğruladığından emin olun. CSRF token sunucuda da kontrol edilmeli.
3. **Oturum çerezleri**: `Secure; HttpOnly; SameSite=Lax` (veya Strict) olduğundan emin olun.
4. **Dosya içe aktarma** (`calisan-organizasyon` xlsx/csv, 5000 satıra kadar): sunucuda dosya
   türü/boyutu ve içerik doğrulaması, bellek/işlem sınırı uygulayın.
5. **Örnek/yedek .json dosyaları** (`OKR_Merkez_Yedek.json`, `Eski_Tarayici_Analitik_Yedegi.json`,
   `Isgucu_Yedekleme_Yedek.json` vb. istemciden referanslanıyor): bunların yalnızca **kurgu veri**
   içerdiğini doğrulayın; gerçek dışa aktarım iseler kimlik doğrulama arkasına alın.
6. **Hız sınırlama (rate limit)** ve kaba-kuvvet koruması: giriş ve `api.php` için.
7. **Senkron XHR** (`tenant-session.js`) hem performans hem güvenilirlik açısından asenkrona
   çevrilmeli (ayrıntı: GELISTIRME.md / madde 5).
8. **Tutarsız kimlik doğrulama**: `/projeler/toplanti-asistani/` HTTP Basic Auth (401) ile
   korunurken diğerleri uygulama oturumu kullanıyor; tek bir kimlik modeline oturtun.
9. **KVKK**: kişisel veri işleyen bir platform için aydınlatma/rıza/çerez metinleri hem hukuki
   hem güvenlik-yönetişim gereği (bkz. GELISTIRME.md madde 1).
