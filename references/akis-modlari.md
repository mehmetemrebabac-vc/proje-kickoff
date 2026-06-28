# Akış Modları — Resume · Mod · Çatışma Geçidi · Devir

> **Misyon:** Skill'in OPERASYONEL akış mekaniği — **oturum boyutu** (resume), **proje boyutu** (greenfield/brownfield), **dosya-sistemi boyutu** (pre-write çatışma geçidi) ve **çıkış boyutu** (devir/handoff). `tutarlilik.md` *içerik* çelişkisini denetler; **bu dosya akışı + dosya-sistemini** denetler. İkisi birlikte motoru tamamlar. (Kaynak: SDD araçları — GitHub Spec Kit, OpenSpec, BMAD, Agent OS; scaffold conflict UX — Yeoman/copier; Anthropic *Effective harnesses for long-running agents*; KB *Ralph — Otonom Agentic Kodlama Loop'u (prd.json)*.)

---

## 1. §0 RESUME — skill her çağrıldığında İLK iş

> İlke: **"5 dosya kalıcı defterdir; sohbet-içi defter onun diskten türetilen önbelleğidir."** Oturum koparsa veri kaybolmaz — yeniden türetilir (reload değil, **re-derive**; Ralph/Spec-Kit converge kalıbı).

```
ADIM 1 — TARA: <proje-kökü> içinde INTENT.md / PLAN.md / CLAUDE.md / DESIGN.md / MEMORY.md
         ve .kickoff/state.json var mı? (ls / Read)
ADIM 2 — DALLAN:
  • Hiçbiri yok       → YENİ OTURUM → §2 MOD sorusuna geç.
  • Bazısı/hepsi var  → RESUME → ADIM 3.
ADIM 3 — DEFTERİ DİSKTEN YENİDEN-TÜRET:
  • state.json varsa oku (hızlı anchor). Yoksa/eksikse, var olan her .md'yi OKU ve
    kilit kararları deftere damıt (tutarlilik.md §2 formatı):
      INTENT→AMAÇ · PLAN/DESIGN/CLAUDE→UYGULAMA · MEMORY→AYNA.
  • Türetilmiş defter üzerinde pre-write gate'i (tutarlilik.md §3) yeniden çalıştır →
    mevcut set tutarlı mı? Çıkan çelişkileri tutarlilik.md §5 ile işaretle, raporla.
ADIM 4 — SOR: "Şu dosyalar mevcut: <liste> (durum: <state>).
         [D] Kaldığım yerden devam   ·   [B] Baştan (mevcutlar çatışma geçidinden geçer)."
ADIM 5 — DEVAM: sabit sırada (INTENT→…→MEMORY) İLK eksik/yarım dosyadan başla.
         Var olan dosyalara §3 pre-write çatışma geçidi uygulanır.
```

**`.kickoff/state.json`** (her ONAY'dan sonra güncellenir; MEMORY.md'den AYRI — bu süreç-durumu, o proje-hafızası; Anthropic: durum için Markdown yerine JSON, model JSON'u yanlışlıkla ezmeye daha az meyilli):
```json
{ "mod": "greenfield|brownfield",
  "durum": { "intent":"done", "plan":"done", "claude":"in-progress",
             "design":"pending", "memory":"pending" },
  "acik_sorular": ["..."],
  "son_guncelleme": "<tarih>" }
```

---

## 2. §0 MOD — greenfield / brownfield (yeni oturumda, RESUME'dan sonra)

**SOR:** *"Sıfırdan yeni proje mi (GREENFIELD) yoksa mevcut koda feature/değişiklik mi (BROWNFIELD)?"* → cevabı deftere **K0** olarak işle (Katman: META, kesin).

### GREENFIELD → mevcut akış aynen
5 dosyayı sıfırdan kur. Dizin boş varsayılır; **yine de her YAZ §3 pre-write geçidinden geçer** (sürpriz dosyaya karşı).

### BROWNFIELD → sıra değişir: önce KEŞİF, sonra UZLAŞTIRMA (YAZMA değil)
```
KEŞİF FAZI (5 dosyadan ÖNCE):
  • Mevcut dizini tara: CLAUDE.md / AGENTS.md / README / package.json / .git / dizin yapısı.
  • Stack / pattern / konvansiyonu OKU ve özetle (Agent OS discover-standards;
    Spec-Kit brownfield bootstrap: koddan tech-stack/pattern türet).
  • Bulguları deftere "mevcut gerçeklik" satırları olarak yaz.
UZLAŞTIRMA FAZI (her dosya için):
  • 5 dosyayı SIFIRDAN değil, MEVCUT GERÇEKLİKTEN türet.
  • INTENT = "mevcut X'i bozmadan Y ekle"; başarı kriteri "mevcut testler hâlâ geçer"
    içerir; kapsam-dışına "mevcut kontratları/pattern'leri değiştirme" satırı ZORUNLU.
  • PLAN = tam-sistem değil DELTA (change-level) adımları.
  • CLAUDE.md / DESIGN.md mevcut konvansiyonları YANSITIR (icat etmez); var olan
    dosyalarla MERGE edilir (§3 — özellikle CLAUDE.md daima birleştir).
  • Değişmeyecek INVARIANT'ları açıkça yaz (change-level spec 4-elemanı:
    mevcut davranış · hedef delta · değişmeyecek invariant · kapsam-sınırı).
```
> **Karar kuralı:** Tam-pipeline yalnızca büyük YENİ alt-sistemde; bugfix/feature/refactor için DELTA spec yeter.

---

## 3. Pre-write çatışma geçidi (HARD — her YAZ'dan önce)

> Vault kuralının (*"çelişki = işaretle, üzerine yazma"*) **dosya-sistemi karşılığı.** 5 dosyanın HER BİRİ için, Write çağrısından ÖNCE bu geçit çalışır. **Default ASLA "üzerine yaz" değildir.**

```
ADIM 1 — VAR MI?  Hedef <proje-kökü>/<DOSYA>.md mevcut mu? (Read dene.)
  • YOK   → doğrudan YAZ. (greenfield happy-path)
  • VAR   → ADIM 2.
ADIM 2 — AYNI MI?  Mevcut içeriği üretilecek taslakla karşılaştır.
  • IDENTICAL (anlamca aynı) → SESSİZ ATLA. "değişiklik yok: <DOSYA>" de. SORMA.
  • FARKLI → ADIM 3.
ADIM 3 — DIFF + SOR (kör karar yasak). Önce farkı özetle:
    ⚠️ <DOSYA>.md zaten mevcut.  + eklenecek: <madde>   − çelişen: <madde>
  Sonra 4 seçenek (default YOK; kullanıcı seçer):
    [B] Birleştir   → mevcut + taslağı tutarlilik §4 ile uzlaştır → yaz
    [A] Atla        → mevcut dosyaya dokunma; deftere "atlandı" yaz
    [Y] Yeni-isimle → taslağı <DOSYA>.kickoff-new.md olarak yaz; kullanıcı birleştirir
    [Ü] Üzerine-yaz → YALNIZCA kullanıcı açıkça seçerse; mevcut <DOSYA>.bak alınır
ADIM 4 — BİRLEŞTİR seçilirse:
  • Mevcut içeriği bir AKRAN KARAR KAYNAĞI gibi ele al (defterdeki önceki satır statüsünde).
  • Her parça için tutarlilik §4 sınıflaması: mükerrer→atla · tamamlayıcı→ekle ·
    ÇELİŞKİ→§5 protokolü (işaretle/katmanla/çöz veya SOR) · genelleme→üst-ilke not et.
  • Kullanıcının mevcut içeriğini KORU; kickoff parçalarını EKLE. Çelişki sessizce
    ezilmez — işaretlenir, deftere `çözüldü→K#` ile iz bırakır.
```

### CLAUDE.md özel kuralı (karma dosya — ASLA tam-overwrite)
Mevcut `CLAUDE.md` varsa **default daima [B] Birleştir**; [Ü] sunulmaz/önerilmez. Claude Code `/init` mantığı: oku → kickoff bölümlerini (`# Proje · # Stack · # Kurallar · # Yapma` + Çatışma kuralı) EKLE → kullanıcının var olan kurallarını KORU → çelişeni işaretle + SOR. Gerekçe: `CLAUDE.md` hem iskelet hem kullanıcı-içeriği taşır; force onu siler (Spec-Kit `constitution.md` force-ezme bug'ı dersi). `README` / `.gitignore` gibi karma dosyalar da aynı.

---

## 4. Devir (handoff) — kodlama fazına temiz geçiş (§6b)

> 5 dosya = bir sonraki ajanın okuyacağı **kalıcı handoff artefaktı** (BMAD self-contained story; Anthropic fresh-session). Devir = dosya-tabanlı, sohbet değil.

```
ÖN-KOŞUL: §6a kapanış matrisi temiz + defterde "açık-soru" YOK.
1. DEVİR ÖZETİ üret (5 dosya = kendine-yeten devir kontratı):
   girilecek dosyalar (PLAN+CLAUDE+DESIGN okunacak) · kapsam-dışı (INTENT'ten) ·
   ilk PLAN adımı · uçtan-uca doğrulama kriteri.
2. TEMİZ OTURUM emri: kullanıcıya AÇIKÇA söyle — "Bu oturumu KAPAT / `/clear` yap;
   kodlamaya 5 dosyayı okuyan TAZE oturumda başla. Eski kickoff-keşif context'i
   Claude'u raydan çıkarır." (Claude Code plan-kabulünde context'i zaten oto-temizler;
   devir = planlı /clear.)
3. İLK PLAN ADIMI reçetesi (taze oturuma verilecek başlangıç-prompt'u):
   "PLAN.md adım-1'i uygula; CLAUDE/DESIGN kurallarına uy; commit → run → düzelt:
   testi yaz → başarısız gör → testi commit'le (güvenlik ağı) → yeşil olana dek uygula
   → tam suite → commit. done = iddia değil KANIT (test/build çıktısı)."
4. STATE'i son kez yaz (.kickoff/state.json: tüm dosyalar done, devir-edildi).
```
> **Adversarial gate (ops.):** İlk adım sonrası taze bir alt-ajanla diff'i PLAN.md'ye karşı denetlet — her gereksinim uygulandı mı, edge-case'ler testli mi, kapsam-dışı bir şey değişti mi. **Otonom uç** istenirse → KB *Ralph — Otonom Agentic Kodlama Loop'u (prd.json)* (çapraz-referans; kickoff burada biter).

---

## Örnek akış — brownfield + resume senaryosu (doğrulama)
```
1. /proje-kickoff çağrılır; dizin: mevcut bir Next.js repo.
2. §0 RESUME taraması: INTENT.md + PLAN.md mevcut, CLAUDE.md mevcut (kullanıcı yazmış),
   .kickoff/state.json yok → RESUME. Defter INTENT+PLAN'dan türetilir; CLAUDE.md
   "akran karar kaynağı" olarak okunur. Pre-write gate: PLAN bir adımı kapsam-dışına
   giriyor → §5 işaretle → kullanıcıya raporla.
3. §2 MOD = brownfield (kod var). Keşif: package.json/CLAUDE.md okunur, stack özeti.
4. Kullanıcı [D] devam → ilk eksik dosya DESIGN.md.
5. DESIGN röportajı → taslak → §3: DESIGN.md yok → doğrudan YAZ. state.json güncellenir.
6. CLAUDE.md sırası: mevcut → [B] Birleştir ZORUNLU → kickoff bölümleri eklenir,
   kullanıcı kuralları korunur, bir çelişki §5 ile işaretlenip SORulur.
7. MEMORY.md → §6a matris temiz → §6b Devir: özet + "/clear, taze oturumda PLAN adım-1".
```

---

**Çapraz-referans:** `SKILL.md` (§0 ve §6 buraya çağırır) · `references/tutarlilik.md` (§4 ilişki sınıfları + §5 çelişki protokolü bu geçidin içerik tarafı). **Kaynak:** GitHub Spec Kit · OpenSpec · BMAD-METHOD · Agent OS · Yeoman Conflicter · copier · Anthropic *Effective harnesses for long-running agents* · KB *Ralph (prd.json)* · *AI Kodlamada Commit Disiplini*.
