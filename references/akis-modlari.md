# Akış Modları — Resume · Mod · Disk Geçidi · Plan-Mode · Arıza Modları

> **Misyon:** Skill'in OPERASYONEL akış mekaniği — **oturum boyutu** (resume/ayrıştırma), **proje boyutu** (greenfield / brownfield-yapısal / brownfield-DELTA), **dosya-sistemi boyutu** (disk çatışma geçidi) ve **harness boyutu** (plan-mode). `tutarlilik.md` *içerik* çelişkisini denetler (içerik geçidi); **bu dosya akışı + dosya-sistemini** denetler (disk geçidi). İkisi birlikte motoru tamamlar. **Çıkış boyutu (devir/handoff) ayrı dosyadadır → `references/devir.md` (yalnız §6b'de okunur).** (Kaynak: SDD araçları — GitHub Spec Kit, OpenSpec, BMAD, Agent OS; scaffold conflict UX — Yeoman/copier; Anthropic *Effective harnesses for long-running agents*; KB *Ralph — Otonom Agentic Kodlama Loop'u (prd.json)*.)
> **Kullanıcı-yüzü dili (SKILL.md ilke 7):** bu dosyadaki iç terimler (RESUME, state.json, mod adları, defter, re-derive) sohbette kullanıcıya söylenmez; aşağıdaki soru kalıpları SADE hâlleriyle sorulur. Dosya adları (INTENT.md vb.) gerçek artefakt oldukları için söylenebilir.

---

## 1. §0 RESUME — skill her çağrıldığında İLK iş

> İlke: **"5 dosya kalıcı defterdir; sohbet-içi defter onun diskten türetilen önbelleğidir."** Oturum koparsa veri kaybolmaz — yeniden türetilir (reload değil, **re-derive**; Ralph/Spec-Kit converge kalıbı).

```
ADIM 1 — TARA: <proje-kökü> içinde .kickoff/state.json + 5 dosya (INTENT.md / PLAN.md /
         CLAUDE.md / DESIGN.md / MEMORY.md) + docs/specs/*.md var mı? (ls / Read)
ADIM 2 — AYRIŞTIR (üç-katmanlı sinyal; "dosya var" ≠ "kickoff izi" — kökünde kendi
         CLAUDE.md'si olan HER brownfield repo'yu RESUME sanma):
  • .kickoff/state.json VAR → GERÇEK RESUME:
      – state.faz == "devredildi" → TAMAMLANMIŞ dalı (SOR, sade): "Bu projenin kurulumu
        daha önce tamamlanıp kodlamaya geçilmiş. [Y] Yeni bir iş var (küçük değişiklik
        ya da yeni kurulum) · [R] Mevcut dosyalarda düzeltme yapalım · [İ] Çık."
      – değilse (faz == "kickoff") → yarım oturum → ADIM 3.
  • state.json YOK ama INTENT.md VE PLAN.md birlikte var → MUHTEMEL KALINTI → kökeni SOR
      (sade): "Bu INTENT/PLAN dosyalarını daha önce bu kurulumla mı başlatmıştık, yoksa
      elle/başka bir araçla mı yazıldı?"
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
    mevcut set tutarlı mı? Çıkan çelişkileri tutarlilik.md §5 ile işaretle, SADE dille raporla.
ADIM 4 — SOR (AskUserQuestion ile, sade): "Bu klasörde daha önce başlanmış bir kurulum
         buldum; şunlar hazır: <sade liste — örn. 'niyet ve plan dosyaları tamam,
         kurallar dosyası yarım kalmış'>.
         [D] Kaldığımız yerden devam   ·   [B] Baştan başla (var olan dosyalar korunarak
         ele alınır — §3 geçidi)."
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
> **DELTA varyantı (mod == "delta"):** `durum` anahtarları 5-dosya seti DEĞİL, spec-odaklıdır:
> `"durum": { "spec": "pending|in-progress|done", "claude": "done" }` — `claude` yalnız
> merge-dokunuşu yapıldıysa bulunur (kickoff-verify v2 anahtar-setini denetler).
> **Re-baseline kuralı (paralel oturum/editör koruması):** her faz başında ve her YAZ'dan
> önce `kesif_izi`ndeki dosyaların değişip değişmediğine bak (mtime/içerik) — değiştiyse
> ilgili dosyayı YENİDEN oku, defteri tazele, farkı kullanıcıya SADE dille raporla. Keşifte
> okunan dosyalar da diskin gerçeğidir; defter bayatlamış olabilir.
> **Yaşam döngüsü:** `.kickoff/` proje repo'sunda KALIR ve commit'lenir (devir sonrası
> TAMAMLANMIŞ tespiti + audit izi bunun üzerinden çalışır). `.gitignore`'a KOYMA —
> koyarsan başka makinede RESUME ayrıştırıcısı kör kalır (kickoff-verify v2 bunu denetler).

---

## 2. §0 MOD — greenfield / brownfield-yapısal / brownfield-DELTA (yeni oturumda, RESUME'dan sonra)

**SOR (AskUserQuestion, 3 seçenek — kullanıcıya SADE etiketlerle):** *"Bu iş ne tür? ① **Sıfırdan yeni bir proje** · ② **Mevcut projeye büyük yeni bir parça** · ③ **Küçük değişiklik / düzeltme / bakım**"* → cevabı deftere **K0** olarak İÇ adıyla işle (greenfield / brownfield-yapısal / brownfield-DELTA; Katman: META, kesin). Teknik mod adları sohbette kullanılmaz; yalnız defter + `state.json.mod`'da yaşar.
> **Funnel/Önerilen kuralı:** serbest anlatı ya da dizin sinyali modu netçe gösteriyorsa (boş dizin → ①; "şu endpoint'e X ekleyeceğim" gibi tarif → ③) o seçeneği **"(Önerilen)"** işaretle + tek cümle gerekçe söyle — seçim yine kullanıcının, dayatma yok.
> **Karar kuralı:** Tam-pipeline yalnızca büyük YENİ alt-sistemde; bugfix/feature/refactor/bakım için ③ yeter. Kullanıcı kararsızsa farkı iki SADE cümleyle anlat ("5 dosya = projenin kalıcı el kitabı; ③ = küçük işler için tek sayfalık değişiklik sözleşmesi") ve SOR — dayatma.

### GREENFIELD → mevcut akış aynen
5 dosyayı sıfırdan kur. Dizin boş varsayılır; **yine de her YAZ §3 pre-write geçidinden geçer** (sürpriz dosyaya karşı).

### BROWNFIELD-YAPISAL → sıra değişir: önce KEŞİF, sonra UZLAŞTIRMA (YAZMA değil)
```
KEŞİF FAZI (5 dosyadan ÖNCE):
  • Delegasyon eşiği: keşif ~15+ dosya okumayı gerektirecekse (monorepo / büyük kod
    tabanı) taramayı Explore-tipi SALT-OKUR alt-ajana devret (Agent tool) — ısmarlanan:
    "stack, konvansiyonlar, CLAUDE.md/AGENTS.md/README özeti, test/çalıştırma
    komutları". Dönen özet deftere "mevcut gerçeklik", ajanın okuduğu dosyalar
    kesif_izi'ne işlenir. Küçük repo'da ana oturumda oku (alt-ajan yükü gereksiz).
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
KEŞİF FAZI: brownfield-yapısal ile AYNI (delegasyon eşiği dahil; mevcut
  stack/konvansiyon/CLAUDE.md oku, bulguları deftere "mevcut gerçeklik" olarak yaz).
SPEC: tek dosya → docs/specs/<feature>.md (şablon: assets/templates/DELTA.md ·
  doldurulmuş örnek: assets/examples/DELTA-ornek.md — few-shot çapası).
  4-eleman change-spec: mevcut davranış · hedef delta (tek cümle) · değişmeyecek
  INVARIANT'lar · kapsam-sınırı — artı BK# kimlikli GWT başarı kriterleri ve
  atomik adımlar (her adım → BK#). INTENT ayrı yazılmaz: spec'in "hedef delta +
  kapsam-sınırı" bölümü AMAÇ katmanıdır (kuzey yıldızı orada yaşar; tutarlilik §1
  hiyerarşisi aynen geçerli).
CLAUDE.md: yalnız GEREKLİ merge-dokunuşu (yeni kural/yasak varsa; §3 disk geçidi —
  daima birleştir). DESIGN.md / MEMORY.md YAZILMAZ.
KAPANIŞ: INTERVIEW→TASLAK→ONAY→disk geçidi→YAZ döngüsü spec için aynen işler;
  kickoff-verify --delta TEMİZ → devir (references/devir.md — aynı reçete, tek spec ile).
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
ADIM 3 — DIFF + SOR (kör karar yasak). Önce farkı SADE dille özetle:
    ⚠️ <DOSYA> zaten var. Eklenecekler: <madde>   ·   Çelişenler: <madde>
  Sonra 4 seçenek (default YOK; kullanıcı seçer; etiketler sade — iç adlar köşeli):
    [B] İkisini birleştir (senin içeriğin korunur)        ← iç ad: Birleştir (merge)
    [A] Dosyaya dokunma                                    ← iç ad: Atla
    [Y] Yan dosya olarak kaydet (<DOSYA>.kickoff-new.md)   ← iç ad: Yeni-isimle
    [Ü] Üzerine yaz (önce yedeği alınır: <DOSYA>.bak)      ← YALNIZCA kullanıcı açıkça seçerse
ADIM 4 — BİRLEŞTİR seçilirse:
  • Mevcut içeriği bir AKRAN KARAR KAYNAĞI gibi ele al (defterdeki önceki satır statüsünde).
  • Her parça için tutarlilik §4 sınıflaması: mükerrer→atla · tamamlayıcı→ekle ·
    ÇELİŞKİ→§5 protokolü (işaretle/katmanla/çöz veya SOR) · genelleme→üst-ilke not et.
  • Kullanıcının mevcut içeriğini KORU; kickoff parçalarını EKLE. Çelişki sessizce
    ezilmez — işaretlenir, deftere `çözüldü→K#` ile iz bırakır (kullanıcıya sunum:
    tek sade cümle — SKILL.md ilke 7).
```

### CLAUDE.md özel kuralı (karma dosya — ASLA tam-overwrite)
Mevcut `CLAUDE.md` varsa **default daima [B] Birleştir**; [Ü] sunulmaz/önerilmez. Claude Code `/init` mantığı: oku → kickoff bölümlerini (`# Proje · # Stack · # Kurallar · # Yapma` + Çatışma kuralı) EKLE → kullanıcının var olan kurallarını KORU → çelişeni işaretle + SOR. Gerekçe: `CLAUDE.md` hem iskelet hem kullanıcı-içeriği taşır; force onu siler (Spec-Kit `constitution.md` force-ezme bug'ı dersi). `README` / `.gitignore` gibi karma dosyalar da aynı.

---

## 4. Devir (handoff) → `references/devir.md`

Devir reçetesi (bütünlük bekçisi · iskelet commit · devir özeti + RETURN köprüsü · temiz oturum · ilk PLAN adımı · critic · state) ve otonom uç (PLAN → prd.json) **ayrı dosyada yaşar**; SKILL.md §6b'de okunur. Burada tutulmaz — oturum başındaki zorunlu okuma yükünü küçük tutmak için.

---

## 5. Plan-mode protokolü (kısa)

Kickoff **dosya yazan** bir akıştır; Claude Code plan mode ise dosya yazımını kilitler.
Kural: kullanıcı plan mode'daysa röportaj/taslak/keşif aynen sürer (hepsi salt-okur),
ama her `YAZ` adımından önce kullanıcıdan plan mode'dan çıkmasını iste (ya da yazılacak
içeriği plan olarak sun, kabulünde yaz). Kabul-sonrası context temizlenirse §1 RESUME
ayrıştırıcısı zaten güvence — state.json + diskteki dosyalar kaldığı yeri bilir.

---

## 6. Arıza modları (araç/ortam fallback'leri — sessiz düşme YASAK)

Araç eksikliği akışı DURDURMAZ; her arızada sırayla: ① kullanıcıya SADE tek cümleyle bildir → ② fallback'i uygula → ③ deftere işle. Hiçbir arıza sessizce yutulmaz, hiçbir adım "araç yoktu" diye sessizce atlanmaz.

| Arıza | Fallback |
|---|---|
| `python3` yok / kickoff-verify koşarken hata | Script docstring'indeki kontrol listesi (SSOT) **ELLE** madde madde denetlenir; devir özetine "mekanik değil elle doğrulandı" notu düşülür. |
| `state.json` bozuk (geçersiz JSON) | Bozuk dosyayı `.kickoff/state.json.bak`e taşı; defteri §1 ADIM 3 ile diskteki dosyalardan yeniden türet; state.json'ı sıfırdan kur. |
| Alt-ajan açılamıyor (keşif Explore'u / 6a taze-göz / devir critic'i) | Ana model üstlenir + kullanıcıya "bağımsız göz yok, kendi taramam" uyarısı; 6a'da taze-göz güvencesinin eksik kaldığı devir özetine not edilir. |
| AskUserQuestion kullanılamıyor | Aynı seçenekler düz metin numaralı liste olarak sorulur; default dayatılmaz, "(Önerilen)" işareti korunur. |
| WebFetch yok / ağ kapalı | Araştırma sorusu kullanıcıya yöneltilir ya da makul varsayılan ÖNERİLİR (SKILL.md ilke 5 "bilmiyorum" yolu); kaynaksız iddia uydurulmaz. |

---

## Örnek akış 1 — brownfield + kalıntı ayrıştırma (doğrulama)
```
1. /proje-kickoff çağrılır; dizin: mevcut bir Next.js repo.
2. §1 ADIM 2 AYRIŞTIR: state.json YOK; INTENT.md + PLAN.md birlikte VAR; CLAUDE.md de
   var (kullanıcı yazmış) → MUHTEMEL KALINTI → köken SORULUR (sade). Kullanıcı "yarım
   kalmıştı" der → ADIM 3: defter INTENT+PLAN'dan türetilir, state.json yeniden kurulur;
   CLAUDE.md "akran karar kaynağı" olarak okunur. İçerik geçidi: PLAN bir adımı
   kapsam-dışına giriyor → tutarlilik §5 işaretle → kullanıcıya SADE cümleyle raporla.
3. §2 MOD = mevcut projeye büyük yeni parça (iç ad: brownfield-yapısal). Keşif:
   package.json/CLAUDE.md okunur, stack özeti; kesif_izi state.json'a yazılır.
4. Kullanıcı [D] devam → ilk eksik dosya DESIGN.md.
5. DESIGN röportajı → taslak → içerik geçidi → ONAY → disk geçidi: DESIGN.md yok →
   doğrudan YAZ. state.json güncellenir.
6. CLAUDE.md sırası: mevcut → [B] Birleştir ZORUNLU → kickoff bölümleri eklenir,
   kullanıcı kuralları korunur, bir çelişki tutarlilik §5 ile işaretlenip SORulur.
7. MEMORY.md → §6a taze-göz taraması + kickoff-verify TEMİZ → §6b Devir
   (references/devir.md): bekçi önerisi + başlangıç kaydı + özet + "/clear, taze
   oturumda PLAN adım-1" + critic.
```

## Örnek akış 2 — DELTA + false-positive önleme (doğrulama)
```
1. /proje-kickoff çağrılır; dizin: kökünde kendi CLAUDE.md'si olan mevcut bir repo.
2. §1 ADIM 2: state.json yok, INTENT/PLAN yok, yalnız CLAUDE.md var → RESUME DEĞİL
   (eski davranış burada yanlış alarm verirdi) → YENİ OTURUM; CLAUDE.md brownfield
   keşif girdisi.
3. §2 MOD sorusu: kullanıcı "şu API'ye rate-limit ekleyeceğim" der → ③ "Küçük
   değişiklik" seçeneği "(Önerilen)" işaretli sunulur → BROWNFIELD-DELTA (iç ad, K0).
4. Keşif → docs/specs/rate-limit.md taslağı (4-eleman + BK'lı GWT + adımlar) → ONAY →
   disk geçidi → YAZ. CLAUDE.md'ye tek kural merge'ü. DESIGN/MEMORY yazılmaz.
5. kickoff-verify --delta TEMİZ → devir (references/devir.md: bekçi + başlangıç kaydı +
   taze oturum + critic).
```

---

**Çapraz-referans:** `SKILL.md` (§0 ve §3 buraya çağırır; §6b → `references/devir.md`) · `references/tutarlilik.md` (§4 ilişki sınıfları + §5 çelişki protokolü bu geçidin içerik tarafı). **Kaynak:** GitHub Spec Kit · OpenSpec · BMAD-METHOD · Agent OS · Yeoman Conflicter · copier · Anthropic *Effective harnesses for long-running agents* · KB *Ralph (prd.json)* · *AI Kodlamada Commit Disiplini*.
