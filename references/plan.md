# PLAN.md Playbook

> Soru: **Hangi sırayla?** INTENT'i **atomik, çalıştırılabilir, doğrulanabilir** adımlara böler. (Plan-Mode mantığı: her adım test edilebilir bir "paketli iş".)

## Nasıl
- INTENT'in **Hedef + Başarı kriteri**nden türet: **her başarı kriteri ≥1 adımla** karşılanmalı (hedef, adımların *toplamıyla* karşılanır).
- Adımları **bağımlılık sırasına** diz (önce-gelen, sonra-gelen net).
- Her adım **atomik** = tek "paketli iş" → **tek commit** (`<scope>: <açıklama>`, → KB *AI Kodlamada Commit Disiplini*).
- Her adımda iki şey yaz: **NE yapılacak** + **NASIL doğrulanacak** (mümkünse localhost'ta ayağa kaldır / test yaz / çıktı gözle).
- Her adımın **karşıladığı başarı kriterini** `→` ile işaretle (izlenebilirlik).
- Belirsiz teknik seçim (stack/araç/pattern) → `/ai-proje-rehberi`'ye danış; karar DESIGN.md'ye gider, PLAN ona hizalanır.

## Röportaj soruları
- *"Hangi adım olmadan diğerleri başlayamaz?"* (bağımlılık) · *"Bu adımın 'bitti' kanıtı ne?"* (doğrulama) · *"Bu tek commit'e sığar mı, yoksa böl?"* (atomiklik).

## Tutarlılık geçidi (zorunlu — `references/tutarlilik.md §3`, INTENT↔PLAN)
- [ ] Her başarı kriteri en az bir adımda karşılanıyor mu?
- [ ] **Kapsam-dışı** bir şeyi planlayan adım var mı? (varsa **çıkar** — kapsam-dışı bekçisi)
- [ ] Adım sırası bağımlılıklara uygun mu?
- [ ] Her adımın doğrulama yolu var mı?

## Çıktı
Proje kökünde `PLAN.md`. **Yazınca deftere damıt** (UYGULAMA katmanı). **Şablon:** `assets/templates/PLAN.md`. **Kaynak:** KB *5-Dosya Workflow'u* + *AI Kodlamada Commit Disiplini* (paketli iş = commit).
