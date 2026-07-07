<!--
  DOLDURULMUŞ ÖRNEK — few-shot çapası (KB *Few-Shot Prompting*: format örneği talimattan güçlüdür).
  Bu dosya HİÇBİR projeye yazılmaz; PLAN taslağının hedef yoğunluğunu gösterir.
  INTENT-ornek.md'nin (newsletter-signup) devamıdır — BK kimlikleri oradan gelir.
  Dikkat: bağımlılık sırası · her adımda Doğrulama + → BK# + scope'lu commit ·
  DOLU kapsam-dışı bekçisi · bütünsel doğrulama özeti.
-->

# PLAN — Bülten Aboneliği (newsletter-signup)

> Hedef (INTENT'ten): Ziyaretçi, sitedeki formdan e-postasını bırakabilsin ve liste sağlayıcıya (Buttondown) otomatik düşsün.

## Adımlar

1. **Cloudflare Function iskeleti** — `/api/subscribe` POST ucu; Buttondown API anahtarı yalnız Function env'inde yaşar.
   - Doğrulama: lokal dev'de `curl -X POST /api/subscribe` boş gövdeye 400 döner; client bundle'ında anahtar grep'le YOK.
   - Karşıladığı kriter: → BK1
   - commit: `fn: subscribe ucu iskeleti`

2. **Buttondown entegrasyonu** — geçerli e-postayı Buttondown API'sine ilet; başarı/hata JSON'u dön.
   - Doğrulama: test anahtarıyla uçtan-uca istek → Buttondown sandbox listesinde abone görünür, yanıt <2 sn.
   - Karşıladığı kriter: → BK1
   - commit: `fn: buttondown entegrasyonu`

3. **Form bileşeni + istemci doğrulaması** — Astro bileşeni; boş/geçersiz e-posta istek atmaz, satır-içi hata gösterir.
   - Doğrulama: Vitest — 5 geçersiz örnekte fetch çağrılMAZ, geçerli örnekte çağrılır.
   - Karşıladığı kriter: → BK2
   - commit: `form: bileşen + istemci doğrulaması`

4. **Spam koruması** — Cloudflare Turnstile (görünmez mod); çözülmezse honeypot alanına düş.
   - Doğrulama: Turnstile token'sız istek Function'da 403 alır.
   - Karşıladığı kriter: → BK2
   - commit: `fn: turnstile koruması`

5. **Erişilebilirlik + başarı mesajı** — form etiketleri/odak durumları; marka tonlu başarı metni.
   - Doğrulama: Lighthouse a11y ≥95 (CI'da koşulur); başarı metni pazarlama sorumlusuna okutulur.
   - Karşıladığı kriter: → BK3, → BK4
   - commit: `form: erişilebilirlik + başarı mesajı`

## Kapsam-dışı bekçisi
- Double opt-in akışı — plana SIZMADI ✔ (Buttondown ayarına bırakıldı)
- Abone sayısı dashboard'u / analitik — plana SIZMADI ✔
- Mevcut sayfaların tasarımını değiştirmek — plana SIZMADI ✔ (form tek bileşen)

## Doğrulama özeti
- Tam suite (Vitest + uçtan-uca istek + Lighthouse CI) yeşil; Buttondown sandbox'ında bir abone kaydı uçtan uca gözlendi; BK4 metni pazarlama onaylı.
