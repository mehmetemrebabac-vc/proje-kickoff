# CLAUDE.md Playbook — Proje Anayasası

> Soru: **Hangi kurallarla?** Her oturumda **otomatik yüklenen** kalıcı bağlam — projenin "anayasası" + davranış sözleşmesi.

## 4 Prensip (Karpathy — birebir özü)
1. **Think Before Coding** — *varsayma; belirsizliği gizleme, yüzeye çıkar; gerekirse SOR.* (Kuralı **açık** yaz, modele bırakma.)
2. **Simplicity First** — *problemi çözen minimum kod; spekülatif özellik / gereksiz soyutlama / sorulmamış esneklik yok.*
3. **Surgical Changes** — *sadece gerekene dokun; mevcut stile uy; bozuk olmayanı refactor etme; yalnızca kendi açtığın dağınıklığı topla.*
4. **Goal-Driven Execution** — *muğlak isteği test edilebilir başarı kriterine çevir, doğrulanana dek döngüle.* ("Validation ekle" → "geçersiz girdilere test yaz, sonra geçir".)
> Ayrıca: **yasakları açık yaz** ("Yapma" > "Yap") · **yeni kararı hemen ekle** (bayat CLAUDE.md = bayat cevap) · **tek dosya/tek kaynak.**

## Bölümler
- `# Proje` — 1-2 cümle, **INTENT hedefiyle uyumlu.**
- `# Stack` — diller, framework, araçlar; **DESIGN.md ile birebir aynı** (sapma = çelişki).
- `# Kurallar` — kod/komut/akış kuralları. Commit: **`<scope>: <açıklama>`** (paketli iş başına; conventional-commit *değil*, scope öne — örn. `auth: refresh token süresini uzat`, `api: /users endpoint'i ekle`). Test/çalıştırma kuralları. **Hafıza kuralı** (şablonda hazır — SİLME): MEMORY döngüsünü kodlama fazında canlı tutan tek yer burasıdır; CLAUDE.md oto-yüklenir, MEMORY.md yüklenmez.
- `# Yapma` — açık yasaklar; **INTENT/Kapsam-dışı'nı buraya güçlendirerek taşı.**
- **Çatışma kuralı (yaz):** dosyalar teknik konuda çelişirse **DESIGN.md kazanır**; INTENT (amaç) kuzey yıldızıdır, ezilemez.
- **Katman eleme (her aday kural için):** *"bu her oturumda mı geçerli, yoksa bu göreve mi özgü?"* — göreve özgüyse CLAUDE'a değil PLAN/INTENT'e yönlendir (kalıcı kimlik ↔ göreve-özgü ayrımı; KB *System Prompt Tasarımı*).
- **Enflasyon lint'i:** MUST/CRITICAL/ASLA'yı yalnız gerçek yasaklara sakla — bağırılan kural aşırı-tetiklenir; her yasağın yanına *nedenini* yaz. Taslak-onay döngüsünde buda: her cümle bir davranışı değiştirmiyorsa sil (KB *Meta-Prompting*).

## Tutarlılık geçidi (`references/tutarlilik.md §3`, INTENT/PLAN↔CLAUDE)
- [ ] `# Proje` INTENT hedefini yansıtıyor mu?
- [ ] `# Stack` PLAN adımlarının gerektirdiğini kapsıyor mu?
- [ ] `# Kurallar`/`# Yapma` PLAN adımlarıyla veya hedefle çelişmiyor mu?
- [ ] `# Yapma` kapsam-dışını güçlendiriyor mu (çürütmüyor)?

## Çıktı
Proje kökünde `CLAUDE.md`. **Yazınca deftere damıt** (UYGULAMA katmanı). **Şablon:** `assets/templates/CLAUDE.template.md` (memory-collision için `.template` ekli; mevcut `CLAUDE.md` varsa ASLA tam-overwrite — `references/akis-modlari.md §3` ile birleştir). **Kaynak:** KB *5-Dosya Workflow'u* + *Karpathy Claude Code Kuralları* (4 prensip) + *AI Kodlamada Commit Disiplini* (scope-prefixed commit).
