<!--
  PLAN.md — Uygulama Sırası  ·  Soru: HANGİ SIRAYLA?
  INTENT'i çalıştırılabilir, ATOMİK, doğrulanabilir adımlara böler.
  Kural: her başarı kriteri ≥1 adımla karşılanır; kapsam-dışına giren adım YOK.
  Her adım = tek "paketli iş" = tek commit (scope: açıklama).
  Yazınca bu yorum bloklarını sil.
-->

# PLAN — <Proje / Feature Adı>

> Hedef (INTENT'ten): <tek cümle hedefi buraya kopyala — hizalama çapası>

## Adımlar
<!-- Her adım: NE yapılacak + NASIL doğrulanacak. Mümkünse localhost'ta ayağa kaldır / test yaz.
     Adımları bağımlılık sırasına diz. Karşıladığı başarı kriterini → ile işaretle. -->

1. **<adım adı>** — <ne yapılacak>
   - Doğrulama: <nasıl test edilir / hangi çıktı görülür>
   - Karşıladığı kriter: → BK1
   - commit: `<scope>: <açıklama>`

2. **<adım adı>** — <ne yapılacak>
   - Doğrulama: <…>
   - Karşıladığı kriter: → BK2
   - commit: `<scope>: <açıklama>`

<!-- Karşıladığı kriter DAİMA "→ BK#" biçiminde (INTENT'teki kimlik) — kickoff-verify
     mekanik eşler: her BK ≥1 adımda karşılanmalı, her adım geçerli bir BK'ye işaret etmeli. -->

<!-- … gereği kadar adım. Belirsiz teknik seçim çıkarsa /ai-proje-rehberi'ye danış. -->

## Kapsam-dışı bekçisi
<!-- INTENT/Kapsam-dışı'nı buraya yapıştır; hiçbir adımın buraya girmediğini doğrula. -->
- <INTENT kapsam-dışı maddesi> — plana SIZMADI ✔

## Doğrulama özeti
<!-- Tüm adımlar bitince hedefin karşılandığını nasıl bütünsel doğrularız? -->
- <doldur>
