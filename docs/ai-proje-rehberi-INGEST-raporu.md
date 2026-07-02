# INGEST Raporu — SDD & Scaffold/Handoff/Resume Bilgisi (ai-proje-rehberi için)

> **Bu nedir:** `proje-kickoff` skill'inin 5 zayıflığı üzerine yapılan 6-alan derin araştırmanın (46 repo taranmış) damıtılmış ürünü. Amaç: vault'a (**ai-proje-rehberi**) eklenebilecek YENİ/değerli bilgiyi sana hazır sunmak. **Hepsi ÖNERİDİR** — INGEST kaynak-değerlendirme motorundan geçir, **öner→onay→ekle**. Vault'ta grep ile doğrulandı: SDD / spec-kit / openspec / bmad / brownfield / greenfield / handoff / resume / scaffold-conflict konularının **hiçbiri mevcut değil**.
> Üretildiği oturum: proje-kickoff skill güçlendirmesi (adversarial inceleme → derin araştırma → yama). Skill repo'su: `~/.claude/skills/proje-kickoff/` (vault dışı).

---

## 1. Önerilen YENİ notlar (öncelikli, deduplike)

> 6 araştırma bloğunda spec-kit ~5, brownfield ~4, handoff/resume ~3 kez tekrar etti → tek kanonik nota birleştirildi. Kalite barını geçemeyen yüzeysel adaylar (cc-sdd, lean-spec, Tessl, Conductor) elendi.

### A. Spec-Driven Development (SDD) — Spec Kit · OpenSpec · BMAD · Agent OS Karşılaştırması
- **Kategori:** Claude Code & Kodlama Ajanları
- **Tag'ler:** `claude-code` `workflow` `orkestrasyon` `agent` `spec-driven` `mimari`
- **Neden değerli:** Kullanıcının `proje-kickoff` skill'inin ve `5-Dosya Workflow'u` notunun tam içine düştüğü, 2025-2026'nın en hızlı büyüyen kodlama-ajanı kategorisi (Spec Kit ~93-116k★, OpenSpec 57k★, BMAD 50k★). Ortak omurga (`constitution/spec → plan → tasks → implement`) + `constitution.md ≡ INTENT` eşlemesi + `/speckit.converge` (brownfield re-entry) doğrudan skill'i besler. `5-Dosya Workflow'u`'nu dış-dünya bağlamına oturtur (mükerrer değil; o dosyaları, bu *framework ailesini* anlatır).
- **Kaynak URL:** https://github.com/github/spec-kit
- **Öz:** SDD niyeti (spec) birincil kaynak yapıp kodu ondan üretir; her faz diske yazılan Markdown artefaktı olur. Spec Kit resmi/ağır (constitution→specify→clarify→plan→tasks→implement + insan-review kapıları), OpenSpec hafif/brownfield-first (delta-spec), BMAD çok-ajanlı agile (story-sharding), Agent OS 3-katman (Standards/Product/Specs). Hepsi durumu git'lenebilir düz dosyada tutar, fazlar arası insan-onayı şart koşar.

### B. Brownfield vs Greenfield — Spec/Plan Stratejisi
- **Kategori:** Claude Code & Kodlama Ajanları
- **Tag'ler:** `spec-driven` `workflow` `claude-code` `brownfield` `greenfield` `guardrails`
- **Neden değerli:** AI-kodlamanın en kritik kör-noktası; iki-mod ayrımı endüstri standardı: greenfield=spec'i sıfırdan doldur; brownfield=ÖNCE mevcut mimariyi belgele, var-olanı KİLİTLE, yalnızca DELTA'yı spec'le. `5-Dosya`'nın greenfield-örtük varsayımını tamamlar.
- **Kaynak URL:** https://www.augmentcode.com/guides/spec-driven-development-brownfield-codebases
- **Öz:** Brownfield'de sıra tersine döner: greenfield "spec→kod", brownfield "kod→keşif-belgesi→spec". Change-level spec'in 4 öğesi: mevcut davranış · hedef delta · değişmeyecek invariant · kapsam-sınırı. Tam-pipeline yalnızca büyük yeni alt-sistem için; bugfix/feature/refactor için change-level spec. Mevcut config (CLAUDE.md) **birleştirilir, ezilmez.**

### C. Spec→Implementation Devri (Handoff) — Temiz-Context'e Geçiş
- **Kategori:** Claude Code & Kodlama Ajanları
- **Tag'ler:** `claude-code` `context` `workflow` `loop-engineering` `agent` `orkestrasyon`
- **Neden değerli:** Genel AI-kodlama disiplini; 3 bağımsız resmi kaynak aynı kalıbı söylüyor. `5-Dosya` ve `Loop Engineering` notlarını tamamlar (geçiş ritüeli).
- **Kaynak URL:** https://code.claude.com/docs/en/best-practices
- **Öz:** Spec/plan bitince TAZE oturumda (yalnızca spec context'i) uygulamaya geç — Claude Code'da plan-kabul sonrası context temizliği `showClearContextOnPlanAccept` ayarına bağlı OPSİYONELDİR (default kapalı) — bu yüzden devirde AÇIK `/clear` emri verilir ("eski keşif çöpü plan-adherence'ı bozar"). İyi spec self-contained handoff kontratıdır: dosya/arayüz adları + kapsam-dışı + uçtan-uca doğrulama. Hiyerarşik context çıkarımı (Description→Acceptance→Design) = INTENT→PLAN→DESIGN hiyerarşisi.

### D. Agentic Resumability — Diske Yazılan Durum & Oturum-Arası Re-entry
- **Kategori:** AI Sistemleri Mimari & Otomasyon
- **Tag'ler:** `agent` `loop-engineering` `memory` `context` `orkestrasyon` `workflow`
- **Neden değerli:** Her uzun/çok-oturumlu ajan işi için cross-cutting mimari. `Ralph`, `Loop Engineering`, `Kalıcı Hafızalı AI Çalışan` notlarına hub.
- **Kaynak URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Öz:** Yakınsak kalıp: context EFEMERAL/amnezik kabul edilir; kalıcı durum DİSKTE düz, sürüm-kontrollü dosyalarda yaşar; resume = sabit oturum-başı protokolüyle bu dosyaları (+git log) yeniden okuyup "neredeyiz"i türetmek. Küçük makine-okunur STATUS işareti (Anthropic JSON'u Markdown'a tercih etti: model JSON'u yanlışlıkla ezmeye daha az meyilli) + append-only progress log + git history.

### E. Scaffold Çatışma Çözümü — Var-Olan Dosyayla Güvenli Birleşme
- **Kategori:** Claude Code & Kodlama Ajanları
- **Tag'ler:** `claude-code` `scaffold` `conflict-resolution` `claude-md` `workflow` `guardrails`
- **Neden değerli:** Vault'un "çelişki=işaretle, üzerine yazma" INGEST ilkesinin dosya-sistemi düzeyindeki somut karşılığı. Olgun scaffold araçlarının HİÇBİRİ sessiz ezmez — kanıtlı UX/güvenlik kalıbı.
- **Kaynak URL:** https://yeoman.github.io/generator/4.x/Conflicter.html
- **Öz:** Altın standart Yeoman Conflicter: yazmadan önce diskteki içerikle karşılaştır → identical→sessiz atla, farklıysa per-file `[Ynaxdh]` + DIFF'i overwrite'tan ÖNCE göster. copier `.copier-answers.yml` + 3-yönlü merge, çatışmayı git-marker/.rej ile yüzeye çıkarır. Spec Kit kategori-tabanlı koruma; `constitution.md` force-ezme bug'ı "karma dosya (CLAUDE.md) asla tam-overwrite edilmemeli" dersi. Claude Code `/init` de var-olan CLAUDE.md'yi ezmez, iyileştirir.

### F. EARS Notasyonu — Test Edilebilir Gereksinim/Kabul Kriteri (Kiro)
- **Kategori:** Prompt Teknikleri
- **Tag'ler:** `prompt-teknigi` `workflow` `spec-driven` `guardrails`
- **Neden değerli:** Kısa, yüksek-kaldıraçlı. INTENT'in "sayılabilir başarı kriteri" ve PLAN'ın "doğrulanabilir adım" kapılarına reçete. `Prompt Zanaatı — Ölçülebilir Rol` notu var ama gereksinim/kabul-kriteri tarafı yok (tamamlayıcı).
- **Kaynak URL:** https://kiro.dev/docs/specs/
- **Öz:** EARS (Easy Approach to Requirements Syntax), Kiro'nun `requirements.md`'de kullandığı kalıplı sözdizimi ("WHEN <tetik>, THE SYSTEM SHALL <davranış>"). Kabul kriterlerini test edilebilir/ölçülebilir yazmaya zorlar; koddan üretilen spec'lerin niyetten sapması (alignment loss) riskini azaltır.

---

## 2. Mevcut notları zenginleştirme önerileri (yeni not GEREKMEZ)

- **`Ralph — Otonom Agentic Kodlama Loop'u (prd.json)`** → `prd.json + progress.txt + git history` modelinin **endüstri-default resumability kalıbı** olduğuna çapraz-ref (Anthropic harness, Spec Kit converge, Task Master next). Yeni Not D'ye link; BMAD story-sharding ile karşılaştırma (tek-orkestratör vs çok-ajan agile).
- **`5-Dosya Workflow'u (INTENT, PLAN, CLAUDE, DESIGN, MEMORY)`** → Greenfield-örtük olduğunu işaretle; Not B (brownfield çatalı) + Not A (SDD ailesi) linki. `constitution.md ≡ INTENT`, `tasks.md ≡ PLAN` eşlemesi.
- **`Loop Engineering — Prompting'den Loop Tasarımına`** → Not C (handoff/fresh-context) + Not D (resumability) bağı; verifier-kapalı `commit→test→düzelt`'in handoff-sonrası ilk adım olduğu.
- **`Gelişmiş Skill Mühendisliği …`** + **`Claude Skills (Agent Skills) — Tam Rehber`** → (a) progressive disclosure 3-seviye + references-read imperatifi ("Claude işaret edilmeden referans okumaz"); (b) **CLAUDE.md filename-collision uyarısı** — `assets/templates/CLAUDE.md` adlı dosya memory-special yüklenir; `.template.md` ekiyle yeniden adlandır. (Bu skill iterasyonunda uygulandı.)
- **`Kalıcı Hafızalı "AI Çalışan" Sistemi`** → supersession kalıbı (`is_latest=false`, silme yerine işaretle) + episodic append-only; vault'un "çelişki=işaretle, üzerine yazma"sının hafıza-mekanik karşılığı.

---

## 3. Keşfedilen repo/araç dizini (46 → en uygun 13)

| Ad | URL | Bir cümle | Uygunluk |
|---|---|---|---|
| github/spec-kit | https://github.com/github/spec-kit | Resmi SDD toolkit: constitution→specify→plan→tasks→implement, her faz Markdown artefaktı. | Not A/B/C kanonik. |
| Fission-AI/OpenSpec | https://github.com/Fission-AI/OpenSpec | Hafif brownfield-first SDD: delta-spec + propose→apply→archive; `/opsx:continue` resume. | Not A/B/D/E; skill felsefesine en yakın. |
| bmad-code-org/BMAD-METHOD | https://github.com/bmad-code-org/BMAD-METHOD | Çok-ajan agile SDD; story-sharding + `document-project` brownfield keşfi. | Not A/B; handoff altın standardı. |
| buildermethods/agent-os | https://github.com/buildermethods/agent-os | 3-katman SDD; mevcut dosya bulunca SORAR, `discover-standards`. | Not B; CLAUDE/INTENT/DESIGN ile yapısal eşleşme. |
| copier-org/copier | https://copier.readthedocs.io/en/stable/updating/ | `.copier-answers.yml` + 3-yönlü merge; asla sessiz ezmez. | Not E; brownfield re-run + state-record. |
| yeoman Conflicter | https://yeoman.github.io/generator/4.x/Conflicter.html | Scaffold conflict UX altın standardı: identical→skip, farklıysa `[Ynaxdh]`+diff. | Not E; kör-overwrite kalıbı. |
| anthropics/skills | https://github.com/anthropics/skills | Resmi Agent Skills repo'su: SKILL.md + references/ + scripts/ + assets/. | Skill-authoring zenginleştirme. |
| eyaltoledano/claude-task-master | https://github.com/eyaltoledano/claude-task-master | PRD→tasks.json + `state.json`; `task-master next` status+deps. | Not D; "resume=next-from-status". |
| obra/superpowers | https://github.com/obra/superpowers | Claude Code skill framework'ü: brainstorm→plan→subagent-dev. | Skill mekaniği zenginleştirme. |
| Anthropic long-running harness | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Initializer/coding ajan ayrımı + progress.txt + re-read protokolü. | Not D authoritative zemin. |
| Kiro (AWS) | https://kiro.dev/docs/specs/ | Spec-driven IDE; requirements.md'yi EARS notasyonuyla üretir. | Not F; ölçülebilir-kriter reçetesi. |
| wcpaxx/spec-kit-brownfield-extensions | https://github.com/wcpaxx/spec-kit-brownfield-extensions | Mevcut koddan tech-stack türetip constitution üretir. | Not B; constitution-from-code. |
| zhimin-z/Awesome-Spec-Driven-Development | https://github.com/zhimin-z/Awesome-Spec-Driven-Development | 25+ SDD aracının küratörlü listesi. | Gelecek INGEST için meta-keşif. |

---

## 4. Ekleme protokolü (hatırlatma)
Her adayı vault INGEST motorundan geçir: damıt → adversarial doğrula → skor-kartı (≥70 KABUL) → uyum/çelişki tara → `_sources/` ham kaydı → **öner→onay→ekle** → ≥1 karşılıklı bağ + MOC + Index → `python3 <vault>/scripts/kb-verify.py` TEMİZ ✅ (script v4'ten beri vault repo'sunda yaşar). **Birleştirme uyarısı:** A (SDD), B (brownfield), E (scaffold-conflict) içerik komşusu — aralarında çapraz-ref kur, tekrarı önle.
