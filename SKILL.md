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
4. **INTERVIEW → TASLAK → ONAY → YAZ.** Her dosya: soru-cevap röportajı → tam taslak göster → kullanıcı onayı → **proje dizinine `.md` yaz.** Onaysız hiçbir dosya yazma.
5. **TÜRKÇE**, kaynak-göster, uydurma yok. Kararlar kullanıcınındır; sınırda/çelişkide **SOR.**

## Akış

### 0. Başlangıç
Sor: (a) **Proje nedir?** (1-2 cümle), (b) **Hangi dizine kurulacak?** (proje kökü — dosyalar oraya yazılır), (c) Stack/araç belirsizse → "`/ai-proje-rehberi` ile danışmak ister misin?" öner.
Oturum boyunca bir **tutarlılık defteri** tut → `references/tutarlilik.md §2` formatı (`# · Kaynak · Karar[tek cümle] · Katman[AMAÇ/UYGULAMA/AYNA] · Durum`). Her dosyanın kilit kararları buraya damıtılır; sonraki dosyalar buna hizalanır.
Şablonlar `assets/templates/<DOSYA>.md`'de (iskelet + rehber yorum). Taslağı şablondan başlat, röportaj cevaplarıyla doldur, yorumları sil.

> **Her dosyada döngü:** INTERVIEW → TASLAK (şablondan) → **pre-write gate** (`tutarlilik.md §3`) → ONAY → YAZ → defteri güncelle (`§2`). Gate kalırsa → çelişki protokolü (`§5`): işaretle/sınıfla/çöz veya SOR.

### 1. INTENT.md — niyet sözleşmesi (ilk, KRİTİK)
`references/intent.md` · şablon `assets/templates/INTENT.md`. 6 başlığı **TEK TEK** röportajla (Bağlam · Hedef[tek cümle] · Kullanıcı · Başarı kriteri[sayılabilir] · **Kapsam dışı** · Riskler). Her başlıkta yeterli derinliğe inene dek takip soruları sor. Kalite kapısı → taslak → onay → `INTENT.md` yaz. (AMAÇ katmanı = sonraki her dosyanın çapası.)

### 2. PLAN.md
`references/plan.md` · şablon `assets/templates/PLAN.md`. INTENT'ten türet: niyeti atomik, doğrulanabilir adımlara böl. **Gate (INTENT↔PLAN):** her başarı kriteri ≥1 adımla karşılanır; **kapsam-dışına** giren adım YOK. Taslak → onay → yaz.

### 3. CLAUDE.md
`references/claude-md.md` · şablon `assets/templates/CLAUDE.md`. `# Proje · # Stack · # Kurallar · # Yapma` (4 prensip: kural+yasak açık, hemen-ekle, tek-kaynak). **Gate (INTENT/PLAN↔CLAUDE):** `# Stack` PLAN'ın gerektirdiğini kapsar, `# Yapma` kapsam-dışını güçlendirir; "çatışma → DESIGN.md kazanır" kuralını yaz. Taslak → onay → yaz.

### 4. DESIGN.md
`references/design.md` · şablon `assets/templates/DESIGN.md`. Mimari kararlar (her zaman) + (UI varsa) tasarım dili (`google-labs/design.md` formatı + **kendi palet/font**, içselleştirilmiş). **Gate:** INTENT/PLAN ile uyum; CLAUDE ile teknik çelişki çıkarsa **DESIGN kazanır → CLAUDE'u güncelle.** Taslak → onay → yaz.

### 5. MEMORY.md
`references/memory.md` · şablon `assets/templates/MEMORY.md`. 4-katman iskelet (working/episodic/semantic/procedural). **Gate (hepsi↔MEMORY):** katmanlar 4 dosyanın kesin kararlarını doğru yansıtır (ayna), eski karar taşımaz. Taslak → onay → yaz.

### 6. Kapanış — bütünsel tutarlılık geçişi
`tutarlilik.md §6` 5×5 matrisi + kapanış checklist'iyle 5 dosyayı **birlikte** tara (geç çıkan zincir-çelişkiler). Kalan tutarsızlığı raporla/çöz. Özet + sıradaki: **commit → run → düzelt** döngüsü (KB *AI Kodlamada Commit Disiplini*).

## Kapsam (negatif sınır)
SADECE yeni proje/feature **kickoff**'u. Bilgi/yaklaşım sorusu → `/ai-proje-rehberi`. Mevcut projede tek-dosya düzenleme/bug → normal asistan. Şüphedeysen sor.
