<!--
  MEMORY.md — Neyi Hatırlıyor?  ·  Soru: NEYİ HATIRLIYOR?
  Oturumlar arası kalan karar & öğrenmeler. 4-katman (agentmemory).
  Otorite: MEMORY = AYNA katmanı — hiçbir şeyi belirlemez; diğer 4 dosyanın KESİN
  kararlarını doğru yansıtır. Eski/çelişen karar taşıma.
  Bu kök dosya bir İNDEKS; büyüyen içerik memory/ alt-klasörlerine taşınır.
  Çalışma kuralı: CLAUDE.md + MEMORY.md birlikte — her prompt sonunda
  "MEMORY'e bir şey yazılmalı mı?" kararı verilir.   Yazınca bu yorum bloklarını sil.
-->

# MEMORY — <Proje / Feature Adı>

## working — şu anki aktif bağlam
<!-- Üzerinde çalışılan güncel PLAN adımı / açık görev. Kısa ömürlü, sık güncellenir. -->
- Aktif adım: <PLAN/Adım-n>
- Açık iş: <doldur>
- Ayrıntı dosyası: `memory/working/current.md`

## episodic — ne oldu, ne zaman
<!-- Tarih-damgalı olay/karar günlüğü (append-only). Çözülen çelişkiler buraya. -->
- <YYYY-AA-GG>: <ne oldu / hangi karar verildi>
- Günlükler: `memory/episodic/<tarih>.md`

## semantic — kalıcı gerçekler & kararlar
<!-- Proje hakkında değişmez bilgi. Kaynak: INTENT + DESIGN kesin kararları. -->
- <gerçek/karar> (kaynak: INTENT/DESIGN)

## procedural — nasıl-yapılır kalıpları
<!-- Tekrarlayan işlemler / reusable yordamlar. Kaynak: CLAUDE.md kuralları.
     Format: tetik → koşul → aksiyon (taklit edilebilir olsun; KB *Hafıza Taksonomisi*). -->
- <tetik: ne olduğunda> → <koşul: hangi durumda> → <aksiyon: ne yapılır / hangi komut>

---
<!-- Tutarlılık: bu dosya yukarıdaki katman-eşlemesini izler — semantic←INTENT/DESIGN,
     procedural←CLAUDE, episodic←çözülen çelişkiler, working←güncel PLAN adımı. -->
