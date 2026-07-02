# Akış Modları — Resume · Mod · Çatışma Geçidi · Devir

> **Misyon:** Skill'in OPERASYONEL akış mekaniği — **oturum boyutu** (resume/ayrıştırma), **proje boyutu** (greenfield / brownfield-yapısal / brownfield-DELTA), **dosya-sistemi boyutu** (disk çatışma geçidi), **çıkış boyutu** (devir/handoff) ve **harness boyutu** (plan-mode). `tutarlilik.md` *içerik* çelişkisini denetler (içerik geçidi); **bu dosya akışı + dosya-sistemini** denetler (disk geçidi). İkisi birlikte motoru tamamlar. (Kaynak: SDD araçları — GitHub Spec Kit, OpenSpec, BMAD, Agent OS; scaffold conflict UX — Yeoman/copier; Anthropic *Effective harnesses for long-running agents*; KB *Ralph — Otonom Agentic Kodlama Loop'u (prd.json)*.)

---

## 1. §0 RESUME — skill her çağrıldığında İLK iş

> İlke: **"5 dosya kalıcı defterdir; sohbet-içi defter onun diskten türetilen önbelleğidir."** Oturum koparsa veri kaybolmaz — yeniden türetilir (reload değil, **re-derive**; Ralph/Spec-Kit converge kalıbı).

```
ADIM 1 — TARA: <proje-kökü> içinde .kickoff/state.json + 5 dosya (INTENT.md / PLAN.md /
         CLAUDE.md / DESIGN.md / MEMORY.md) + docs/specs/*.md var mı? (ls / Read)
ADIM 2 — AYRIŞTIR (üç-katmanlı sinyal; "dosya var" ≠ "kickoff izi" — kökünde kendi
         CLAUDE.md'si olan HER brownfield repo'yu RESUME sanma):
  • .kickoff/state.json VAR → GERÇEK RESUME:
      – state.faz == "devredildi" → TAMAMLANMIŞ dalı (SOR): "Bu kickoff bitmiş/devredilmiş.
        [Y] Yeni iş (DELTA ya da yeni kickoff) · [R] Mevcut dosyalarda revizyon · [İ] Çık."
      – değilse (faz == "kickoff") → yarım oturum → ADIM 3.
  • state.json YOK ama INTENT.md VE PLAN.md birlikte var → MUHTEMEL KALINTI → kökeni SOR:
      "Bu INTENT/PLAN yarım bir kickoff'tan mı, yoksa elle/başka araçla mı yazıldı?"
      kickoff iziyse ADIM 3 (+ state.json'ı yeniden kur); değilse alttaki madde gibi davran.
  • Yalnız CLAUDE.md / README / tekil dosya var → RESUME DEĞİL. Bunlar önceden-var-olan
    proje dosyalarıdır → YENİ OTURUM (§2 MOD); bulgular BROWNFIELD keşfine "mevcut
    gerçeklik" girdisi olur (dosyalar akran karar kaynağı — §3 disk geçidi zaten korur).
  • Hiçbiri yok → YENİ OTURUM → §2 MOD sorusuna geç.
ADIM 3 — DEFTERİ DİSKTEN YENİDEN-TÜRET:
  • state.json'ı oku (hızlı anchor); eksik kaldıysa var olan her .md'yi OKU ve
    kilit kararları deftere damıt (tutarlilik.md §2 formatı):
      INTENT→AMAÇ · PLAN/DESIGN/CLAUDE→UYGULAMA · MEMORY→AYNA.
  • Türetilmiş defter üzerinde içerik geçidini (tutarlilik.md §3) yeniden çalıştır →
    mevcut set tutarlı mı? Çıkan çelişkileri tutarlilik.md §5 ile işaretle, raporla.
ADIM 4 — SOR (AskUserQuestion ile): "Şu dosyalar mevcut: <liste> (durum: <state>).
         [D] Kaldığım yerden devam   ·   [B] Baştan (mevcutlar disk geçidinden geçer)."
ADIM 5 — DEVAM: sabit sırada (INTENT→…→MEMORY) İLK eksik/yarım dosyadan başla.
         Var olan dosyalara §3 disk çatışma geçidi uygulanır.
```

**`.kickoff/state.json` (ZORUNLU — her ONAY'dan sonra güncellenir;** MEMORY.md'den AYRI — bu süreç-durumu, o proje-hafızası; Anthropic: durum için Markdown yerine JSON, model JSON'u yanlışlıkla ezmeye daha az meyilli). RESUME ayrıştırıcısının tek güvenilir sinyali budur — "opsiyonel" değildir:
```json
{ "mod": "greenfield|brownfield|delta",
  "faz": "kickoff|devredildi",
  "proje_koku": "<mutlak yol>",
  "durum": { "intent":"done", "plan":"done", "claude":"in-progress",
             "design":"pending", "memory":"pending" },
  "acik_sorular": ["..."],
  "kesif_izi": { "<okunan dosya>": "<mtime|ilk-64-karakter>" },
  "son_guncelleme": "<tarih>" }
```
> **Re-baseline kuralı (paralel oturum/editör koruması):** her faz başında ve her YAZ'dan
> önce `kesif_izi`ndeki dosyaların değişip değişmediğine bak (mtime/içerik) — değiştiyse
> ilgili dosyayı YENİDEN oku, defteri tazele, farkı kullanıcıya raporla. Keşifte okunan
> dosyalar da diskin gerçeğidir; defter bayatlamış olabilir.
> **Yaşam döngüsü:** `.kickoff/` proje repo'sunda KALIR ve commit'lenir (devir sonrası
> TAMAMLANMIŞ tespiti + audit izi bunun üzerinden çalışır). `.gitignore`'a KOYMA —
> koyarsan başka makinede RESUME ayrıştırıcısı kör kalır.

---

## 2. §0 MOD — greenfield / brownfield-yapısal / brownfield-DELTA (yeni oturumda, RESUME'dan sonra)

**SOR (AskUserQuestion, 3 seçenek):** *"① GREENFIELD — sıfırdan yeni proje · ② BROWNFIELD-YAPISAL — mevcut koda büyük YENİ alt-sistem (tam 5-dosya) · ③ BROWNFIELD-DELTA — bugfix / feature / refactor / bakım (tek change-spec, hafif yol)"* → cevabı deftere **K0** olarak işle (Katman: META, kesin).
> **Karar kuralı:** Tam-pipeline yalnızca büyük YENİ alt-sistemde; bugfix/feature/refactor/bakım için DELTA yeter. Kullanıcı kararsızsa iki cümleyle farkı anlat ("5 dosya = kalıcı proje anayasası; DELTA = tek dosyalık değişiklik sözleşmesi") ve SOR — dayatma.

### GREENFIELD → mevcut akış aynen
5 dosyayı sıfırdan kur. Dizin boş varsayılır; **yine de her YAZ §3 pre-write geçidinden geçer** (sürpriz dosyaya karşı).

### BROWNFIELD-YAPISAL → sıra değişir: önce KEŞİF, sonra UZLAŞTIRMA (YAZMA değil)
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
### BROWNFIELD-DELTA → tek dosyalık change-spec (hafif yol; 5 dosya YAZILMAZ)
```
KEŞİF FAZI: brownfield-yapısal ile AYNI (mevcut stack/konvansiyon/CLAUDE.md oku,
  bulguları deftere "mevcut gerçeklik" olarak yaz).
SPEC: tek dosya → docs/specs/<feature>.md (şablon: assets/templates/DELTA.md).
  4-eleman change-spec: mevcut davranış · hedef delta (tek cümle) · değişmeyecek
  INVARIANT'lar · kapsam-sınırı — artı BK# kimlikli GWT başarı kriterleri ve
  atomik adımlar (her adım → BK#). INTENT ayrı yazılmaz: spec'in "hedef delta +
  kapsam-sınırı" bölümü AMAÇ katmanıdır (kuzey yıldızı orada yaşar; tutarlilik §1
  hiyerarşisi aynen geçerli).
CLAUDE.md: yalnız GEREKLİ merge-dokunuşu (yeni kural/yasak varsa; §3 disk geçidi —
  daima birleştir). DESIGN.md / MEMORY.md YAZILMAZ.
KAPANIŞ: INTERVIEW→TASLAK→ONAY→disk geçidi→YAZ döngüsü spec için aynen işler;
  kickoff-verify --delta TEMİZ → devir §4 (aynı reçete, tek spec ile).
```

---

## 3. Disk çatışma geçidi (HARD — her YAZ'dan önce)

> **İki geçit vardır, ikisi de zorunludur:** **İÇERİK geçidi** (`tutarlilik.md §3` — taslak, önceki kararlarla çelişiyor mu?) ve **DİSK geçidi** (burası — diskteki mevcut dosya ezilecek mi?). Sıra: TASLAK → içerik geçidi → ONAY → **disk geçidi** → YAZ. Aynı adla iki geçit anılıp teki atlanmasın diye adları ayrıdır.

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
ÖN-KOŞUL: §6a kapanış matrisi temiz + defterde "açık-soru" YOK + kickoff-verify TEMİZ
          (python3 <skill>/scripts/kickoff-verify.py <proje-kökü>; DELTA'da --delta).
1. İSKELET COMMIT'İ: kodlamaya geçmeden 5 dosya (ya da DELTA spec'i) + .kickoff/
   commit'lenir — `kickoff: 5-dosya iskeleti + state` ("önce commit" kuralının ilk
   uygulaması; dosyalar sonradan bozulursa geri-dönüş noktası → KB *AI Kodlamada
   Commit Disiplini*).
2. DEVİR ÖZETİ üret (5 dosya = kendine-yeten devir kontratı):
   girilecek dosyalar (PLAN+CLAUDE+DESIGN okunacak) · kapsam-dışı (INTENT'ten) ·
   ilk PLAN adımı · uçtan-uca doğrulama kriteri.
3. TEMİZ OTURUM emri: kullanıcıya AÇIKÇA söyle — "Bu oturumu KAPAT / `/clear` yap;
   kodlamaya 5 dosyayı okuyan TAZE oturumda başla. Eski kickoff-keşif context'i
   Claude'u raydan çıkarır." (DİKKAT — yaygın yanılgı: Claude Code plan-kabulü
   context'i OTOMATİK TEMİZLEMEZ; bu `showClearContextOnPlanAccept` ayarına bağlı
   opsiyonel bir tekliftir ve default KAPALIDIR. Devirdeki AÇIK /clear emri tam bu
   yüzden vardır.)
4. İLK PLAN ADIMI reçetesi (taze oturuma verilecek başlangıç-prompt'u):
   "PLAN.md adım-1'i uygula; CLAUDE/DESIGN kurallarına uy; commit → run → düzelt:
   testi yaz → başarısız gör → testi commit'le (güvenlik ağı) → yeşil olana dek uygula
   → tam suite → commit. done = iddia değil KANIT (adımın → BK# GWT'sinin Then'i).
   İstenmeyen sonuçta GERİ AL: son yeşil commit'e dön (revert / çift-esc rewind),
   .md'leri düzelt, tekrar dene. Araç seti: /context (token kontrolü) · /effort ·
   plan mode (karmaşık adımda). Model/effort seçimi için KB *Claude Model Seçimi* +
   *Model Ayarları* notlarına bak (buraya gömme — bayatlar)."
5. CRITIC (DEFAULT — opsiyonel değil): ilk paketli işten sonra TAZE bir alt-ajanla
   diff'i PLAN.md + INTENT'e karşı denetlet — her gereksinim uygulandı mı, edge-case
   testli mi, kapsam-dışına taşma var mı? Critic'siz loop = ajanın kendi ödevini
   onaylaması (→ KB *Loop Engineering*). Kullanıcı açıkça vazgeçerse atlanır.
6. STATE'i son kez yaz (.kickoff/state.json: tüm dosyalar done, faz: "devredildi").
```

### Otonom uç (opsiyonel) — PLAN → prd.json köprüsü
Kullanıcı devir sonrasını otonom loop'a (Ralph tarzı) bağlamak isterse reçete:
- **Dönüşüm (mekanik):** her PLAN adımı → bir story: `{ "id": "S<numara>", "tanim":
  "<adımın NE'si>", "kabul": "<adımın → BK# GWT Then'i>", "durum": "pending" }` →
  `prd.json`; ilerleme `progress.txt` + git history'de yaşar (→ KB *Ralph — Otonom
  Agentic Kodlama Loop'u (prd.json)*).
- **Taze-instance kuralı:** her story TEMİZ context'li taze oturumda koşar (yalnız ilk
  adım değil); hafıza dosyalarda yaşar, sohbette değil.
- **Frenler (zorunlu):** ① max-iteration — "N denemede yeşil olmazsa DUR ve insana
  raporla"; ② no-progress — "aynı hatayı ikinci kez alıyorsan boşa dönüyorsun, DUR";
  ③ gerçek tamamlanma = testler geçti, ajanın 'iyi hissetmesi' değil (→ KB *Loop
  Engineering — Prompting'den Loop Tasarımına*).
- Kickoff burada biter; loop'un işletimi ayrı iştir.

---

## 5. Plan-mode protokolü (kısa)

Kickoff **dosya yazan** bir akıştır; Claude Code plan mode ise dosya yazımını kilitler.
Kural: kullanıcı plan mode'daysa röportaj/taslak/keşif aynen sürer (hepsi salt-okur),
ama her `YAZ` adımından önce kullanıcıdan plan mode'dan çıkmasını iste (ya da yazılacak
içeriği plan olarak sun, kabulünde yaz). Kabul-sonrası context temizlenirse §1 RESUME
ayrıştırıcısı zaten güvence — state.json + diskteki dosyalar kaldığı yeri bilir.

---

## Örnek akış 1 — brownfield + kalıntı ayrıştırma (doğrulama)
```
1. /proje-kickoff çağrılır; dizin: mevcut bir Next.js repo.
2. §1 ADIM 2 AYRIŞTIR: state.json YOK; INTENT.md + PLAN.md birlikte VAR; CLAUDE.md de
   var (kullanıcı yazmış) → MUHTEMEL KALINTI → köken SORULUR. Kullanıcı "yarım kickoff'tı"
   der → ADIM 3: defter INTENT+PLAN'dan türetilir, state.json yeniden kurulur; CLAUDE.md
   "akran karar kaynağı" olarak okunur. İçerik geçidi: PLAN bir adımı kapsam-dışına
   giriyor → tutarlilik §5 işaretle → kullanıcıya raporla.
3. §2 MOD = brownfield-yapısal (büyük yeni alt-sistem). Keşif: package.json/CLAUDE.md
   okunur, stack özeti; kesif_izi state.json'a yazılır.
4. Kullanıcı [D] devam → ilk eksik dosya DESIGN.md.
5. DESIGN röportajı → taslak → içerik geçidi → ONAY → disk geçidi: DESIGN.md yok →
   doğrudan YAZ. state.json güncellenir.
6. CLAUDE.md sırası: mevcut → [B] Birleştir ZORUNLU → kickoff bölümleri eklenir,
   kullanıcı kuralları korunur, bir çelişki tutarlilik §5 ile işaretlenip SORulur.
7. MEMORY.md → §6a matris + kickoff-verify TEMİZ → §6b Devir: iskelet commit + özet +
   "/clear, taze oturumda PLAN adım-1" + critic.
```

## Örnek akış 2 — DELTA + false-positive önleme (doğrulama)
```
1. /proje-kickoff çağrılır; dizin: kökünde kendi CLAUDE.md'si olan mevcut bir repo.
2. §1 ADIM 2: state.json yok, INTENT/PLAN yok, yalnız CLAUDE.md var → RESUME DEĞİL
   (eski davranış burada yanlış alarm verirdi) → YENİ OTURUM; CLAUDE.md brownfield
   keşif girdisi.
3. §2 MOD sorusu: kullanıcı "şu API'ye rate-limit ekleyeceğim" der → BROWNFIELD-DELTA.
4. Keşif → docs/specs/rate-limit.md taslağı (4-eleman + BK'lı GWT + adımlar) → ONAY →
   disk geçidi → YAZ. CLAUDE.md'ye tek kural merge'ü. DESIGN/MEMORY yazılmaz.
5. kickoff-verify --delta TEMİZ → devir §4 (iskelet commit + taze oturum + critic).
```

---

**Çapraz-referans:** `SKILL.md` (§0 ve §6 buraya çağırır) · `references/tutarlilik.md` (§4 ilişki sınıfları + §5 çelişki protokolü bu geçidin içerik tarafı). **Kaynak:** GitHub Spec Kit · OpenSpec · BMAD-METHOD · Agent OS · Yeoman Conflicter · copier · Anthropic *Effective harnesses for long-running agents* · KB *Ralph (prd.json)* · *AI Kodlamada Commit Disiplini*.
