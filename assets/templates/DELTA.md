<!--
  DELTA change-spec  ·  Soru: NEYİ, NEYİ BOZMADAN DEĞİŞTİRİYORUZ?
  BROWNFIELD-DELTA modunun tek dosyası (5 dosya YAZILMAZ). Hedef: docs/specs/<feature>.md
  Otorite: "Hedef delta + Kapsam sınırı" bölümleri AMAÇ katmanıdır (kuzey yıldızı) —
  hiçbir adım/karar bunları çiğneyemez (tutarlilik.md §1 aynen geçerli).
  Kısa tut (≤1 sayfa). Yazınca bu yorum bloklarını sil.
-->

# DELTA — <Feature / Fix Adı>

## Mevcut davranış
<!-- Bugün sistem ne yapıyor? (Keşif fazından — koddan doğrulanmış, tahmin değil.) -->
<doldur>

## Hedef delta
<!-- TEK cümle: bu değişiklik bitince ne FARKLI olacak? Çözümü değil sonucu yaz. -->
<doldur — tek cümle>

## Değişmeyecek INVARIANT'lar
<!-- Bu iş sırasında BOZULMAYACAK mevcut davranış/kontratlar. "Mevcut testler geçer" daima ilk satır. -->
- Mevcut testler hâlâ geçer.
- <doldur — API kontratı / davranış / performans sınırı>

## Kapsam sınırı
<!-- Bu değişikliğin BİLEREK dokunmadığı yerler. Boş bırakma. -->
- <doldur>

## Başarı Kriteri
<!-- BK# kimlikli, GWT-demirli, sayılabilir. Doğrulayıcı sınıfı: [kod|judge|insan] — [kod]a it. -->
- [ ] **BK1** Given <durum>, When <eylem>, Then <ölçülebilir sonuç> · doğrulayıcı: [kod]
- [ ] **BK2** Given <mevcut akış>, When <değişiklik sonrası>, Then <invariant korunur> · doğrulayıcı: [kod]

## Adımlar
<!-- Atomik, bağımlılık sıralı; her adım → BK#'ye demirli, tek commit. -->
1. **<adım>** — <ne yapılacak>
   - Doğrulama: <nasıl test edilir>
   - Karşıladığı kriter: → BK1
   - commit: `<scope>: <açıklama>`
