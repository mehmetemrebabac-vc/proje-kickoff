# INTENT.md Playbook — Niyet Sözleşmesi

> İlk ve en kritik dosya; **plan ve koddan ÖNCE** yazılır. İnsanın *ne istediğini* tek dosyada netleştirir. Kısa tut (≤1 sayfa), cevaplar mümkünse tek cümle. Yaşam döngüsü: **Oluştur → Tartış → Arşivle.** Tutarlılıkta **AMAÇ katmanı = kuzey yıldızı** (→ `references/tutarlilik.md §1`).

## 6 Başlık — TEK TEK röportajla (her birini yeterince derinleştir)
Her başlık için soru bankasından başla; yüzeyde kalma, somutlaşana dek **takip sorusu** sor.

1. **## Bağlam** — Şu an ne durumda? Hangi sistem/süreç? Hangi acı/eksik?
   - *"Bugün bu olmadan nasıl yapıyorsun?"* · *"En çok ne canını sıkıyor?"* · *"Bu sorun ne sıklıkta / kime dokunuyor?"*
2. **## Hedef** — Ne istiyoruz? **TEK cümlede.** Çözümü değil **sonucu** yaz.
   - *"Bittiğinde tek cümleyle ne demiş olacağız?"* · *"Bunu bir cümleye indirsek, hangi kelime düşemez?"*
3. **## Kullanıcı** — Kim için? Hangi rol?
   - *"Birinci kullanıcı kim, ikincil kim?"* (çok rol varsa **P1/P2** önceliklendir) · *"Onun günü bununla nasıl değişir?"*
4. **## Başarı kriteri** — Nasıl ölçeriz? **Sayılabilir/test edilebilir liste.**
   - Her madde için: *"**Given** <durum>, **When** <eylem>, **Then** <ölçülebilir sonuç>"* tekniğiyle somutla.
   - *"Bu maddeyi nasıl test ederiz, hangi sayı/eşik?"* — "hızlı/iyi/kolay" gibi muğlak sıfatları kov.
5. **## Kapsam dışı** — Bu görevde **YAPMAYACAKLARIMIZ.** Planı dağılmaktan korur — **ASLA atlama/boş bırakma.**
   - *"Neyi bilerek dışarıda bırakıyoruz?"* · *"Hangi 'olsa güzel'leri bu sürüme almıyoruz?"*
6. **## Riskler** — Bilinen tuzaklar + **her birine azaltma planı** (`<risk> → <azaltma>`).
   - *"En olası başarısızlık nedeni ne?"* · *"Hangi varsayım yanlış çıkarsa her şey çöker?"*

## Derinlik kuralı
Yüzeyde kalma: somutlaşana, ölçülebilir/tek-cümle olana dek takip sorusu sor. Gerekirse benzer projeleri/repo'ları araştırıp örnek getir (titizlik > hız).

## Kalite kapısı (yazmadan önce)
- [ ] Hedef **tek cümle** mi (sonuç odaklı, çözüm değil)? · [ ] Başarı kriterleri **sayılabilir** mi? · [ ] **Kapsam-dışı** dolu mu? · [ ] Riskler azaltmalı mı? · [ ] ≤1 sayfa mı?

## Çıktı
Proje kökünde `INTENT.md` (veya görev-bazlı: `docs/intent/<feature>.md`). Sistem dosyası değil — CLAUDE.md'den referansla. **Yazınca deftere damıt** (`tutarlilik.md §2`): Hedef/Kapsam-dışı/Başarı = AMAÇ katmanı, kesin.
**Şablon:** `assets/templates/INTENT.md`. **Kaynak:** KB *5-Dosya Workflow'u (INTENT, PLAN, CLAUDE, DESIGN, MEMORY)* (6 başlık otorite); ölçülebilirlik tekniği: spec-driven development (Given/When/Then) — yardımcı.
