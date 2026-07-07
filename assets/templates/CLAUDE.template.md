<!--
  CLAUDE.md — Proje Anayasası  ·  Soru: HANGİ KURALLARLA?
  Her oturumda OTOMATİK yüklenir. Projenin kalıcı bağlamı + davranış sözleşmesi.
  4 prensip (Karpathy): ① kuralı açık yaz (modele bırakma) ② yasağı açık yaz
  ("Yapma" > "Yap") ③ yeni kararı HEMEN ekle (bayat CLAUDE.md = bayat cevap)
  ④ tek dosya / tek kaynak.   Yazınca bu yorum bloklarını sil.
-->

# Proje
<!-- 1-2 cümle. INTENT/Hedef ile uyumlu. -->
<doldur>

# Stack
<!-- Diller, framework'ler, araçlar, servisler. DESIGN.md ile BİREBİR aynı olmalı. -->
- <doldur>

# Kurallar
<!-- Kod / komut / akış kuralları — AÇIK yaz, modele bırakma. -->
- **Think before coding:** varsayma; belirsizliği yüzeye çıkar, gerekirse SOR.
- **Simplicity first:** isteneni çöz; spekülatif özellik / gereksiz soyutlama yok.
- **Surgical changes:** sadece gerekeni değiştir; mevcut stile uy, alakasız yeri refactor etme.
- **Goal-driven:** muğlak isteği test edilebilir başarı kriterine çevir, doğrulanana dek döngüle.
- **Commit:** `<scope>: <açıklama>` (paketli iş başına; conventional-commit değil, scope öne).
- **Hafıza:** oturum başında `MEMORY.md`'yi oku; her paketli işten sonra sor: "MEMORY'e yazılacak var mı?" — kesinleşen karar → semantic, olay/çözülen çelişki → episodic (tarih-damgalı), tekrarlanabilir kalıp → procedural (tetik→koşul→aksiyon).
- **Test/çalıştırma:** <proje-özel kural>
- <ekle…>

# Yapma
<!-- AÇIK yasaklar. INTENT/Kapsam-dışı'nı buraya güçlendirerek taşı. "Yapma" en güçlü komuttur. -->
- <doldur>

---
<!-- Alttaki Çatışma kuralı satırı AYNEN KALIR; bu yorum bloğu ise silinir: -->
> **Çatışma kuralı:** Dosyalar teknik konuda çelişirse **DESIGN.md kazanır.** INTENT (amaç/hedef/kapsam-dışı) ise hiçbir dosyanın çiğneyemeyeceği kuzey yıldızıdır.
