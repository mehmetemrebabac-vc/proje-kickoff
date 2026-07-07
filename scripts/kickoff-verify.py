#!/usr/bin/env python3
"""
kickoff-verify.py v2 — kickoff çıktısının mekanik doğrulaması (SADECE OKUR).

Bu docstring, kontrol listesinin SSOT'udur (SKILL.md 6a buraya işaret eder).
Felsefe: kritik doğrulamada dil yerine script (KB *Claude Skills — Tam Rehber*).
6a kapanış matrisi (anlamsal tutarlılık — v3'te TAZE alt-ajan tarar) ile
TAMAMLAYICIDIR, ikamesi değildir: script yapısal/mekanik kontratı denetler,
anlamı taze-göz ajanı + kullanıcı denetler.

NORMAL MOD (5-dosya) — ERROR (TEMİZ'i düşürür):
   1) 5 dosya varlığı — INTENT.md / PLAN.md / CLAUDE.md / DESIGN.md / MEMORY.md proje kökünde
   2) Şablon kalıntısı — `<doldur`, `<Proje / Feature Adı>`, `<adım adı>`, `<YYYY-AA-GG>`,
      `<tetik:` gibi doldurulmamış yer-tutucular (5 dosyada; kod blokları hariç)
   3) INTENT bütünlüğü — 6 başlık (Bağlam·Hedef·Kullanıcı·Başarı Kriteri·Kapsam Dışı·Riskler)
      mevcut ve DOLU; Kapsam Dışı ≥1 madde; her Risk satırında `→` (azaltma); Başarı
      Kriteri'nde ≥1 `**BK<N>**` kimlikli madde
   4) BK↔adım eşlemesi — INTENT'teki her BK, PLAN'da ≥1 adımın `→ BK<N>` referansında;
      PLAN'daki her `→ BK<N>` INTENT'te tanımlı
   5) PLAN bütünlüğü (v2) — `## Adımlar` / `## Kapsam-dışı bekçisi` / `## Doğrulama özeti`
      başlıkları mevcut; ≥1 numaralı adım; her adım bloğunda `Doğrulama:` VE `commit:` satırı
   6) CLAUDE bütünlüğü — `# Proje` `# Stack` `# Kurallar` `# Yapma` başlıkları + Çatışma
      kuralı satırı ("DESIGN.md kazanır")
   7) MEMORY bütünlüğü — 4 katman başlığı (working/episodic/semantic/procedural)
   8) DESIGN bütünlüğü — ≥1 `##` bölüm + `Mimari Kararlar` başlığı (toleranslı: `A.` öneki
      opsiyonel) + ≥1 `**Karar:**` ve ≥1 `**Gerekçe:**` ADR alanı (v2)
   9) state.json — .kickoff/state.json mevcut + geçerli JSON + şema: mod ∈
      {greenfield,brownfield,delta} · faz ∈ {kickoff,devredildi} · durum değerleri ∈
      {pending,in-progress,done} · durum anahtar-seti (v2): normal modda 5 dosya anahtarı
      zorunlu, delta'da `spec` zorunlu (`claude` opsiyonel) · proje_koku mevcut
  10) .gitignore bekçisi (v2, her iki modda) — `.kickoff` ignore edilmişse ERROR
      (başka makinede RESUME ayrıştırıcısı kör kalır — akis-modlari.md §1)

DELTA MODU (--delta) — ERROR:
   D1) docs/specs/ altında ≥1 spec dosyası
   D2) Her spec'te bölümler: Mevcut davranış · Hedef delta · Değişmeyecek INVARIANT ·
       Kapsam sınırı · Başarı Kriteri · Adımlar — hepsi dolu
   D3) Spec-içi BK↔adım eşlemesi (madde 4 ile aynı kural)
   D4) Şablon kalıntısı + state.json (mod=="delta") + 10) .gitignore bekçisi
   D5) İlk INVARIANT (v2) — "Değişmeyecek INVARIANT'lar"ın ilk maddesi "Mevcut testler…"
   (5-dosya kontrolleri UYGULANMAZ; CLAUDE.md varsa yalnız kalıntı taranır)

WARNING (raporlanır; --strict ile TEMİZ'i düşürür):
   W1) HTML yorum bloğu kalmış (`<!--` — muhtemel silinmemiş şablon rehberi)
   W2) CLAUDE `# Kurallar`'da Hafıza kuralı yok ("Hafıza"/"MEMORY" geçmiyor — devir
       sonrası hafıza döngüsü ölü doğar)
   W3) MUST/CRITICAL/ASLA enflasyonu — CLAUDE'da >5 bağırılan kural
   W4) Doğrulayıcı sınıfı işaretsiz BK (`[kod]`/`[judge]`/`[insan]` yok) veya
       kriterlerin yarıdan fazlası `[insan]` (koda itilmemiş)
   W5) INTENT >70 satır (≤1 sayfa hedefi)
   W6) GWT izi (v2) — BK tanım satırında Given/When/Then üçlüsü eksik

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
PLAN_HEADS = ["## Adımlar", "## Kapsam-dışı bekçisi", "## Doğrulama özeti"]
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


def section_body(text, head):
    """head ile bir sonraki 1-2 seviyeli başlık arası gövde (None = bölüm yok)."""
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
    lines = [l for l in strip_fences(intent_text).splitlines() if BK_DEF.search(l)]
    # W4 — doğrulayıcı sınıfı
    unmarked = [l for l in lines if not re.search(r"\[(kod|judge|insan)\]", l)]
    if unmarked:
        warn(f"{len(unmarked)} BK'de doğrulayıcı sınıfı işareti yok ([kod|judge|insan]): {label}")
    insan = [l for l in lines if "[insan]" in l]
    if lines and len(insan) > len(lines) / 2:
        warn(f"kriterlerin yarıdan fazlası [insan] ({len(insan)}/{len(lines)}) — koda itilmemiş: {label}")
    # W6 — GWT izi
    nogwt = [l for l in lines
             if not (re.search(r"\bGiven\b", l, re.I) and re.search(r"\bWhen\b", l, re.I)
                     and re.search(r"\bThen\b", l, re.I))]
    if nogwt:
        warn(f"{len(nogwt)} BK'de GWT izi eksik (Given/When/Then): {label}")


def check_plan_structure(pt):
    for h in PLAN_HEADS:
        if not re.search(rf"^{re.escape(h)}\s*$", pt, re.M):
            err(f"PLAN başlığı eksik: `{h}`")
    body = section_body(pt, "## Adımlar")
    if body is None:
        return  # başlık hatası yukarıda verildi
    marks = list(re.finditer(r"^\s*(\d+)\.\s", body, re.M))
    if not marks:
        err("PLAN'da hiç numaralı adım yok (`## Adımlar` boş)")
        return
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        block = body[m.start():end]
        n = m.group(1)
        if "Doğrulama:" not in block:
            err(f"PLAN adım {n}'de `Doğrulama:` satırı yok (NE + NASIL doğrulanacak zorunlu)")
        if "commit:" not in block:
            err(f"PLAN adım {n}'de `commit:` satırı yok (paketli iş = tek commit)")


def check_design(dt):
    if not re.search(r"^## ", dt, re.M):
        err("DESIGN.md'de hiç `##` bölüm yok (boş iskelet?)")
        return
    if not re.search(r"^##\s+(A\.\s*)?Mimari Kararlar", dt, re.M | re.I):
        err("DESIGN'de `Mimari Kararlar` bölümü yok (şablon: `## A. Mimari Kararlar`)")
    if "**Karar:**" not in dt:
        err("DESIGN'de hiç `**Karar:**` ADR alanı yok (ADR-lite: Karar·Gerekçe·Neden diğeri değil)")
    if "**Gerekçe:**" not in dt:
        err("DESIGN'de hiç `**Gerekçe:**` ADR alanı yok (her karar bir INTENT kriterini taşımalı)")


def check_gitignore():
    p = os.path.join(ROOT, ".gitignore")
    if not os.path.exists(p):
        return
    for line in read(p).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ".kickoff" in s:
            err(f".gitignore `.kickoff`'u dışlıyor (`{s}`) — başka makinede RESUME kör kalır; satırı kaldır (akis-modlari.md §1)")


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
    durum = s.get("durum") or {}
    for k, v in durum.items():
        if v not in ("pending", "in-progress", "done"):
            err(f"state.json durum.{k} geçersiz: {v!r}")
    if DELTA:
        if "spec" not in durum:
            err("state.json durum.spec eksik (DELTA modunda zorunlu anahtar; `claude` opsiyonel)")
    else:
        for k in ("intent", "plan", "claude", "design", "memory"):
            if k not in durum:
                err(f"state.json durum.{k} eksik (5-dosya modunda zorunlu anahtar)")


print(f"=== kickoff-verify v2 · mod: {'DELTA' if DELTA else '5-DOSYA'} · kök: {ROOT} ===")

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
            body = section_body(t, h)
            if body is None:
                err(f"bölüm eksik `{h}`: {label}")
            elif not body:
                err(f"bölüm boş `{h}`: {label}")
        check_bk_mapping(t, t, label)
        inv = section_body(t, "## Değişmeyecek INVARIANT'lar")
        if inv:
            bullets = [l.strip() for l in inv.splitlines() if l.strip().startswith("- ")]
            if not bullets or "mevcut testler" not in bullets[0].lower():
                err(f"ilk INVARIANT 'Mevcut testler hâlâ geçer' değil (şablon kuralı — daima ilk satır): {label}")
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
            body = section_body(it, h)
            if body is None:
                err(f"INTENT başlığı eksik: `{h}`")
            elif not body:
                err(f"INTENT bölümü boş: `{h}`")
        kd = section_body(it, "## Kapsam Dışı") or ""
        if kd and not re.search(r"^- \S", kd, re.M):
            err("Kapsam Dışı'nda madde imi yok (≥1 `- madde` zorunlu — ASLA boş bırakılmaz)")
        rk = section_body(it, "## Riskler") or ""
        for line in rk.splitlines():
            if line.startswith("- ") and "→" not in line:
                err(f"Risk satırında azaltma (`→`) yok: '{line.strip()[:60]}'")
        if len(it.splitlines()) > 70:
            warn(f"INTENT {len(it.splitlines())} satır (>70 — ≤1 sayfa hedefini aşıyor)")

    if "INTENT.md" in have and "PLAN.md" in have:
        print("\n--- 4) BK ↔ ADIM EŞLEMESİ ---")
        check_bk_mapping(read(os.path.join(ROOT, "INTENT.md")),
                         read(os.path.join(ROOT, "PLAN.md")), "INTENT↔PLAN")

    if "PLAN.md" in have:
        print("\n--- 5) PLAN BÜTÜNLÜĞÜ ---")
        check_plan_structure(read(os.path.join(ROOT, "PLAN.md")))

    if "CLAUDE.md" in have:
        print("\n--- 6) CLAUDE BÜTÜNLÜĞÜ ---")
        ct = read(os.path.join(ROOT, "CLAUDE.md"))
        for h in CLAUDE_HEADS:
            if not re.search(rf"^{re.escape(h)}\s*$", ct, re.M):
                err(f"CLAUDE başlığı eksik: `{h}`")
        if "DESIGN.md kazanır" not in ct:
            err("Çatışma kuralı satırı yok ('DESIGN.md kazanır' — şablonda AYNEN KALIR işaretli)")
        if not re.search(r"Hafıza|MEMORY", ct):
            warn("CLAUDE `# Kurallar`'da Hafıza kuralı yok — devir sonrası MEMORY döngüsü ölü doğar")
        shouts = len(re.findall(r"\b(MUST|CRITICAL|ASLA|NEVER)\b", strip_fences(ct)))
        if shouts > 5:
            warn(f"MUST/CRITICAL/ASLA enflasyonu: {shouts} (bağırılan kural aşırı-tetiklenir; buda)")

    if "MEMORY.md" in have:
        print("\n--- 7) MEMORY BÜTÜNLÜĞÜ ---")
        mt = read(os.path.join(ROOT, "MEMORY.md"))
        for h in MEM_LAYERS:
            if not re.search(rf"^{re.escape(h)}", mt, re.M):
                err(f"MEMORY katmanı eksik: `{h}`")

    if "DESIGN.md" in have:
        print("\n--- 8) DESIGN BÜTÜNLÜĞÜ ---")
        check_design(read(os.path.join(ROOT, "DESIGN.md")))

print("\n--- 9) STATE.JSON ---")
check_state()

print("\n--- 10) .GITIGNORE BEKÇİSİ ---")
check_gitignore()

tail = f" | uyarı: {warnings} ⚠" if warnings else ""
fail = problems > 0 or (STRICT and warnings > 0)
print(f"\nSONUÇ: {'TEMİZ ✅' if problems == 0 else f'{problems} sorun ❌'}{tail}")
sys.exit(1 if fail else 0)
