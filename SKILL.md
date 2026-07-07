---
name: proje-kickoff
disable-model-invocation: true
description: >-
  Yeni bir proje/feature'a BAŞLAMADAN ÖNCE 5 temel .md dosyasını (INTENT, PLAN,
  CLAUDE, DESIGN, MEMORY) uçtan uca, soru-cevapla, titizlikle tasarlayıp oluşturan
  proje-başlatma orkestratörü; bakım/bugfix/küçük feature için hafif DELTA modu
  (tek change-spec) içerir. Boş bir chat'te /proje-kickoff ile çağrılır; dosyaları
  sırayla, her birini gerektiği kadar derinlikte, birbiriyle TUTARLI olacak şekilde
  kurar. KULLANMA: hızlı soru, bilgi danışma (onun için /ai-proje-rehberi).
metadata:
  version: 3.0.0   # MAJOR=akış semantiği · MINOR=yeni referans/kontrol · PATCH=metin
---

# Proje Kickoff — 5-Dosya Orkestratörü (+ DELTA modu)

> **Bu çok-mesajlı bir oturumdur.** `/proje-kickoff` ile başlar; 5 dosya (INTENT → PLAN → CLAUDE → DESIGN → MEMORY) ya da DELTA modunda tek change-spec kurulana kadar sürer. Acele yok — ama oturum bölünebilir: her `ONAY`da `.kickoff/state.json` checkpoint'i yazılır, `/clear` sonrası RESUME kaldığı yerden devam eder.
> Temel bilgi: KB *5-Dosya Workflow'u (INTENT, PLAN, CLAUDE, DESIGN, MEMORY)*. Bilgi/yaklaşım danışmak ≠ bu skill → onun için `/ai-proje-rehberi`.

## Çekirdek ilkeler (HARD — asla ihlal etme)
1. **Titizlik > hız.** Her dosyayı **tek tek, başlık başlık, derinlemesine** tasarla. Gereken kadar mesaj harca. Araştırma **hedefli** olsun: soru başına 1-5 kaynak (WebFetch/`/ai-proje-rehberi`); kapsamlı tarama gerekiyorsa **subagent'a devret veya ayrı araştırma oturumu öner** — röportajı bekletme. **Yüzeysel şablon-doldurma YASAK.**
2. **Tutarlılık motoru (kalp).** Her yeni cevap/dosya, **öncekilerle teyitlenir** — geçmişe karşı doğrulanır, paralel/uyumlu tutulur. Çelişki çıkarsa **işaretle + çöz** (üzerine yazma). Hiyerarşi iki katmanlıdır: **INTENT = kuzey yıldızı (AMAÇ — dikey üst-otorite, hiçbir dosya çiğneyemez)**; PLAN/CLAUDE/DESIGN *teknik* çelişirse **DESIGN.md kazanır (yatay hakem)** — ama INTENT amacını asla ezemez. (DELTA modunda AMAÇ katmanı = spec'in "hedef delta + kapsam-sınırı" bölümü.) Motor: `references/tutarlilik.md` — **her `YAZ`dan önce İÇERİK geçidini çalıştır; her `ONAY`dan sonra defteri + state.json'ı güncelle.**
3. **Sıra sabit:** INTENT → PLAN → CLAUDE → DESIGN → MEMORY. Bir dosya **bitip onaylanmadan** sonrakine geçme. (Tek istisna: **BROWNFIELD-DELTA** modu — 5 dosya yerine tek change-spec; → `akis-modlari.md §2`.)
4. **INTERVIEW → TASLAK → [içerik geçidi] → ONAY → [disk geçidi] → YAZ.** Her dosya: soru-cevap → tam taslak göster → **içerik geçidi** (`tutarlilik.md §3` — önceki kararlarla çelişki?) → kullanıcı onayı → **disk geçidi** (`akis-modlari.md §3` — dosya var mı? identical mi? farklıysa DIFF + SOR; `CLAUDE.md` ASLA tam-overwrite — daima birleştir) → proje dizinine yaz. Onaysız/geçitsiz hiçbir dosya yazma. **Kör overwrite = HARD ihlal.**
5. **TÜRKÇE**, kaynak-göster, uydurma yok. Kararlar kullanıcınındır; sınırda/çelişkide **SOR.** Kullanıcı bir soruya *"bilmiyorum / farketmez"* derse: makul bir varsayılan ÖNER + gerekçele, kabul edilirse deftere `açık-soru→varsayılan` notuyla işle ve INTENT/Riskler'e taşı — boş bırakma, dayatma da yapma.
6. **Yapılandırılmış çatallarda AskUserQuestion kullan** ([D]/[B], mod seçimi, [B]/[A]/[Y]/[Ü] — hepsi ≤4 seçenek + Other'a sığar); açık-uçlu röportaj soruları düz metin kalır. Sinyal bir seçeneği netçe gösteriyorsa onu **"(Önerilen)"** işaretle — seçim yine kullanıcının.
7. **Kullanıcı-yüzü dili = SADE Türkçe.** Motorun tekniği (geçitler, defter, state.json, RESUME, mod adları, BK/GWT) sohbete jargon olarak yansıtılmaz: sorular günlük dille sorulur; durum düz cümleyle özetlenir (*"Şu ana kadar netleşenler: … / Hâlâ açık: …"*); çelişki tek sade cümleyle sorulur. Dosyaya yazılan teknik bir öğe (örn. BK numarası) kullanıcının önüne ilk çıktığında tek cümleyle tercüme et. İç işleyiş (referanslar, defter, state, script, dosya içerikleri) TEKNİK kalır — sadeleşen yalnız sohbet yüzüdür.

## Akış

### 0. Başlangıç
**ÖNCE iki motoru Read et:** `references/tutarlilik.md` (içerik geçidi) + `references/akis-modlari.md` (RESUME ayrıştırıcısı / mod / disk geçidi / plan-mode). Devir reçetesi `references/devir.md`'dedir — **yalnız §6b'de** okunur. Sonra sırayla:
1. **RESUME ayrıştırıcısı** (`akis-modlari.md §1` — üç-katmanlı sinyal): `state.json` varsa gerçek RESUME (faz `devredildi` ise TAMAMLANMIŞ dalı); state.json yok ama INTENT+PLAN birlikte varsa kökeni SOR; **yalnız CLAUDE.md/README varsa RESUME DEĞİL** → brownfield keşif girdisi.
2. **MOD sorusu** (`akis-modlari.md §2`, AskUserQuestion — kullanıcıya SADE etiketlerle: *"Sıfırdan yeni bir proje" / "Mevcut projeye büyük yeni bir parça" / "Küçük değişiklik / düzeltme / bakım"*; iç adlar greenfield / brownfield-yapısal / brownfield-DELTA yalnız defter **K0** + state'te). Sinyal netse ilgili seçenek "(Önerilen)". Brownfield'lerde önce **keşif fazı** (mevcut stack/konvansiyon/CLAUDE.md oku; büyük repo'da Explore alt-ajanına devret — eşik `akis-modlari.md §2`; okunanları `state.json.kesif_izi`ne yaz — re-baseline güvencesi).
3. **Funnel açılışı:** bağlam sorularından önce serbest anlatı iste — *"Projeyi/işi kafandaki EN TAM haliyle anlat (dağınık olabilir)."* 6 başlık röportajı bu anlatıdan huni gibi indirgenir; anlatıda cevabı zaten verilmiş soruyu tekrar sorma, teyit et.
4. **Bağlam soruları:** (a) **Proje nedir?** (1-2 cümle — anlatıdan damıt), (b) **Hangi dizine?** (proje kökü — **mutlak yolu sakla**), (c) Stack/araç belirsizse → "`/ai-proje-rehberi` ile danışmak ister misin?" öner.

**Tutarlılık defteri** tut → `tutarlilik.md §2` formatı (`# · Kaynak · Karar[tek cümle] · Katman[AMAÇ/UYGULAMA/AYNA] · Durum`). **Her `ONAY`dan sonra defteri VE `.kickoff/state.json`'ı güncelle (ZORUNLU — şema: `akis-modlari.md §1`).**
**YAZ mekaniği (her dosya):** (1) `assets/templates/<DOSYA>.md`'yi (CLAUDE için `CLAUDE.template.md`, DELTA için `DELTA.md`) Read et; (2) cevaplarla doldur, rehber-yorumları SİL; (3) **disk geçidinden geç** (`akis-modlari.md §3`); (4) hedef = **mutlak** `<proje-kökü>/<DOSYA>.md`; (5) Write — identical ise YAZMA, "[Y] yeni-isimle" ise `<DOSYA>.kickoff-new.md`. Şablonlar skill'in dosyalarıdır; hedef proje dosyalarıyla KARIŞTIRMA.

> **Her dosyada döngü:** o adımın `references/*.md`'sini **ÖNCE Read et** (bu oturumda zaten okunduysa YENİDEN Read etme — compaction sonrası hariç) → INTERVIEW → TASLAK (şablondan) → **içerik geçidi** (`tutarlilik.md §3`) → ONAY → **disk geçidi** (`akis-modlari.md §3`) → YAZ → defter + state.json güncelle. Geçit çelişki bulursa → `tutarlilik.md §5`: işaretle/sınıfla/çöz veya SOR.
> **Plan-mode:** kullanıcı plan mode'daysa röportaj/keşif sürer ama `YAZ` öncesi çıkmasını iste → `akis-modlari.md §5`.

### 1. INTENT.md — niyet sözleşmesi (ilk, KRİTİK)
`references/intent.md` · şablon `assets/templates/INTENT.md` · doldurulmuş örnek: `assets/examples/INTENT-ornek.md` (few-shot çapası — format örneği talimattan güçlüdür). 6 başlığı **TEK TEK** röportajla (Bağlam · Hedef[tek cümle] · Kullanıcı · Başarı kriteri[**BK# kimlikli**, sayılabilir] · **Kapsam dışı** · Riskler). Her başarı kriterini **merdivende sınıfla**: kod-doğrulanabilir mi, LLM-judge mı, insan-onayı mı? — mümkün olan her kriteri **kod-doğrulanabilire it** (devirdeki "done=KANIT" buna bağlanır). Her başlıkta yeterli derinliğe inene dek takip soruları sor. Kalite kapısı → taslak → onay → `INTENT.md` yaz. (AMAÇ katmanı = sonraki her dosyanın çapası.) **Brownfield:** sıfırdan değil keşif-özetinden türet; başarı kriterine "mevcut testler hâlâ geçer", kapsam-dışına "mevcut kontratları değiştirme" ekle (→ `akis-modlari.md §2`).

### 2. PLAN.md
`references/plan.md` · şablon `assets/templates/PLAN.md` · doldurulmuş örnek: `assets/examples/PLAN-ornek.md` (few-shot çapası). INTENT'ten türet: niyeti atomik, doğrulanabilir adımlara böl; **her adım `→ BK#` ile bir kritere demirlenir** (kickoff-verify mekanik eşler: her BK ≥1 adımda, her adım geçerli BK'de). **Gate (INTENT↔PLAN):** her başarı kriteri ≥1 adımla karşılanır; **kapsam-dışına** giren adım YOK. Taslak → onay → yaz.

### 3. CLAUDE.md
`references/claude-md.md` · şablon `assets/templates/CLAUDE.template.md` (memory-collision için `.template` ekli; HEDEFE `<proje-kökü>/CLAUDE.md` yazılır — mevcutsa ASLA tam-overwrite, daima birleştir). `# Proje · # Stack · # Kurallar · # Yapma` (4 prensip: kural+yasak açık, hemen-ekle, tek-kaynak) + **Hafıza kuralı satırı** (MEMORY döngüsünü kodlama fazında canlı tutan tek yer — şablonda hazır). Her aday kural için ele: *"bu her oturumda mı geçerli, yoksa bu göreve mi özgü?"* — göreve özgüyse CLAUDE'a değil PLAN/INTENT'e. **Gate (INTENT/PLAN↔CLAUDE):** `# Stack` PLAN'ın gerektirdiğini kapsar, `# Yapma` kapsam-dışını güçlendirir; "çatışma → DESIGN.md kazanır" kuralını yaz; MUST/ASLA enflasyonu yapma (bağırılan kural aşırı-tetiklenir). Taslak → onay → yaz.

### 4. DESIGN.md
`references/design.md` · şablon `assets/templates/DESIGN.md`. Mimari kararlar (her zaman) + (UI varsa) tasarım dili (`google-labs-code/design.md` formatı + **kendi palet/font**, içselleştirilmiş). **Gate:** INTENT/PLAN ile uyum; CLAUDE ile teknik çelişki çıkarsa **DESIGN kazanır → CLAUDE'u güncelle.** Taslak → onay → yaz.

### 5. MEMORY.md
`references/memory.md` · şablon `assets/templates/MEMORY.md`. 4-katman iskelet (working/episodic/semantic/procedural; procedural = **tetik→koşul→aksiyon** formatında). **Gate (hepsi↔MEMORY):** katmanlar 4 dosyanın kesin kararlarını doğru yansıtır (ayna), eski karar taşımaz. Taslak → onay → yaz.

### 6a. Kapanış — bütünsel tutarlılık geçişi
`tutarlilik.md §6` 5×5 matrisi + kapanış checklist'ini **TAZE bir alt-ajanla** tarat (taze-göz kuralı, DEFAULT — yazan göz kendi ödevini onaylamaz; ayrıntı + ajan görev tanımı `tutarlilik.md §6`; kullanıcı açıkça vazgeçerse ana model tarar). Ardından **deterministik bekçi**: `python3 <skill>/scripts/kickoff-verify.py <proje-kökü>` (DELTA'da `--delta`) → **TEMİZ** olmalı (şablon kalıntısı, eksik başlık, BK↔adım eşlemesi, PLAN/DESIGN bütünlüğü — tam liste script docstring'inde). **6b'ye giriş koşulu:** matris temiz + defterde `açık-soru` YOK + kickoff-verify TEMİZ.

### 6b. Devir (handoff) — kodlama fazına temiz geçiş
**ÖNCE `references/devir.md`'yi oku ve reçetesini AYNEN uygula:** (1) **bütünlük bekçisi** (ÖNER — verify kopyası `.kickoff/verify.py` + hook/CI), (2) **iskelet commit'i** (5 dosya/spec + `.kickoff/` — kodlamadan önce), (3) **devir özeti** (+ RETURN köprüsü: taşınabilir karar sentezi doğduysa `/ai-proje-rehberi`'yi hatırlat), (4) **temiz oturum emri** (açık `/clear`), (5) **ilk PLAN adımı reçetesi** (commit → run → düzelt; done = `→ BK#` GWT'sinin Then'i), (6) **critic — DEFAULT** (taze alt-ajan diff'i PLAN+INTENT'e karşı denetler), (7) state.json `faz: "devredildi"`. Otonom uç istenirse → `devir.md §2` "PLAN → prd.json köprüsü" (KB *Ralph*, *Loop Engineering*); kickoff burada **biter.**

## Kapsam (negatif sınır)
Yeni proje/feature kickoff'u (tam 5-dosya) **ve** mevcut projede bakım/bugfix/küçük feature için **DELTA modu** (tek change-spec). Bilgi/yaklaşım sorusu → `/ai-proje-rehberi`. Tek satırlık düzeltme / spec gerektirmeyen mikro-iş → normal asistan. Şüphedeysen sor.
