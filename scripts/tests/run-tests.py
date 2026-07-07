#!/usr/bin/env python3
"""
kickoff-verify regression testleri (v2 kontrol kapsamı dahil).
Her vaka: geçici dizinde geçerli bir kickoff-çıktısı kur → tek mutasyon → kickoff-verify
→ beklenen exit code + çıktı imzası. Fixture'lar programatik (repo'ya .md konmaz).

Kullanım: python3 scripts/tests/run-tests.py
Çıkış: 0 = tümü geçti, 1 = en az bir vaka düştü.
"""
import os, json, shutil, subprocess, sys, tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kickoff-verify.py")

INTENT = """# INTENT — Test Projesi

## Bağlam
Mevcut süreç elle yürüyor; hata oranı yüksek.

## Hedef
Kullanıcı tek komutla raporu üretebilsin.

## Kullanıcı
P1: Analist.

## Başarı Kriteri
- [ ] **BK1** Given veri hazır, When komut koşar, Then rapor 10 sn içinde üretilir · doğrulayıcı: [kod]
- [ ] **BK2** Given bozuk girdi, When komut koşar, Then anlaşılır hata döner · doğrulayıcı: [kod]

## Kapsam Dışı
- Web arayüzü.

## Riskler
- Veri şeması değişebilir → şema versiyonu pinlenir.
"""

PLAN = """# PLAN — Test Projesi

> Hedef (INTENT'ten): Kullanıcı tek komutla raporu üretebilsin.

## Adımlar
1. **CLI iskeleti** — komut + arg parse.
   - Doğrulama: --help çalışır.
   - Karşıladığı kriter: → BK1
   - commit: `cli: iskelet`
2. **Hata yolu** — bozuk girdi yakalama.
   - Doğrulama: bozuk dosyayla test.
   - Karşıladığı kriter: → BK2
   - commit: `cli: hata yolu`

## Kapsam-dışı bekçisi
- Web arayüzü — plana SIZMADI ✔

## Doğrulama özeti
- İki BK'nin testleri yeşil.
"""

CLAUDE = """# Proje
Tek komutla rapor üreten CLI.

# Stack
- Python 3.12

# Kurallar
- **Commit:** `<scope>: <açıklama>` (paketli iş başına).
- **Hafıza:** oturum başında MEMORY.md'yi oku; paketli iş sonrası MEMORY'e yazılacak var mı değerlendir.

# Yapma
- Web arayüzü ekleme.

---
> **Çatışma kuralı:** Dosyalar teknik konuda çelişirse **DESIGN.md kazanır.** INTENT kuzey yıldızıdır.
"""

DESIGN = """# DESIGN — Test Projesi

## A. Mimari Kararlar

### Stack seçimi
- **Karar:** CLI argparse; çıktı markdown rapor.
- **Gerekçe:** BK1 hızlı üretim; sıfır bağımlılık.
- **Neden diğeri değil:** click — ekstra bağımlılık.
"""

MEMORY = """# MEMORY — Test Projesi

## working — şu anki aktif bağlam
- Aktif adım: PLAN/Adım-1

## episodic — ne oldu, ne zaman
- 2026-07-02: kickoff tamamlandı.

## semantic — kalıcı gerçekler & kararlar
- Rapor formatı markdown (kaynak: DESIGN).

## procedural — nasıl-yapılır kalıpları
- test koşma → değişiklik sonrası → `pytest -q`
"""

DELTA_SPEC = """# DELTA — Rate limit

## Mevcut davranış
API sınırsız istek kabul ediyor.

## Hedef delta
/api uçları dakikada 60 istekle sınırlansın.

## Değişmeyecek INVARIANT'lar
- Mevcut testler hâlâ geçer.

## Kapsam sınırı
- Auth akışına dokunulmaz.

## Başarı Kriteri
- [ ] **BK1** Given 61 istek/dk, When limit aşılır, Then 429 döner · doğrulayıcı: [kod]

## Adımlar
1. **Limiter middleware** — ekle.
   - Doğrulama: 61. istek 429.
   - Karşıladığı kriter: → BK1
   - commit: `api: rate limit`
"""


def w(base, rel, content):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def state(base, mod="greenfield", faz="kickoff"):
    durum = ({"spec": "done"} if mod == "delta"
             else {k: "done" for k in ("intent", "plan", "claude", "design", "memory")})
    w(base, ".kickoff/state.json", json.dumps({
        "mod": mod, "faz": faz, "proje_koku": base,
        "durum": durum,
        "acik_sorular": [], "son_guncelleme": "2026-07-02"}))


def base_project(d):
    w(d, "INTENT.md", INTENT); w(d, "PLAN.md", PLAN); w(d, "CLAUDE.md", CLAUDE)
    w(d, "DESIGN.md", DESIGN); w(d, "MEMORY.md", MEMORY); state(d)


def base_delta(d):
    w(d, "docs/specs/rate-limit.md", DELTA_SPEC); state(d, mod="delta")


def run(d, delta=False, strict=False):
    cmd = [sys.executable, SCRIPT, d] + (["--delta"] if delta else []) + (["--strict"] if strict else [])
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout + r.stderr


CASES = []
def case(name, delta=False):
    def deco(fn):
        CASES.append((name, fn, delta))
        return fn
    return deco


@case("base: 5-dosya projesi TEMİZ (exit 0)")
def _(d):
    rc, out = run(d); assert rc == 0 and "TEMİZ" in out, out

@case("eksik dosya → ERROR")
def _(d):
    os.remove(os.path.join(d, "DESIGN.md"))
    rc, out = run(d); assert rc == 1 and "dosya yok: DESIGN.md" in out, out

@case("şablon kalıntısı <doldur → ERROR")
def _(d):
    open(os.path.join(d, "INTENT.md"), "a", encoding="utf-8").write("\n<doldur>\n")
    rc, out = run(d); assert rc == 1 and "şablon kalıntısı" in out, out

@case("INTENT bölümü boş (Kapsam Dışı) → ERROR")
def _(d):
    t = INTENT.replace("- Web arayüzü.\n", "")
    w(d, "INTENT.md", t)
    rc, out = run(d); assert rc == 1 and ("bölümü boş" in out or "madde imi yok" in out), out

@case("Risk satırında azaltma yok → ERROR")
def _(d):
    w(d, "INTENT.md", INTENT.replace("- Veri şeması değişebilir → şema versiyonu pinlenir.",
                                     "- Veri şeması değişebilir."))
    rc, out = run(d); assert rc == 1 and "azaltma" in out, out

@case("BK karşılanmıyor → ERROR")
def _(d):
    w(d, "PLAN.md", PLAN.replace("→ BK2", "→ BK1"))
    rc, out = run(d); assert rc == 1 and "BK2 hiçbir adımda" in out, out

@case("adım tanımsız BK'ye işaret → ERROR")
def _(d):
    w(d, "PLAN.md", PLAN.replace("→ BK2", "→ BK9"))
    rc, out = run(d); assert rc == 1 and "tanımsız BK9" in out, out

@case("CLAUDE çatışma kuralı yok → ERROR")
def _(d):
    w(d, "CLAUDE.md", CLAUDE.replace("**DESIGN.md kazanır.**", "belirsiz."))
    rc, out = run(d); assert rc == 1 and "Çatışma kuralı" in out, out

@case("MEMORY katmanı eksik → ERROR")
def _(d):
    w(d, "MEMORY.md", MEMORY.replace("## procedural — nasıl-yapılır kalıpları", "## kalıplar"))
    rc, out = run(d); assert rc == 1 and "katmanı eksik" in out, out

@case("state.json yok → ERROR")
def _(d):
    shutil.rmtree(os.path.join(d, ".kickoff"))
    rc, out = run(d); assert rc == 1 and "state.json YOK" in out, out

@case("state.json geçersiz mod → ERROR")
def _(d):
    state(d, mod="hibrit")
    rc, out = run(d); assert rc == 1 and "mod geçersiz" in out, out

@case("Hafıza kuralı yok → WARNING (exit 0; --strict 1)")
def _(d):
    w(d, "CLAUDE.md", CLAUDE.replace("- **Hafıza:** oturum başında MEMORY.md'yi oku; paketli iş sonrası MEMORY'e yazılacak var mı değerlendir.\n", ""))
    rc, out = run(d); assert rc == 0 and "Hafıza kuralı yok" in out, out
    rc2, _o = run(d, strict=True); assert rc2 == 1, _o

@case("MUST/ASLA enflasyonu → WARNING")
def _(d):
    open(os.path.join(d, "CLAUDE.md"), "a", encoding="utf-8").write(
        "\n- ASLA X. ASLA Y. MUST Z. NEVER Q. CRITICAL W. ASLA V.\n")
    rc, out = run(d); assert rc == 0 and "enflasyonu" in out, out

@case("doğrulayıcı sınıfı işaretsiz BK → WARNING")
def _(d):
    w(d, "INTENT.md", INTENT.replace(" · doğrulayıcı: [kod]", "", 1))
    rc, out = run(d); assert rc == 0 and "doğrulayıcı sınıfı işareti yok" in out, out

@case("delta: geçerli spec TEMİZ", delta=True)
def _(d):
    rc, out = run(d, delta=True); assert rc == 0 and "TEMİZ" in out, out

@case("delta: INVARIANT bölümü eksik → ERROR", delta=True)
def _(d):
    sp = os.path.join(d, "docs/specs/rate-limit.md")
    w(d, "docs/specs/rate-limit.md", DELTA_SPEC.replace("## Değişmeyecek INVARIANT'lar\n- Mevcut testler hâlâ geçer.\n\n", ""))
    rc, out = run(d, delta=True); assert rc == 1 and "bölüm eksik" in out, out

@case("delta: spec yok → ERROR", delta=True)
def _(d):
    shutil.rmtree(os.path.join(d, "docs"))
    rc, out = run(d, delta=True); assert rc == 1 and "hiç spec yok" in out, out

@case("delta: state mod!=delta → ERROR", delta=True)
def _(d):
    state(d, mod="greenfield")
    rc, out = run(d, delta=True); assert rc == 1 and "beklenen: delta" in out, out

# --- v2 vakaları ---

@case("v2: PLAN başlığı eksik (Kapsam-dışı bekçisi) → ERROR")
def _(d):
    w(d, "PLAN.md", PLAN.replace("## Kapsam-dışı bekçisi", "## Bekçi"))
    rc, out = run(d); assert rc == 1 and "PLAN başlığı eksik" in out, out

@case("v2: PLAN adımında Doğrulama satırı yok → ERROR")
def _(d):
    w(d, "PLAN.md", PLAN.replace("   - Doğrulama: --help çalışır.\n", ""))
    rc, out = run(d); assert rc == 1 and "adım 1" in out and "Doğrulama:" in out, out

@case("v2: PLAN adımında commit satırı yok → ERROR")
def _(d):
    w(d, "PLAN.md", PLAN.replace("   - commit: `cli: hata yolu`\n", ""))
    rc, out = run(d); assert rc == 1 and "adım 2" in out and "commit:" in out, out

@case("v2: DESIGN'de Karar ADR alanı yok → ERROR")
def _(d):
    w(d, "DESIGN.md", DESIGN.replace("- **Karar:** CLI argparse; çıktı markdown rapor.\n", ""))
    rc, out = run(d); assert rc == 1 and "**Karar:**" in out, out

@case("v2: .gitignore .kickoff'u dışlıyor → ERROR")
def _(d):
    w(d, ".gitignore", "node_modules/\n.kickoff/\n")
    rc, out = run(d); assert rc == 1 and ".gitignore" in out, out

@case("v2: GWT izi eksik BK → WARNING (exit 0; --strict 1)")
def _(d):
    w(d, "INTENT.md", INTENT.replace(
        "- [ ] **BK2** Given bozuk girdi, When komut koşar, Then anlaşılır hata döner · doğrulayıcı: [kod]",
        "- [ ] **BK2** Bozuk girdide anlaşılır hata döner · doğrulayıcı: [kod]"))
    rc, out = run(d); assert rc == 0 and "GWT izi" in out, out
    rc2, _o = run(d, strict=True); assert rc2 == 1, _o

@case("v2: state durum.plan anahtarı eksik → ERROR")
def _(d):
    w(d, ".kickoff/state.json", json.dumps({
        "mod": "greenfield", "faz": "kickoff", "proje_koku": d,
        "durum": {k: "done" for k in ("intent", "claude", "design", "memory")},
        "acik_sorular": [], "son_guncelleme": "2026-07-02"}))
    rc, out = run(d); assert rc == 1 and "durum.plan eksik" in out, out

@case("v2: delta ilk INVARIANT 'mevcut testler' değil → ERROR", delta=True)
def _(d):
    w(d, "docs/specs/rate-limit.md",
      DELTA_SPEC.replace("- Mevcut testler hâlâ geçer.", "- API şeması değişmez."))
    rc, out = run(d, delta=True); assert rc == 1 and "ilk INVARIANT" in out, out


def main():
    fails = 0
    for name, fn, delta in CASES:
        d = tempfile.mkdtemp(prefix="kickoffverify-test-")
        try:
            (base_delta if delta else base_project)(d)
            fn(d)
            print(f"  PASS  {name}")
        except AssertionError as e:
            fails += 1
            print(f"  FAIL  {name}")
            for ln in str(e).splitlines()[-20:]:
                print(f"        {ln}")
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(f"\n{len(CASES)-fails}/{len(CASES)} geçti")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
