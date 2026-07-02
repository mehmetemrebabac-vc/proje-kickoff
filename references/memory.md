# MEMORY.md Playbook — Oturumlar Arası Hafıza

> Soru: **Neyi hatırlıyor?** Oturumlar arası kalan karar & öğrenmeler. (`agentmemory` 4-katman yapısı.) Tutarlılıkta **AYNA katmanı**: hiçbir şey belirlemez; diğer 4 dosyanın **kesin** kararlarını doğru yansıtır (eski/çelişen karar taşımaz → `references/tutarlilik.md §1`, §3 "hepsi↔MEMORY").

## 4 Katman (+ somut dosya düzeni)
Kök `MEMORY.md` bir **indeks**tir; büyüyen içerik `memory/` alt-klasörlerine taşınır.
- **working** — şu anki aktif bağlam (güncel PLAN adımı / açık iş) → `memory/working/current.md`
- **episodic** — ne oldu, ne zaman (tarih-damgalı, **append-only**; çözülen çelişkiler buraya) → `memory/episodic/<tarih>.md`
- **semantic** — kalıcı gerçekler/kararlar (proje hakkında değişmez bilgi)
- **procedural** — "nasıl-yapılır" kalıpları, **tetik→koşul→aksiyon** formatında (taklit edilebilir olsun; tekrarlayan işlemler / reusable yordamlar)

## Katman eşlemesi (ayna kuralı)
`semantic` ← INTENT/DESIGN kesin gerçekleri · `procedural` ← CLAUDE kuralları · `episodic` ← çözülen çelişkiler · `working` ← güncel PLAN adımı.

## Çalışma kuralı
CLAUDE.md + MEMORY.md **birlikte**: her paketli iş sonunda *"MEMORY'e bir şey yazılmalı mı?"* kararı verilir. Kararlar episodic+semantic'e, öğrenilen kalıplar procedural'a. **Bu kural üretilen `CLAUDE.md # Kurallar`'da yaşar** (şablonda hazır) — çünkü kodlama fazında oto-yüklenen tek dosya CLAUDE.md'dir; kural yalnız burada (skill tarafında) kalsaydı devirden sonra hiçbir oturuma yüklenmez, MEMORY ilk günden bayatlar.

## Sınır — MEMORY.md ↔ diğer hafıza mekanizmaları
`MEMORY.md` = **dosya-tabanlı, repo-içi PROJE hafızası** (bu projenin kararları/kalıpları; repo ile taşınır). Claude Code'un kullanıcı-seviyesi kalıcı hafızası veya `agentmemory` (MCP) gibi mekanizmalar **kullanıcı/oturum-düzeyi** hafızadır — ikame değil, katmandır; aynı 4-katman taksonomiyi izlerler. Röportajda sor: *"dosya-tabanlı MEMORY.md yetiyor mu, yoksa oturumlar-arası yoğun hafıza ihtiyacı var mı (→ agentmemory)?"* Vektör-DB'li hafıza isteği gelirse: küratörlü küçük korpus için index-first yeter, vektör altyapısı erken optimizasyondur (→ KB *RAG vs Index-First — Ne Zaman Hangisi?*).

## Tutarlılık geçidi (`references/tutarlilik.md §3`)
- [ ] `semantic` INTENT/DESIGN kararlarıyla çelişmiyor mu (eski karar taşımıyor mu)?
- [ ] `working` güncel PLAN adımını yansıtıyor mu?
- [ ] `procedural` CLAUDE `# Kurallar`'ın bir kopyası/uzantısı mı (çelişki yok)?

## Çıktı
Proje kökünde `MEMORY.md` (+ gerekirse `memory/` alt-klasörleri). **Şablon:** `assets/templates/MEMORY.md`. **Kaynak:** KB *5-Dosya Workflow'u* + *Hafıza Taksonomisi — Working, Episodic, Semantic, Procedural* (kanonik 4-katman çapası) + *agentmemory* (dosya-tabanlı uygulamanın MCP kuzeni).
