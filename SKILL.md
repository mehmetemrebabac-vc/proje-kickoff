---
name: proje-kickoff
disable-model-invocation: true
description: >-
  Yeni bir proje/feature'a BAŞLAMADAN ÖNCE 5 temel .md dosyasını (INTENT, PLAN,
  CLAUDE, DESIGN, MEMORY) uçtan uca, soru-cevapla, titizlikle tasarlayıp oluşturan
  proje-başlatma orkestratörü. Boş bir chat'te /proje-kickoff ile çağrılır; 5 dosyayı
  sırayla, her birini gerektiği kadar derinlikte, birbiriyle TUTARLI olacak şekilde
  kurar. KULLANMA: mevcut projede tek dosya düzenleme, hızlı soru, bilgi danışma
  (onun için /ai-proje-rehberi).
metadata:
  version: 1.0.0
---

# Proje Kickoff — 5-Dosya Orkestratörü

> **Bu UZUN, çok-mesajlı bir oturumdur.** `/proje-kickoff` ile başlar; 5 dosya (INTENT → PLAN → CLAUDE → DESIGN → MEMORY) eksiksiz kurulana kadar **aynı chat'te** sürer. Acele yok.
> Temel bilgi: KB *5-Dosya Workflow'u (INTENT, PLAN, CLAUDE, DESIGN, MEMORY)*. Bilgi/yaklaşım danışmak ≠ bu skill → onun için `/ai-proje-rehberi`.

## Çekirdek ilkeler (HARD — asla ihlal etme)
1. **Titizlik > hız.** Her dosyayı **tek tek, başlık başlık, derinlemesine** tasarla. Gereken kadar mesaj harca (300 olsa da). Gerekirse **50 repo/kaynak araştır** (WebFetch/`git clone` + incele) ya da `/ai-proje-rehberi`'ye danış. **Yüzeysel şablon-doldurma YASAK.**
2. **Tutarlılık motoru (kalp).** Her yeni cevap/dosya, **öncekilerle teyitlenir** — geçmişe karşı doğrulanır, paralel/uyumlu tutulur. Çelişki çıkarsa **işaretle + çöz** (üzerine yazma). Hiyerarşi iki katmanlıdır: **INTENT = kuzey yıldızı (AMAÇ — dikey üst-otorite, hiçbir dosya çiğneyemez)**; PLAN/CLAUDE/DESIGN *teknik* çelişirse **DESIGN.md kazanır (yatay hakem)** — ama INTENT amacını asla ezemez. Motor: `references/tutarlilik.md` — **her `YAZ`dan önce pre-write gate'i çalıştır; her `ONAY`dan sonra defteri güncelle.**
3. **Sıra sabit:** INTENT → PLAN → CLAUDE → DESIGN → MEMORY. Bir dosya **bitip onaylanmadan** sonrakine geçme.
4. **INTERVIEW → TASLAK → ONAY → [pre-write çatışma geçidi] → YAZ.** Her dosya: soru-cevap → tam taslak göster → kullanıcı onayı → **YAZ'dan önce `references/akis-modlari.md §3` pre-write geçidini çalıştır** (dosya var mı? identical mi? farklıysa DIFF + SOR; `CLAUDE.md` ASLA tam-overwrite — daima birleştir) → proje dizinine yaz. Onaysız/geçitsiz hiçbir dosya yazma. **Kör overwrite = HARD ihlal.**
5. **TÜRKÇE**, kaynak-göster, uydurma yok. Kararlar kullanıcınındır; sınırda/çelişkide **SOR.**

## Akış

### 0. Başlangıç
**ÖNCE iki motoru Read et:** `references/tutarlilik.md` (içerik-tutarlılığı) + `references/akis-modlari.md` (akış: resume/mod/çatışma/devir). Sonra sırayla:
1. **RESUME taraması** (`akis-modlari.md §1`): `<proje-kökü>`'nde 5 dosyadan biri / `.kickoff/state.json` var mı? → **VARSA** defteri diskten yeniden-türet + "[D] devam / [B] baştan" SOR; **YOKSA** yeni oturum.
2. **MOD sorusu** (`akis-modlari.md §2`): "Sıfırdan yeni proje mi (**GREENFIELD**) yoksa mevcut koda feature mı (**BROWNFIELD**)?" → defterde **K0**. Brownfield ise önce **keşif fazı** (mevcut stack/konvansiyon/CLAUDE.md oku), 5 dosyayı *mevcut gerçeklikten* türet.
3. **Bağlam soruları:** (a) **Proje nedir?** (1-2 cümle), (b) **Hangi dizine?** (proje kökü — **mutlak yolu sakla**; dosyalar oraya yazılır), (c) Stack/araç belirsizse → "`/ai-proje-rehberi` ile danışmak ister misin?" öner.

**Tutarlılık defteri** tut → `tutarlilik.md §2` formatı (`# · Kaynak · Karar[tek cümle] · Katman[AMAÇ/UYGULAMA/AYNA] · Durum`). Her `ONAY`dan sonra güncelle (ops. `.kickoff/state.json`).
**YAZ mekaniği (her dosya):** (1) `assets/templates/<DOSYA>.md`'yi (CLAUDE için `CLAUDE.template.md`) Read et; (2) cevaplarla doldur, rehber-yorumları SİL; (3) **pre-write çatışma geçidinden geç** (`akis-modlari.md §3`); (4) hedef = **mutlak** `<proje-kökü>/<DOSYA>.md`; (5) Write — identical ise YAZMA, "[Y] yeni-isimle" ise `<DOSYA>.kickoff-new.md`. Şablonlar skill'in dosyalarıdır; hedef proje dosyalarıyla KARIŞTIRMA.

> **Her dosyada döngü:** o adımın `references/*.md`'sini **ÖNCE Read et** → INTERVIEW → TASLAK (şablondan) → ONAY → **pre-write gate** (`akis-modlari.md §3`) → YAZ → defteri güncelle. Gate çelişki bulursa → `tutarlilik.md §5`: işaretle/sınıfla/çöz veya SOR.

### 1. INTENT.md — niyet sözleşmesi (ilk, KRİTİK)
`references/intent.md` · şablon `assets/templates/INTENT.md`. 6 başlığı **TEK TEK** röportajla (Bağlam · Hedef[tek cümle] · Kullanıcı · Başarı kriteri[sayılabilir] · **Kapsam dışı** · Riskler). Her başlıkta yeterli derinliğe inene dek takip soruları sor. Kalite kapısı → taslak → onay → `INTENT.md` yaz. (AMAÇ katmanı = sonraki her dosyanın çapası.) **Brownfield:** sıfırdan değil keşif-özetinden türet; başarı kriterine "mevcut testler hâlâ geçer", kapsam-dışına "mevcut kontratları değiştirme" ekle (→ `akis-modlari.md §2`).

### 2. PLAN.md
`references/plan.md` · şablon `assets/templates/PLAN.md`. INTENT'ten türet: niyeti atomik, doğrulanabilir adımlara böl. **Gate (INTENT↔PLAN):** her başarı kriteri ≥1 adımla karşılanır; **kapsam-dışına** giren adım YOK. Taslak → onay → yaz.

### 3. CLAUDE.md
`references/claude-md.md` · şablon `assets/templates/CLAUDE.template.md` (memory-collision için `.template` ekli; HEDEFE `<proje-kökü>/CLAUDE.md` yazılır — mevcutsa ASLA tam-overwrite, daima birleştir). `# Proje · # Stack · # Kurallar · # Yapma` (4 prensip: kural+yasak açık, hemen-ekle, tek-kaynak). **Gate (INTENT/PLAN↔CLAUDE):** `# Stack` PLAN'ın gerektirdiğini kapsar, `# Yapma` kapsam-dışını güçlendirir; "çatışma → DESIGN.md kazanır" kuralını yaz. Taslak → onay → yaz.

### 4. DESIGN.md
`references/design.md` · şablon `assets/templates/DESIGN.md`. Mimari kararlar (her zaman) + (UI varsa) tasarım dili (`google-labs/design.md` formatı + **kendi palet/font**, içselleştirilmiş). **Gate:** INTENT/PLAN ile uyum; CLAUDE ile teknik çelişki çıkarsa **DESIGN kazanır → CLAUDE'u güncelle.** Taslak → onay → yaz.

### 5. MEMORY.md
`references/memory.md` · şablon `assets/templates/MEMORY.md`. 4-katman iskelet (working/episodic/semantic/procedural). **Gate (hepsi↔MEMORY):** katmanlar 4 dosyanın kesin kararlarını doğru yansıtır (ayna), eski karar taşımaz. Taslak → onay → yaz.

### 6a. Kapanış — bütünsel tutarlılık geçişi
`tutarlilik.md §6` 5×5 matrisi + kapanış checklist'iyle 5 dosyayı **birlikte** tara (geç çıkan zincir-çelişkiler). Kalan tutarsızlığı raporla/çöz. **6b'ye giriş koşulu:** matris temiz + defterde `açık-soru` YOK.

### 6b. Devir (handoff) — kodlama fazına temiz geçiş
**ÖNCE `references/akis-modlari.md §4`'ü oku.** (1) **Devir özeti** üret (girilecek dosyalar + kapsam-dışı + ilk PLAN adımı + uçtan-uca doğrulama). (2) **Temiz oturum emri:** kullanıcıya açıkça söyle — "Bu oturumu KAPAT / `/clear`; kodlamaya 5 dosyayı okuyan **TAZE** oturumda başla." (3) **İlk PLAN adımı reçetesi** + **commit → run → düzelt** döngüsü (done = iddia değil **KANIT**; KB *AI Kodlamada Commit Disiplini*). (4) `.kickoff/state.json` son kez yaz. Otonom uç → KB *Ralph — Otonom Agentic Kodlama Loop'u (prd.json)*; kickoff burada **biter.**

## Kapsam (negatif sınır)
SADECE yeni proje/feature **kickoff**'u. Bilgi/yaklaşım sorusu → `/ai-proje-rehberi`. Mevcut projede tek-dosya düzenleme/bug → normal asistan. Şüphedeysen sor.
