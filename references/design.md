# DESIGN.md Playbook — Mimari & Tasarım Dili

> Soru: **Nasıl kurulu?** İki bölüm: **(A) Mimari Kararlar** (her zaman) + **(B) Tasarım Dili** (UI varsa). Tutarlılıkta **teknik hakem** = PLAN/CLAUDE/DESIGN teknik çelişirse **DESIGN kazanır** (ama INTENT amacını ezemez → `references/tutarlilik.md §1`). **Başkasının DESIGN.md'si performans vermez → İÇSELLEŞTİR.**

## A. Mimari Kararlar (her zaman)
Her kilit kararı **ADR-lite** yaz: **Karar · Gerekçe · Neden diğeri değil.**
- Kapsam: stack gerekçeleri, veri modeli/akış, sınırlar/katmanlar, entegrasyonlar, kilit trade-off'lar.
- Her karar bir INTENT başarı kriterini/sınırını **taşımalı** (amaca hizmet).
- Belirsiz mimari/araç → `/ai-proje-rehberi`'ye danış; gerekirse referans repo'ları aç-incele.

### Mimari karar check-listi (UI olsun olmasın — ADR-hafif)
Her kilit teknik karar için kısa ADR kaydı (özellikle **non-UI** projelerde DESIGN'ın asıl gövdesi budur):
- [ ] **Karar:** ne seçildi (tek cümle)
- [ ] **Bağlam/güç:** hangi kısıt/INTENT kriteri bunu zorladı
- [ ] **Alternatifler:** elenen ≥1 seçenek + neden elendi
- [ ] **Sonuç/ödünleşim:** kazanılan + feda edilen (perf/karmaşıklık/kilitlenme)
- [ ] **Sınır:** değişmeyecek invariant (brownfield'da mevcut kontrat)

Kapsanması gereken **non-UI eksenler:** veri modeli/şema · API/arayüz kontratları · hata-yönetimi & idempotency · eşzamanlılık/state · gözlemlenebilirlik · güvenlik sınırı · dağıtım/runtime. Her ADR'yi INTENT başarı kriterine demirle.

## B. Tasarım Dili (UI projesiyse — yoksa atla)
`google-labs-code/design.md` formatı: **token (makine-okunur) + prose (NEDEN).**
- **Token'lar (yaml):** `colors` (primary/secondary/tertiary=tek vurgu/neutral=zemin), `typography` (h1/body/mono: fontFamily+fontSize+weight), `rounded`, `spacing`, `components`. Referans: `{colors.primary}`.
- **Prose — sıralı `##` bölümler:** Overview · Colors · Typography · Layout & Spacing · (Elevation) · (Shapes) · Components · Do's & Don'ts. Her bölüm token kararının gerekçesi.
- **Kendi palet/font'un** — genel değil, projeye/kullanıcıya özel ("statement"/minimal vb. ton).
- **Açık-kaynak hızlandırıcılar:** palet/ton İLHAMI için KB *awesome-design-md — AI Ajanları için Hazır DESIGN.md Koleksiyonu* (73+ hazır dosya; **kopyalama — içselleştir**, yukarıdaki ilke). Token bloğu yazılınca opsiyonel mekanik doğrulama: google-labs `design.md` CLI `lint` komutu (yapı + WCAG kontrast; makinede kuruluysa — üret-sonra-doğrula ruhu).

## Tutarlılık geçidi (`references/tutarlilik.md §3`)
- [ ] Mimari, INTENT başarı kriterlerini destekliyor mu? Kapsam-dışını mimariye sızdırmıyor mu? (INTENT↔DESIGN)
- [ ] Her PLAN adımı bu mimariyle uygulanabilir mi? (PLAN↔DESIGN)
- [ ] CLAUDE `# Stack`/`# Kurallar` ile çelişen var mı? → **çelişirse DESIGN kazanır, CLAUDE'u güncelle** (bilinçli, gerekçeli).

## Çıktı
Proje kökünde `DESIGN.md`. **Yazınca deftere damıt** (UYGULAMA katmanı; teknik hakem). **Şablon:** `assets/templates/DESIGN.md`. **Kaynak:** KB *DESIGN.md — AI-Okunur Tasarım Sistemi Spec'i (Google Labs)* (token+prose formatı) + *5-Dosya Workflow'u*.
