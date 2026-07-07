# Devir (Handoff) — Kodlama Fazına Temiz Geçiş

> **Misyon:** SKILL.md §6b'nin motoru — kickoff bitince işi kodlama fazına dosya-tabanlı devretmek. 5 dosya (ya da DELTA spec'i) = bir sonraki ajanın okuyacağı **kalıcı handoff artefaktı** (BMAD self-contained story; Anthropic fresh-session). Devir = dosya-tabanlı, sohbet değil. Bu dosya **yalnız §6b'de okunur** (oturum başı okuma yükünü küçük tutmak için `akis-modlari.md`'den ayrıldı).
> **Kullanıcı-yüzü dili (SKILL.md ilke 7):** adım adları iç terimdir; kullanıcıya sade söyle — "iskelet commit'i" → *"başlangıç kaydını (commit) alıyorum"* · "critic" → *"bağımsız bir kontrol ajanı"* · "handoff/devir" → *"kodlamaya geçiş"*.

## 1. Devir reçetesi (sırayla, AYNEN uygula)

```
ÖN-KOŞUL: §6a kapanışı temiz (tutarlilik.md §6 taze-göz taraması + matris) + defterde
          "açık-soru" YOK + kickoff-verify TEMİZ
          (python3 <skill>/scripts/kickoff-verify.py <proje-kökü>; DELTA'da --delta).
1. BÜTÜNLÜK BEKÇİSİ (ÖNER — E/H; sade sor: "Bu kurulum dosyaları ileride değişirse
   tutarlılığı otomatik denetleyen küçük bir bekçi kurayım mı?"). E ise:
   ① <skill>/scripts/kickoff-verify.py → <proje-kökü>/.kickoff/verify.py olarak KOPYALA
     (repo ile taşınır; CI'da ve skill kurulu olmayan makinede de koşar).
   ② Proje .claude/settings.json'ına hook ekle (dosya mevcutsa disk geçidi gibi BİRLEŞTİR):
     "PostToolUse": [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command":
       "f=$(jq -r .tool_input.file_path); case \"$f\" in *INTENT.md|*PLAN.md|*CLAUDE.md|*DESIGN.md|*MEMORY.md|*/specs/*.md) python3 .kickoff/verify.py . 2>&1 | tail -4;; esac; exit 0" }]}]
     (DELTA projesinde komuta --delta ekle. Alternatif: CI adımı —
     `python3 .kickoff/verify.py . --strict`.) → KB *8 Pratik Claude Code Hook'u*:
     "CLAUDE.md öneridir, hook garantidir." Reddedilirse atla, deftere işle.
2. İSKELET COMMIT'İ: kodlamaya geçmeden 5 dosya (ya da DELTA spec'i) + .kickoff/ (+ varsa
   hook'lu .claude/settings.json) commit'lenir — `kickoff: 5-dosya iskeleti + state`
   ("önce commit" kuralının ilk uygulaması; dosyalar sonradan bozulursa geri-dönüş
   noktası → KB *AI Kodlamada Commit Disiplini*).
3. DEVİR ÖZETİ üret (5 dosya = kendine-yeten devir kontratı):
   girilecek dosyalar (PLAN+CLAUDE+DESIGN okunacak) · kapsam-dışı (INTENT'ten) ·
   ilk PLAN adımı · uçtan-uca doğrulama kriteri.
   + RETURN köprüsü (tek satır): kickoff'ta başka projelere de taşınabilir bir
   karar/yaklaşım sentezi doğduysa kullanıcıya sor — "Bu karar bilgi havuzuna da
   girsin mi? → /ai-proje-rehberi ile eklenir." (Kickoff vault'a ASLA kendisi yazmaz;
   yalnız hatırlatır.)
4. TEMİZ OTURUM emri: kullanıcıya AÇIKÇA ve sade söyle — "Bu oturumu kapat / `/clear`
   yap; kodlamaya, 5 dosyayı okuyan TAZE bir oturumda başla. Buradaki uzun kurulum
   sohbeti kodlama oturumunu raydan çıkarır." (DİKKAT — yaygın yanılgı: Claude Code
   plan-kabulü context'i OTOMATİK TEMİZLEMEZ; `showClearContextOnPlanAccept` ayarına
   bağlı opsiyonel bir tekliftir ve default KAPALIDIR. Açık /clear emri bu yüzden var.)
5. İLK PLAN ADIMI reçetesi (taze oturuma verilecek başlangıç-prompt'u):
   "PLAN.md adım-1'i uygula; CLAUDE/DESIGN kurallarına uy; commit → run → düzelt:
   testi yaz → başarısız gör → testi commit'le (güvenlik ağı) → yeşil olana dek uygula
   → tam suite → commit. done = iddia değil KANIT (adımın → BK# GWT'sinin Then'i).
   İstenmeyen sonuçta GERİ AL: son yeşil commit'e dön (revert / çift-esc rewind),
   .md'leri düzelt, tekrar dene. Araç seti: /context (token kontrolü) · /effort ·
   plan mode (karmaşık adımda). Model/effort seçimi için KB *Claude Model Seçimi* +
   *Model Ayarları* notlarına bak (buraya gömme — bayatlar)."
6. CRITIC (DEFAULT — opsiyonel değil): ilk paketli işten sonra TAZE bir alt-ajanla
   diff'i PLAN.md + INTENT'e karşı denetlet — her gereksinim uygulandı mı, edge-case
   testli mi, kapsam-dışına taşma var mı? Critic'siz loop = ajanın kendi ödevini
   onaylaması (→ KB *Loop Engineering*). Kullanıcı açıkça vazgeçerse atlanır.
7. STATE'i son kez yaz (.kickoff/state.json: tüm dosyalar done, faz: "devredildi").
```

## 2. Otonom uç (opsiyonel) — PLAN → prd.json köprüsü

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

**Çapraz-referans:** `SKILL.md §6b` (buraya çağırır) · `references/akis-modlari.md §1` (faz `"devredildi"` → TAMAMLANMIŞ dalı) · `references/tutarlilik.md §6` (ön-koşuldaki kapanış geçişi). **Kaynak:** BMAD-METHOD · Anthropic *Effective harnesses for long-running agents* · KB *Ralph (prd.json)* · *Loop Engineering* · *AI Kodlamada Commit Disiplini* · *8 Pratik Claude Code Hook'u*.
