<!--
  DESIGN.md — Nasıl Kurulu?  ·  Soru: NASIL KURULU?
  İki bölüm: (A) Mimari Kararlar — HER ZAMAN.  (B) Tasarım Dili — sadece UI varsa.
  Otorite: DESIGN = teknik hakem. PLAN/CLAUDE/DESIGN teknik çelişirse DESIGN kazanır
  (ama INTENT amacını asla ezemez).  "Başkasının DESIGN.md'si performans vermez → İÇSELLEŞTİR."
  Yazınca bu yorum bloklarını sil.
-->

# DESIGN — <Proje / Feature Adı>

## A. Mimari Kararlar
<!-- Her karar ADR-lite: ne · neden · neden diğeri değil. INTENT hedefini taşımalı. -->

### <Karar 1 — örn. "Stack seçimi">
- **Karar:** <doldur>
- **Gerekçe:** <doldur — hangi başarı kriterini/sınırı taşıyor>
- **Neden diğeri değil:** <eleştirilen alternatif + ret nedeni>

### <Karar 2 — örn. "Veri modeli / akış">
- **Karar:** <doldur>
- **Gerekçe:** <doldur>
- **Neden diğeri değil:** <doldur>

<!-- Sınırlar/katmanlar, kilit trade-off'lar, entegrasyonlar… gereği kadar karar ekle. -->

---

## B. Tasarım Dili
<!-- SADECE UI projesiyse. Format: google-labs-code/design.md (token + prose).
     Token'lar AJANA tam değer verir; prose NEDEN'ini anlatır.
     Genel değil — PROJEYE ÖZEL palet/font seç (içselleştir). UI yoksa bu bölümü sil. -->

### Token'lar
<!-- (Saf bir tasarım-sistemi dosyasında bunlar YAML front-matter olurdu; burada mimariyle
     birlikte yaşadığı için yaml bloğu olarak gömülü. Referans sözdizimi: {colors.primary}) -->
```yaml
name: <Tema Adı>
colors:
  primary: "<#hex / oklch(...)>"
  secondary: "<#hex>"
  tertiary: "<#hex>"        # tek vurgu/etkileşim rengi
  neutral: "<#hex>"         # zemin
typography:
  h1:    { fontFamily: "<Başlık fontu>", fontSize: "3rem",   fontWeight: 700 }
  body-md: { fontFamily: "<Gövde fontu>", fontSize: "1rem",  lineHeight: 1.5 }
  mono:  { fontFamily: "<Mono font>",   fontSize: "0.875rem" }
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
```

### Prose (token'ların NEDEN'i — sıralı bölümler)
<!-- google-labs kanonik sıra; gereksizleri sil. Her bölüm token kararının gerekçesi. -->
- **Overview:** <genel tasarım tavrı / hissi — "statement", minimal vb.>
- **Colors:** <her rengin rolü; neden bu palet>
- **Typography:** <başlık/gövde/mono seçimi ve nedeni>
- **Layout & Spacing:** <ritim, ızgara, yoğunluk>
- **Components:** <kilit bileşenlerin davranışı/varyantları>
- **Do's & Don'ts:** <yapılacak (✔) / kaçınılacak (✗)>
