<!--
  DOLDURULMUŞ ÖRNEK — few-shot çapası (KB *Few-Shot Prompting*: format örneği talimattan güçlüdür).
  Bu dosya HİÇBİR projeye yazılmaz; röportajda hedef kaliteyi göstermek içindir.
  Dikkat edilecekler: tek-cümle Hedef · BK# kimlikli, GWT'li, [kod]a itilmiş kriterler ·
  DOLU Kapsam Dışı · azaltmalı Riskler · ≤1 sayfa.
-->

# INTENT — Bülten Aboneliği (newsletter-signup)

## Bağlam
Pazarlama sitemiz statik (Astro, Cloudflare Pages'te); e-posta toplama yok. Ekip, ilgilenen ziyaretçileri elle LinkedIn'den topluyor — ayda ~40 kişi kaçıyor, ölçüm yok.

## Hedef
Ziyaretçi, sitedeki formdan e-postasını bırakabilsin ve liste sağlayıcıya (Buttondown) otomatik düşsün.

## Kullanıcı
P1: Site ziyaretçisi (abone olan). · P2: Pazarlama sorumlusu (listeyi Buttondown panelinden okuyan — bu projede ekstra arayüz almaz).

## Başarı Kriteri
- [ ] **BK1** Given form açık, When geçerli e-posta gönderilir, Then Buttondown API'sinde abone görünür ve kullanıcıya başarı mesajı döner (<2 sn) · doğrulayıcı: [kod]
- [ ] **BK2** Given geçersiz/boş e-posta, When gönderilir, Then istek API'ye GİTMEZ ve satır-içi hata gösterilir · doğrulayıcı: [kod]
- [ ] **BK3** Given form yayında, When Lighthouse koşulur, Then erişilebilirlik skoru ≥95 kalır · doğrulayıcı: [kod]
- [ ] **BK4** Given başarı mesajı metni, When pazarlama sorumlusu okur, Then marka tonuyla uyumlu bulur · doğrulayıcı: [insan]

## Kapsam Dışı
- Double opt-in akışı (Buttondown'un kendi ayarına bırakılır; bu sürümde kod yazılmaz).
- Abone sayısı dashboard'u / analitik.
- Mevcut sayfaların tasarımını değiştirmek (form tek bileşen olarak eklenir).

## Riskler
- Buttondown API limiti/kesintisi → istek kuyruklamak yerine kullanıcıya "tekrar dene" mesajı + Sentry log (basit tut).
- Spam/bot kayıtları → Cloudflare Turnstile (görünmez mod); çözülmezse honeypot alanına düş.
- API anahtarının statik sitede sızması → anahtar yalnız Cloudflare Function'da yaşar, client'a inmez.
