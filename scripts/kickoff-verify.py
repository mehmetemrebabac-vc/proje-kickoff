#!/usr/bin/env python3
"""
kickoff-verify.py v1 — kickoff çıktısının mekanik doğrulaması (SADECE OKUR).

Bu docstring, kontrol listesinin SSOT'udur (SKILL.md 6a buraya işaret eder).
Felsefe: kritik doğrulamada dil yerine script (KB *Claude Skills — Tam Rehber*).
6a kapanış matrisi (anlamsal tutarlılık) ile TAMAMLAYICIDIR, ikamesi değildir —
script yapısal/mekanik kontratı denetler, anlamı model + kullanıcı denetler.

NORMAL MOD (5-dosya) — ERROR (TEMİZ'i düşürür):
   1) 5 dosya varlığı — INTENT.md / PLAN.md / CLAUDE.md / DESIGN.md / MEMORY.md proje kökünde
   2) Şablon kalıntısı — `<doldur`, `<Proje / Feature Adı>`, `<adım adı>`, `<YYYY-AA-GG>`,
      `<tetik:` gibi doldurulmamış yer-tutucular (5 dosyada; kod blokları hariç)
   3) INTENT bütünlüğü — 6 başlık (Bağlam·Hedef·Kullanıcı·Başarı Kriteri·Kapsam Dışı·Riskler)
      mevcut ve DOLU; Kapsam Dışı ≥1 madde; her Risk satırında `→` (azaltma); Başarı
      Kriteri'nde ≥1 `**BK<N>**` kimlikli madde
   4) BK↔adım eşlemesi — INTENT'teki her BK, PLAN'da ≥1 adımın `→ BK<N>` referansında;
      PLAN'daki her `→ BK<N>` INTENT'te tanımlı
   5) CLAUDE bütünlüğü — `# Proje` `# Stack` `# Kurallar` `# Yapma` başlıkları + Çatışma
      kuralı satırı ("DESIGN.md kazanır")
   6) MEMORY bütünlüğü — 4 katman başlığı (working/episodic/semantic/procedural)
   7) DESIGN varlığı — boş/iskelet değil (≥1 `##` bölüm + yer-tutucusuz)
   8) state.json — .kickoff/state.json mevcut + geçerli JSON + şema: mod ∈
      {greenfield,brownfield,delta} · faz ∈ {kickoff,devredildi} · durum değerleri ∈
      {pending,in-progress,done} · proje_koku mevcut

DELTA MODU (--delta) — ERROR:
   D1) docs/specs/ altında ≥1 spec dosyası
   D2) Her spec'te bölümler: Mevcut davranış · Hedef delta · Değişmeyecek INVARIANT ·
       Kapsam sınırı · Başarı Kriteri · Adımlar — hepsi dolu
   D3) Spec-içi BK↔adım eşlemesi (madde 4 ile aynı kural)
   D4) Şablon kalıntısı + state.json (mod=="delta")
   (5-dosya kontrolleri UYGULANMAZ; CLAUDE.md varsa yalnız kalıntı taranır)

WARNING (raporlanır; --strict ile TEMİZ'i düşürür):
   W1) HTML yorum bloğu kalmış (`<!--` — muhtemel silinmemiş şablon rehberi)
   W2) CLAUDE `# Kurallar`'da Hafıza kuralı yok ("Hafıza"/"MEMORY" geçmiyor — devir
       sonrası hafıza döngüsü ölü doğar)
   W3) MUST/CRITICAL/ASLA enflasyonu — CLAUDE'da >5 bağırılan kural
   W4) Doğrulayıcı sınıfı işaretsiz BK (`[kod]`/`[judge]`/`[insan]` yok) veya
       kriterlerin yarıdan fazlası `[insan]` (koda itilmemiş)
   W5) INTENT >70 satır (≤1 sayfa hedefi)

Kullanım: python3 kickoff-verify.py <proje-kökü> [--delta] [--strict]
Çıkış: 0 = TEMİZ · 1 = ERROR (--strict ile WARNING de) · 2 = kullanım hatası.
"""
import os, re, sys, glob, json

FIVE = ["INTENT.md", "PLAN.md", "CLAUDE.md", "DESIGN.md", "MEMORY.md"]
PLACEHOLDERS = ["<doldur", "<Proje / Feature Adı>", "<Feature / Fix Adı>", "<adım adı>",
                "<YYYY-AA-GG>", "<tetik:", "<risk> → <azaltma>", "<ne yapılacak>"]
INTENT_HEADS = ["## Bağlam", "## Hedef", "## Kullanıcı", "## Başarı Kriteri",
                "## Kapsam Dışı", "## Riskler"]
DELTA_HEADS = ["## Mevcut davranış", "## Hedef delta", "## Değişmeyecek INVARIANT'lar",
               "## Kapsam sınırı", "## Başarı Kriteri", "## Adımlar"]
CLAUDE_HEADS = ["# Proje", "# Stack", "# Kurallar", "# Yapma"]
MEM_LAYERS = ["## working", "## episodic", "## semantic", "## procedural"]
BK_DEF = re.compile(r"\*\*BK(\d+)\*\*")
BK_REF = re.compile(r"→\s*BK(\d+)")

args = sys.argv[1:]
STRICT = "--strict" in args
DELTA = "--delta" in args
args = [a for a in args if a not in ("--strict", "--delta")]
if len(args) != 1 or not os.path.isdir(args[0]):
    print("Kullanım: kickoff-verify.py <proje-kökü> [--delta] [--strict]")
    sys.exit(2)
ROOT = args[0]

problems, warnings = 0, 0


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def strip_fences(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return re.sub(r"~~~.*?~~~", "", t, flags=re.S)


def err(msg):
    global problems
    print(f"   X {msg}")
    problems += 1


def warn(msg):
    global warnings
    print(f"   ⚠ {msg}")
    warnings += 1


def section_body(text, head, all_heads):
    """head ile bir sonraki bilinen başlık arası gövde ('' = bölüm yok)."""
    m = re.search(rf"^{re.escape(head)}\s*$(.*?)(?=^#{{1,2}} |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


def check_placeholders(path, label):
    t = strip_fences(read(path))
    for ph in PLACEHOLDERS:
        if ph in t:
            err(f"şablon kalıntısı `{ph}`: {label}")
    if "<!--" in t:
        warn(f"HTML yorum bloğu kalmış (silinmemiş şablon rehberi?): {label}")


def check_bk_mapping(intent_text, plan_text, label):
    """INTENT/spec BK tanımları ↔ PLAN/adım → BK referansları birebir eşleşmeli."""
    defs = set(BK_DEF.findall(strip_fences(intent_text)))
    refs = set(BK_REF.findall(strip_fences(plan_text)))
    if not defs:
        err(f"hiç **BK#** kimlikli başarı kriteri yok: {label}")
        return
    for bk in sorted(defs - refs, key=int):
        err(f"BK{bk} hiçbir adımda karşılanmıyor (→ BK{bk} referansı yok): {label}")
    for bk in sorted(refs - defs, key=int):
        err(f"adım, tanımsız BK{bk}'ye işaret ediyor (INTENT/spec'te yok): {label}")
    # W4 — doğrulayıcı sınıfı
    lines = [l for l in strip_fences(intent_text).splitlines() if BK_DEF.search(l)]
    unmarked = [l for l in lines if not re.search(r"\[(kod|judge|insan)\]", l)]
    if unmarked:
        warn(f"{len(unmarked)} BK'de doğrulayıcı sınıfı işareti yok ([kod|judge|insan]): {label}")
    insan = [l for l in lines if "[insan]" in l]
    if lines and len(insan) > len(lines) / 2:
        warn(f"kriterlerin yarıdan fazlası [insan] ({len(insan)}/{len(lines)}) — koda itilmemiş: {label}")


def check_state():
    p = os.path.join(ROOT, ".kickoff", "state.json")
    if not os.path.exists(p):
        err(".kickoff/state.json YOK (ZORUNLU — RESUME ayrıştırıcısının tek güvenilir sinyali)")
        return
    try:
        s = json.loads(read(p))
    except ValueError as e:
        err(f"state.json geçersiz JSON: {e}")
        return
    if s.get("mod") not in ("greenfield", "brownfield", "delta"):
        err(f"state.json mod geçersiz: {s.get('mod')!r} (greenfield|brownfield|delta)")
    if s.get("faz") not in ("kickoff", "devredildi"):
        err(f"state.json faz geçersiz: {s.get('faz')!r} (kickoff|devredildi)")
    if DELTA and s.get("mod") != "delta":
        err(f"--delta modunda state.json mod={s.get('mod')!r} (beklenen: delta)")
    if not s.get("proje_koku"):
        err("state.json proje_koku eksik")
    for k, v in (s.get("durum") or {}).items():
        if v not in ("pending", "in-progress", "done"):
            err(f"state.json durum.{k} geçersiz: {v!r}")


print(f"=== kickoff-verify · mod: {'DELTA' if DELTA else '5-DOSYA'} · kök: {ROOT} ===")

if DELTA:
    specs = sorted(glob.glob(os.path.join(ROOT, "docs", "specs", "*.md")))
    print(f"\n--- D1) SPEC VARLIĞI: {len(specs)} dosya ---")
    if not specs:
        err("docs/specs/ altında hiç spec yok (DELTA modu tek change-spec ister)")
    for sp in specs:
        label = os.path.relpath(sp, ROOT)
        t = read(sp)
        print(f"\n--- SPEC: {label} ---")
        check_placeholders(sp, label)
        for h in DELTA_HEADS:
            body = section_body(t, h, DELTA_HEADS)
            if body is None:
                err(f"bölüm eksik `{h}`: {label}")
            elif not body:
                err(f"bölüm boş `{h}`: {label}")
        check_bk_mapping(t, t, label)
    cl = os.path.join(ROOT, "CLAUDE.md")
    if os.path.exists(cl):
        check_placeholders(cl, "CLAUDE.md")
else:
    print("\n--- 1) 5 DOSYA VARLIĞI ---")
    missing = [f for f in FIVE if not os.path.exists(os.path.join(ROOT, f))]
    for f in missing:
        err(f"dosya yok: {f}")
    have = [f for f in FIVE if f not in missing]

    print("\n--- 2) ŞABLON KALINTISI ---")
    for f in have:
        check_placeholders(os.path.join(ROOT, f), f)

    if "INTENT.md" in have:
        print("\n--- 3) INTENT BÜTÜNLÜĞÜ ---")
        it = read(os.path.join(ROOT, "INTENT.md"))
        for h in INTENT_HEADS:
            body = section_body(it, h, INTENT_HEADS)
            if body is None:
                err(f"INTENT başlığı eksik: `{h}`")
            elif not body:
                err(f"INTENT bölümü boş: `{h}`")
        kd = section_body(it, "## Kapsam Dışı", INTENT_HEADS) or ""
        if kd and not re.search(r"^- \S", kd, re.M):
            err("Kapsam Dışı'nda madde imi yok (≥1 `- madde` zorunlu — ASLA boş bırakılmaz)")
        rk = section_body(it, "## Riskler", INTENT_HEADS) or ""
        for line in rk.splitlines():
            if line.startswith("- ") and "→" not in line:
                err(f"Risk satırında azaltma (`→`) yok: '{line.strip()[:60]}'")
        if len(it.splitlines()) > 70:
            warn(f"INTENT {len(it.splitlines())} satır (>70 — ≤1 sayfa hedefini aşıyor)")

    if "INTENT.md" in have and "PLAN.md" in have:
        print("\n--- 4) BK ↔ ADIM EŞLEMESİ ---")
        check_bk_mapping(read(os.path.join(ROOT, "INTENT.md")),
                         read(os.path.join(ROOT, "PLAN.md")), "INTENT↔PLAN")

    if "CLAUDE.md" in have:
        print("\n--- 5) CLAUDE BÜTÜNLÜĞÜ ---")
        ct = read(os.path.join(ROOT, "CLAUDE.md"))
        for h in CLAUDE_HEADS:
            if not re.search(rf"^{re.escape(h)}\s*$", ct, re.M):
                err(f"CLAUDE başlığı eksik: `{h}`")
        if "DESIGN.md kazanır" not in ct:
            err("Çatışma kuralı satırı yok ('DESIGN.md kazanır' — şablonda AYNEN KALSIN işaretli)")
        if not re.search(r"Hafıza|MEMORY", ct):
            warn("CLAUDE `# Kurallar`'da Hafıza kuralı yok — devir sonrası MEMORY döngüsü ölü doğar")
        shouts = len(re.findall(r"\b(MUST|CRITICAL|ASLA|NEVER)\b", strip_fences(ct)))
        if shouts > 5:
            warn(f"MUST/CRITICAL/ASLA enflasyonu: {shouts} (bağırılan kural aşırı-tetiklenir; buda)")

    if "MEMORY.md" in have:
        print("\n--- 6) MEMORY BÜTÜNLÜĞÜ ---")
        mt = read(os.path.join(ROOT, "MEMORY.md"))
        for h in MEM_LAYERS:
            if not re.search(rf"^{re.escape(h)}", mt, re.M):
                err(f"MEMORY katmanı eksik: `{h}`")

    if "DESIGN.md" in have:
        print("\n--- 7) DESIGN VARLIĞI ---")
        dt = read(os.path.join(ROOT, "DESIGN.md"))
        if not re.search(r"^## ", dt, re.M):
            err("DESIGN.md'de hiç `##` bölüm yok (boş iskelet?)")

print("\n--- 8) STATE.JSON ---")
check_state()

tail = f" | uyarı: {warnings} ⚠" if warnings else ""
fail = problems > 0 or (STRICT and warnings > 0)
print(f"\nSONUÇ: {'TEMİZ ✅' if problems == 0 else f'{problems} sorun ❌'}{tail}")
sys.exit(1 if fail else 0)
