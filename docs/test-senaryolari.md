# Test Senaryoları — Davranış Kontratı (mini-eval)

> Her skill değişikliğinden sonra bu 5 senaryo elle (veya subagent'la) koşulur; beklenen
> davranıştan sapma = regresyon. Mekanik kontrat ayrı: `scripts/kickoff-verify.py`
> (+ `scripts/tests/run-tests.py` — 18 otomatik vaka). Bu dosya MODEL davranışını test
> eder — script'in göremediği kısmı. (KB *Gelişmiş Skill Mühendisliği* — eval seti;
> KB *Prompt Evals* — 3-5 örnekli mini-eval pratiği.)

## S1 — Greenfield basit
**Kurulum:** boş dizin; kullanıcı: "not alma CLI'ı yapacağım".
**Beklenen:** RESUME tetiklenmez → MOD sorusu (3 seçenek, AskUserQuestion) → funnel açılışı
("en tam haliyle anlat") → INTENT röportajı başlık başlık; BK# kimlikli + doğrulayıcı-sınıflı
kriterler; taslak-onay-yaz döngüsü; state.json her ONAY'da güncellenir.
**Regresyon işareti:** funnel atlanır; BK kimliksiz kriter; state.json yazılmaz.

## S2 — Brownfield, mevcut CLAUDE.md'li (false-positive tuzağı)
**Kurulum:** kökünde kullanıcının kendi `CLAUDE.md`'si olan repo; INTENT/PLAN/state.json YOK.
**Beklenen:** **RESUME TETİKLENMEZ** ("kaldığın yerden devam mı?" sorulMAZ); CLAUDE.md
brownfield keşif girdisi olur; CLAUDE adımında [B] Birleştir default'u, asla tam-overwrite.
**Regresyon işareti:** skill "[D] devam / [B] baştan" sorarsa → §1 ayrıştırıcı bozulmuş.

## S3 — Yarım kickoff resume
**Kurulum:** `.kickoff/state.json` (faz: kickoff, intent+plan done) + INTENT.md + PLAN.md mevcut.
**Beklenen:** gerçek RESUME → defter diskten re-derive → [D]/[B] sorusu (AskUserQuestion) →
[D]'de sıradaki eksik dosyadan (CLAUDE) devam; mevcut dosyalar disk geçidinden geçer.
**Regresyon işareti:** INTENT'e baştan başlar; defteri türetmeden devam eder.

## S4 — Çelişkili kullanıcı
**Kurulum:** INTENT'te "sıfır-backend statik site" onaylandı; DESIGN röportajında kullanıcı
"Postgres + auth API koyalım" der.
**Beklenen:** dikey ihlal tespiti (INTENT kuzey yıldızı) → çelişki İŞARETLENİR (üzerine
yazılmaz) → kullanıcıya seçenek: INTENT'i revize et (onayla) YA DA DESIGN'ı amaca hizala;
defterde `çözüldü→K#` izi.
**Regresyon işareti:** DESIGN sessizce Postgres'i yazar; INTENT sessizce güncellenir.

## S5 — "Bilmiyorum" diyen kullanıcı + DELTA yönlendirmesi
**Kurulum:** kullanıcı mevcut projesine "şu endpoint'e cache ekleyeceğim" der; Başarı
kriteri sorusuna "bilmiyorum" cevabı verir.
**Beklenen:** MOD sorusunda BROWNFIELD-DELTA önerilir (tam 5-dosya dayatılmaz); "bilmiyorum"a
makul varsayılan ÖNERİLİR + gerekçe + Riskler'e "varsayım" satırı; tek spec dosyası
`docs/specs/…` yazılır, DESIGN/MEMORY yazılmaz; kickoff-verify `--delta` koşulur.
**Regresyon işareti:** bakım işine 5 dosya dayatılır; "bilmiyorum" boş bırakılır ya da
sorgusuz geçilir.
