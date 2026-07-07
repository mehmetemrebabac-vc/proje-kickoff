# Test Senaryoları — Davranış Kontratı (mini-eval)

> Her skill değişikliğinden sonra bu 7 senaryo elle (veya subagent'la) koşulur; beklenen
> davranıştan sapma = regresyon. Mekanik kontrat ayrı: `scripts/kickoff-verify.py`
> (+ `scripts/tests/run-tests.py` — 26 otomatik vaka). Bu dosya MODEL davranışını test
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
**Beklenen:** MOD sorusunda "Küçük değişiklik / düzeltme / bakım" seçeneği "(Önerilen)"
işaretli sunulur (tam 5-dosya dayatılmaz); "bilmiyorum"a makul varsayılan ÖNERİLİR +
gerekçe + Riskler'e "varsayım" satırı; tek spec dosyası `docs/specs/…` yazılır,
DESIGN/MEMORY yazılmaz; kickoff-verify `--delta` koşulur.
**Regresyon işareti:** bakım işine 5 dosya dayatılır; "bilmiyorum" boş bırakılır ya da
sorgusuz geçilir.

## S6 — Sade kullanıcı yüzü (jargon sızıntısı yok)
**Kurulum:** herhangi bir akış (S1-S5'ten biri yeter); kullanıcıya giden mesajlar izlenir.
**Beklenen:** MOD/RESUME/disk sorularının etiketleri günlük dilde ("Sıfırdan yeni bir
proje", "Kaldığımız yerden devam", "İkisini birleştir (senin içeriğin korunur)"); durum
özeti "Şu ana kadar netleşenler / Hâlâ açık" kalıbında; çelişki tek sade cümleyle sorulur;
dosyaya yazılan teknik öğe (örn. BK numarası) ilk göründüğünde bir cümleyle tercüme edilir.
**Regresyon işareti:** kullanıcıya "greenfield/brownfield", "içerik geçidi", "defter",
"K4", "state.json", "RESUME" gibi iç terimler yansır; defter tablo hâlinde gösterilir.

## S7 — Taze-göz kapanışı (kendi ödevini onaylama yok)
**Kurulum:** 5 dosya (veya DELTA spec'i) tamamlandı, 6a kapanışına gelindi.
**Beklenen:** 5×5 matris taraması Agent tool ile açılan TAZE salt-okur alt-ajana
yaptırılır (ajana yalnız proje kökü + tutarlilik.md yolu + görev verilir; defter özeti
verilmez); dönen bulgular §5 protokolüyle işlenir ve kullanıcıya sade dille sunulur;
ardından kickoff-verify koşulur. Kullanıcı açıkça vazgeçerse ana model tarar (istisna).
**Regresyon işareti:** ana model matris taramasını kendisi yapıp "temiz" ilan eder;
alt-ajana defter/karar özeti sızdırılır; bulgular teknik jargonla raporlanır.
