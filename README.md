# proje-kickoff — 5-Dosya Proje Orkestratörü (Claude Code Skill)

Yeni bir projeye/feature'a **kod yazmadan önce** sağlam bir iskelet kuran Claude Code skill'i: soru-cevaplı bir röportajla 5 temel `.md` dosyasını (**INTENT → PLAN → CLAUDE → DESIGN → MEMORY**) tek tek, birbiriyle tutarlı şekilde tasarlar ve proje köküne yazar. Bakım/bugfix/küçük feature için hafif **DELTA modu** (tek sayfalık change-spec) içerir.

> Kullanıcıya dönük yüz sade Türkçedir; motorun tekniği (tutarlılık geçitleri, durum dosyası, mekanik doğrulayıcı) arka planda çalışır.

## Ne yapar?

- **Röportaj → taslak → onay → yaz** döngüsü: her dosya başlık başlık soruyla derinleştirilir; onaysız hiçbir dosya yazılmaz, mevcut dosya asla körlemesine ezilmez.
- **Tutarlılık motoru:** her yeni karar öncekilerle teyit edilir; çelişki işaretlenir ve kullanıcıya sorulur (INTENT = kuzey yıldızı; teknik çatışmada DESIGN kazanır).
- **Kapanışta çift denetim:** taze bir alt-ajan 5 dosyayı çapraz tarar (taze-göz) + `kickoff-verify.py` mekanik kontratı doğrular (şablon kalıntısı, BK↔adım eşlemesi, bütünlük).
- **Devir:** iş, temiz bir kodlama oturumuna dosya-tabanlı reçeteyle devredilir (başlangıç commit'i, bütünlük hook'u önerisi, critic alt-ajanı, isteğe bağlı otonom loop köprüsü).
- **Oturum güvenliği:** her onaydan sonra `.kickoff/state.json` güncellenir; oturum koparsa kaldığı yerden devam eder.

## Kurulum

```bash
git clone https://github.com/mehmetemrebabac-vc/proje-kickoff ~/.claude/skills/proje-kickoff
```

## Kullanım

Claude Code'da boş bir sohbette:

```
/proje-kickoff
```

Skill; yeni proje / mevcut projeye büyük parça / küçük değişiklik ayrımını sorar ve uygun akışı yürütür. Bilgi/yaklaşım danışmak bu skill'in işi değildir (onun için kardeş skill: [ai-proje-rehberi](https://github.com/mehmetemrebabac-vc/ai-proje-rehberi)).

## Yapı

```
SKILL.md                  # çekirdek talimat + ilkeler (her çağrıda yüklenir)
references/               # ihtiyaç anında okunan motorlar
  tutarlilik.md           #   içerik geçidi + çelişki protokolü + kapanış matrisi
  akis-modlari.md         #   resume · mod · disk geçidi · plan-mode
  devir.md                #   kodlama fazına devir reçetesi (+ otonom uç)
  intent/plan/claude-md/design/memory.md   # dosya-başına playbook'lar
assets/templates/         # 5 dosya + DELTA şablonları
assets/examples/          # doldurulmuş few-shot örnekleri (INTENT · PLAN · DELTA)
scripts/kickoff-verify.py # mekanik doğrulayıcı (salt-okur; v2)
scripts/tests/            # regression testleri
docs/test-senaryolari.md  # davranış kontratı (model-tarafı mini-eval)
```

## Test

```bash
python3 scripts/tests/run-tests.py   # kickoff-verify regression paketi
```

## Lisans

[MIT](LICENSE)
