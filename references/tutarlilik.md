# Tutarlılık Motoru (Consistency Engine)

> **Misyon:** 5 dosya (INTENT → PLAN → CLAUDE → DESIGN → MEMORY) sırayla kurulurken, her yeni cevap/dosya öncekilerle **TEYİT** edilir; çelişki üzerine **asla yazılmaz** — işaretlenir, sınıflandırılır, hiyerarşiye göre çözülür **VEYA** kullanıcıya sorulur, sonra deftere işlenir. Bu dosya skill'in kalbidir: her `YAZ` adımı önce buradan geçer. (Kaynak: vault kök `CLAUDE.md` INGEST 4-ilişki taksonomisi + "çelişki = işaretle, üzerine yazma"; KB *5-Dosya Workflow'u* "DESIGN.md kazanır".)
>
> **İçindekiler:** §1 Otorite hiyerarşisi · §2 Defter (+resume) · §3 Pre-write gate · §4 İlişki sınıfları · §5 Çelişki protokolü · §6 Kapanış matrisi. · **Akış/dosya-sistemi mekaniği** (resume, mod, çatışma geçidi, devir) → `references/akis-modlari.md`.

---

## 1. Otorite hiyerarşisi (altın kural)

**INTENT = anayasa (NEDEN). DESIGN = teknik hakem (NASIL).** İkisi ayrı katmandadır; doğru okununca çelişmezler:

```
INTENT  ──► AMAÇ katmanı   · değiştirilemez · hiçbir dosya çiğneyemez (hedef · başarı kriteri · kapsam-dışı)
   │
   └─► DESIGN ──► UYGULAMA katmanı · PLAN/CLAUDE/DESIGN teknik çatışmasında TEK doğruluk kaynağı
          │
          └─► PLAN · CLAUDE   (DESIGN'e ve INTENT'e tabi)

MEMORY  ──► AYNA katmanı · hiçbir şeyi belirlemez; yukarıdaki 4'ünü doğru yansıtmak zorunda
```

- **Dikey kural (üst-otorite):** Bir karar INTENT'in *hedefini / başarı kriterini / kapsam-dışını* ihlal ediyorsa → **karar yanlıştır.** DESIGN bile olsa ezemez. INTENT = kuzey yıldızı buradadır.
- **Yatay kural (teknik hakemlik):** PLAN ↔ CLAUDE ↔ DESIGN *kendi aralarında* teknik olarak çelişirse (stack, pattern, sıra, kural) → **DESIGN kazanır;** diğer ikisi DESIGN'e hizalanır.
- **Sınır:** DESIGN'in yatay üstünlüğü, INTENT'in dikey üstünlüğünü **asla** geçemez.

**Örnek — dikey ihlal (DESIGN kaybeder):**
> INTENT/Hedef: "sıfır-backend, statik site." · DESIGN taslağı: "Postgres + auth API."
> → DESIGN ↔ INTENT dikey ihlali. DESIGN **kaybeder;** amaca hizalanır (örn. statik + edge-KV). Defterde işaretle.

**Örnek — yatay çatışma (DESIGN kazanır):**
> INTENT amacı nötr. · PLAN: "REST ile yaz." · CLAUDE/Kurallar: "REST kullan." · DESIGN: "tRPC."
> → Saf teknik (yatay) çatışma. DESIGN **kazanır;** PLAN + CLAUDE tRPC'ye güncellenir. Defterde işaretle.

---

## 2. Tutarlılık defteri (consistency ledger)

Oturum boyunca tutulan **hafif tek tablo** (sohbet-içi; dosyaya yazılmaz). Her dosyanın `ONAY`ından sonra kilit kararları buraya damıtılır; sonraki her dosya **önce buna hizalanır.**

**Alanlar:** `# · Kaynak (dosya/başlık) · Karar (tek cümle) · Katman (AMAÇ/UYGULAMA/AYNA) · Durum (kesin / açık-soru)`

| #  | Kaynak                | Karar (tek cümle)        | Katman    | Durum       |
|----|-----------------------|--------------------------|-----------|-------------|
| K1 | INTENT/Hedef          | Tek cümlelik hedef …     | AMAÇ      | kesin       |
| K2 | INTENT/Kapsam-dışı    | X yapılmayacak           | AMAÇ      | kesin       |
| K3 | INTENT/Başarı         | Ölçülebilir kriter …     | AMAÇ      | kesin       |
| K4 | PLAN/Adım-n           | Atomik adım …            | UYGULAMA  | kesin       |
| K5 | DESIGN/Mimari         | Teknik karar …           | UYGULAMA  | kesin       |
| …  | …                     | …                        | …         | …           |

**Kurallar:** ① Sadece *kilit* karar girer (gürültü değil). ② Her giriş **tek cümle.** ③ Çelişki çözülünce kaybeden satır *silinmez* → `çözüldü→K#` notuyla işaretlenir. ④ Açık-soru kapanınca `Durum: kesin` olur. ⑤ Defteri her `ONAY`dan sonra kullanıcıya kısa özetle göster.

> **Resume — diskten yeniden-türetme:** Oturum koparsa/context düşerse defter kaybolmaz; `/proje-kickoff` yeniden çağrılınca var olan 5 dosyadan damıtılarak **yeniden kurulur** (`references/akis-modlari.md §1 RESUME`). Disk = kaynak; sohbet defteri = türetilmiş önbellek. Opsiyonel hızlı anchor: `<proje-kökü>/.kickoff/state.json`.

---

## 3. Dosya-öncesi tutarlılık geçidi (pre-write gate)

Her dosya `YAZ` edilmeden önce, ilgili dosya çiftleri için aşağıdaki invariantlar **TEK TEK** kontrol edilir. Bir kontrol kalırsa → §5 (çelişki protokolü).

> **Dosya-sistemi boyutu:** Bu geçit *içerik* çelişkisini denetler. Hedef dosya **diskte zaten varsa**, mevcut dosya da bir **akran karar kaynağıdır** (önceki defter satırıyla aynı statüde) — `references/akis-modlari.md §3` pre-write çatışma geçidiyle okunur + sınıflanır, **ASLA kör-yazılmaz.**

| Çift | Tutarlılık invariantı (✅ = geçer) |
|------|-------------------------------------|
| **INTENT ↔ PLAN**   | Her PLAN adımı bir başarı kriterine/hedefe hizmet eder; hiçbir adım kapsam-dışına girmez; hedef adımların toplamıyla karşılanır |
| **INTENT ↔ CLAUDE** | `# Yapma` kapsam-dışını güçlendirir (çelişmez); `# Kurallar` hedefi engellemez; `# Stack` hedefin gerektirdiğini kapsar |
| **PLAN ↔ CLAUDE**   | Adımların gerektirdiği her teknoloji `# Stack`'te var; hiçbir adım `# Yapma`yı ihlal etmez |
| **INTENT ↔ DESIGN** | Mimari kararlar hedefi taşır; kapsam-dışını mimariye sızdırmaz; UI varsa tasarım dili kullanıcı/başarı kriterine uygun |
| **PLAN ↔ DESIGN**   | Her adım DESIGN mimarisiyle uygulanabilir; adım sırası mimari bağımlılıklarla tutarlı; DESIGN'de olmayan bir bileşeni adım varsaymıyor |
| **CLAUDE ↔ DESIGN** | `# Stack` ve `# Kurallar` DESIGN kararlarının *aynısı* (çelişirse DESIGN kazanır → CLAUDE güncellenir) |
| **hepsi ↔ MEMORY**  | MEMORY katmanları 4 dosyanın *kesin* kararlarını doğru yansıtır; eski/çelişen karar taşımaz. Eşleme: `semantic`←INTENT/DESIGN gerçekleri · `procedural`←CLAUDE kuralları · `episodic`←çözülen çelişkiler · `working`←güncel PLAN adımı |

> **Geçit kuralı:** İlgili tüm satırlar ✅ olmadan `YAZ` **yapılmaz.** Geçemeyen her satır bir *çelişki bulgusu*dur.

---

## 4. İlişki sınıfları (4 ilişki — vault INGEST'ten)

Yeni karar, mevcut deftere göre sınıflanır:

| Sınıf            | Anlam                                  | Eylem |
|------------------|----------------------------------------|-------|
| **Mükerrer**     | Aynı kararı tekrarlıyor                 | Deftere yeni satır ekleme; mevcuda `↔` ile bağla |
| **Tamamlayıcı**  | Boşluğu dolduruyor, çelişmiyor          | Deftere ekle, normal akış |
| **ÇELİŞKİ**      | Mevcut kararla bağdaşmıyor              | → §5 protokolü (işaretle, **asla** üzerine yazma) |
| **Genelleme**    | Mevcut kararın üstüne çıkan/kapsayan ilke | Üst kararı not et; alt kararlar onun örneği olarak hizalanır |

---

## 5. Çelişki tespiti + çözüm protokolü

Çelişki bulununca **dur ve sırayla uygula** (üzerine asla yazma):

```
1. İŞARETLE   → ⚠️ Çelişki: [Kaynak A: karar]  ✗  [Kaynak B: karar]
2. SINIFLA    → §4 (mükerrer / tamamlayıcı / ÇELİŞKİ / genelleme)
3. KATMANLA   → dikey mi (INTENT'e karşı)  ·  yatay mı (PLAN/CLAUDE/DESIGN arası)?
4. ÇÖZ:
     • dikey    → INTENT kazanır; kararı amaca uyarla (otomatik)
     • yatay    → DESIGN kazanır; PLAN/CLAUDE'u hizala (otomatik)
     • belirsiz / INTENT amacı net değil → KULLANICIYA SOR (otomatik çözme)
5. DEFTER     → kaybeden satıra `çözüldü→K#`; kazanan kesinleşir; MEMORY/episodic'e bir satır
```

**Çekirdek kural:** *Üzerine yazma — açıkça işaretle.* Hiçbir karar sessizce ezilmez; her çözüm defterde iz bırakır. INTENT amacının netliğinden şüphedeysen otomatik çözme — **SOR.**

> **Disk muadili:** Diskte mevcut bir dosya taslakla çelişiyorsa bu protokolden **AYNEN** geçer (işaretle → sınıfla → katmanla → çöz/SOR → defter). Dosyayı sessizce ezmek = bu kuralın ihlali (`references/akis-modlari.md §3`).

---

## 6. Kapanış bütünsel geçişi (final holistic pass)

5 dosya bittiğinde, çift-çift geçmiş olsa bile **tam matris** son kez taranır (geç ortaya çıkan zincir-çelişkileri yakalar):

| ↓ kontrol / → karşı | INTENT | PLAN | CLAUDE | DESIGN | MEMORY |
|---------------------|--------|------|--------|--------|--------|
| **INTENT**          | —          | adım↔hedef  | kural↔amaç   | mimari↔amaç   | yansıma |
| **PLAN**            | ✓          | —           | adım↔stack   | adım↔mimari   | yansıma |
| **CLAUDE**          | ✓          | ✓           | —            | stack=DESIGN  | yansıma |
| **DESIGN**          | ✓          | ✓           | ✓            | —             | yansıma |
| **MEMORY**          | ✓          | ✓           | ✓            | ✓             | —       |

**Kapanış checklist'i:**
- [ ] Defterde `Durum: açık-soru` kalan satır YOK
- [ ] Her başarı kriterinin onu karşılayan ≥1 PLAN adımı VAR
- [ ] Hiçbir dosya kapsam-dışına girmiyor
- [ ] CLAUDE `# Stack`/`# Kurallar` = DESIGN (sapma yok)
- [ ] MEMORY 4 katmanı kesin kararları doğru yansıtıyor, eski karar taşımıyor
- [ ] Çözülen her çelişki defterde izli (sessiz ezme yok)

> Matris veya checklist'te bir kalan varsa → kapanış başarısız; ilgili dosya çiftine dön, §5'i uygula, defteri güncelle, tekrar tara.

---

**Çapraz-referans:** `SKILL.md` (akışın her adımında bu geçit çağrılır) · `references/intent.md` (AMAÇ katmanı kaynağı) · `references/design.md` (UYGULAMA katmanı hakemi). **Kaynak:** KB *5-Dosya Workflow'u (INTENT, PLAN, CLAUDE, DESIGN, MEMORY)* + vault kök `CLAUDE.md` (INGEST uyum/çelişki taksonomisi).
