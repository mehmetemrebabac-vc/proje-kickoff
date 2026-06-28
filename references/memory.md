# MEMORY.md Playbook — Oturumlar Arası Hafıza

> Soru: **Neyi hatırlıyor?** Oturumlar arası kalan karar & öğrenmeler. (`agentmemory` 4-katman yapısı.) Tutarlılıkta **AYNA katmanı**: hiçbir şey belirlemez; diğer 4 dosyanın **kesin** kararlarını doğru yansıtır (eski/çelişen karar taşımaz → `references/tutarlilik.md §1`, §3 "hepsi↔MEMORY").

## 4 Katman (+ somut dosya düzeni)
Kök `MEMORY.md` bir **indeks**tir; büyüyen içerik `memory/` alt-klasörlerine taşınır.
- **working** — şu anki aktif bağlam (güncel PLAN adımı / açık iş) → `memory/working/current.md`
- **episodic** — ne oldu, ne zaman (tarih-damgalı, **append-only**; çözülen çelişkiler buraya) → `memory/episodic/<tarih>.md`
- **semantic** — kalıcı gerçekler/kararlar (proje hakkında değişmez bilgi)
- **procedural** — "nasıl-yapılır" kalıpları (tekrarlayan işlemler / reusable yordamlar)

## Katman eşlemesi (ayna kuralı)
`semantic` ← INTENT/DESIGN kesin gerçekleri · `procedural` ← CLAUDE kuralları · `episodic` ← çözülen çelişkiler · `working` ← güncel PLAN adımı.

## Çalışma kuralı
CLAUDE.md + MEMORY.md **birlikte**: her prompt sonunda *"MEMORY'e bir şey yazılmalı mı?"* kararı verilir. Kararlar episodic+semantic'e, öğrenilen kalıplar procedural'a.

## Tutarlılık geçidi (`references/tutarlilik.md §3`)
- [ ] `semantic` INTENT/DESIGN kararlarıyla çelişmiyor mu (eski karar taşımıyor mu)?
- [ ] `working` güncel PLAN adımını yansıtıyor mu?
- [ ] `procedural` CLAUDE `# Kurallar`'ın bir kopyası/uzantısı mı (çelişki yok)?

## Çıktı
Proje kökünde `MEMORY.md` (+ gerekirse `memory/` alt-klasörleri). **Şablon:** `assets/templates/MEMORY.md`. **Kaynak:** KB *5-Dosya Workflow'u* + *RAG, Fine-Tuning, Memory & Guardrails — Karar Çerçevesi* (4-katman memory).
