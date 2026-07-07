<!--
  DOLDURULMUŞ ÖRNEK — few-shot çapası; HİÇBİR projeye yazılmaz.
  DELTA change-spec'in hedef yoğunluğu: koddan doğrulanmış mevcut davranış · tek cümle
  hedef delta · "mevcut testler geçer" İLK invariant · DOLU kapsam sınırı ·
  invariant-koruma GWT'li BK · → BK# demirli atomik adımlar.
-->

# DELTA — API Rate Limit (rate-limit)

## Mevcut davranış
`/api/*` uçları kimlik doğrulama sonrası istek sayısı sınırı olmadan çalışıyor (keşif: `src/middleware/` altında limiter yok; yük testinde 500 istek/dk kabul edildi).

## Hedef delta
`/api/*` uçları istemci başına dakikada 60 istekle sınırlansın; aşan istek 429 + `Retry-After` başlığı alsın.

## Değişmeyecek INVARIANT'lar
- Mevcut testler hâlâ geçer.
- Auth akışı ve `/health` ucu limit DIŞI kalır (kesintisiz izleme).
- Yanıt gövdesi şemaları değişmez.

## Kapsam sınırı
- Kalıcı/dağıtık limit deposu (Redis vb.) YOK — tek instance, bellek-içi sayaç.
- Kullanıcı-bazlı kota / faturalama YOK.

## Başarı Kriteri
- [ ] **BK1** Given aynı istemciden dakikada 61. istek, When limit aşılır, Then 429 + `Retry-After` başlığı döner · doğrulayıcı: [kod]
- [ ] **BK2** Given mevcut test suite'i, When limiter eklendikten sonra koşulur, Then tamamı geçer ve `/health` limitsiz 200 döner · doğrulayıcı: [kod]

## Adımlar
1. **Limiter middleware** — bellek-içi sliding-window sayaç; `/api/*`'a takılır, `/health` hariç tutulur.
   - Doğrulama: birim test — 60 istek OK, 61. istek 429 + `Retry-After`.
   - Karşıladığı kriter: → BK1
   - commit: `api: rate limit middleware`
2. **Invariant güvencesi** — tam suite + `/health` limitsizlik testi.
   - Doğrulama: CI yeşil; `/health`'e 100 ardışık istek, hepsi 200.
   - Karşıladığı kriter: → BK2
   - commit: `api: limit invariant testleri`
