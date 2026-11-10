"""Bangun laporan PDF dari laporan/laporan_final.md (markdown-it-py + Chrome/Edge headless).

Pakai: python scripts/build_report_pdf.py ["<url-video-demo>"]
Dua lintasan: lintasan 1 menentukan halaman tiap judul, lintasan 2 mengisi nomor halaman di daftar isi.
"""
import csv, html as H, re, subprocess, sys, tempfile
from pathlib import Path
from markdown_it import MarkdownIt

LAP = Path(__file__).resolve().parents[1] / "laporan"
SRC, OUT = LAP / "laporan_final.md", LAP / "laporan_final.pdf"
DEFAULT_DEMO = "https://youtu.be/CK6UM8pfm84"
DEMO = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DEMO
STUDENT = {"nama": "Muhammad Daffa Raihan", "nim": "25917045", "repo": "https://github.com/Dffarhn2004/basketball-jugling-detector"}
PER_MENIT = [124, 139, 137, 134, 134, 135, 135, 135, 133, 133, 136, 136, 134, 134, 133, 135, 136, 133, 133, 136]
BROWSER = next(p for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if Path(p).exists())

CSS = """
@page { size: A4; margin: 22mm 18mm 20mm 18mm;
  @top-left { content: "The Juggling Bounces Challenge"; font: 8pt Calibri, sans-serif; color: #777; }
  @top-right { content: "Laporan Proyek Deep Learning"; font: 8pt Calibri, sans-serif; color: #777; }
  @bottom-center { content: counter(page); font: 9pt Calibri, sans-serif; color: #777; } }
@page :first { margin: 0; @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
:root { --navy: #111; --accent: #555; --soft: #f4f4f4; --line: #cfcfcf; --ink: #1a1a1a; }
* { box-sizing: border-box; }
body { font: 10.3pt/1.55 Calibri, "Segoe UI", sans-serif; color: #333; margin: 0; text-align: left; overflow-wrap: anywhere; }
h1, h2 { font-family: Cambria, Georgia, serif; color: var(--navy); text-align: left; }
h1 { font-size: 19pt; margin: 0 0 10pt; padding-bottom: 5pt; border-bottom: 1pt solid #111; break-before: page; }
h1.first { break-before: auto; }
h2 { font-size: 12.5pt; margin: 15pt 0 5pt; break-after: avoid; }
p { margin: 0 0 6pt; } ul, ol { margin: 0 0 7pt; padding-left: 18pt; } li { margin-bottom: 2.5pt; }
strong, b { color: #000; font-weight: 800; } a { color: #111; text-decoration: underline; }
code { font: 8.8pt Consolas, monospace; background: #f0f0f0; padding: 0 2.5pt; border-radius: 2pt; }
pre { font: 8.4pt/1.45 Consolas, monospace; background: #f6f6f6; border: .6pt solid var(--line); border-left: 3pt solid #777;
      padding: 7pt 9pt; white-space: pre-wrap; text-align: left; break-inside: avoid; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 7pt 0 10pt; font-size: 8.9pt; line-height: 1.38; text-align: left; }
tbody tr, thead tr { break-inside: avoid; } thead { display: table-header-group; }
thead th { white-space: nowrap; background: #e9e9e9; color: #111; font-weight: 700; padding: 4pt 6pt; border: .6pt solid #9a9a9a; }
tbody td { padding: 3.4pt 6pt; border: .6pt solid var(--line); vertical-align: top; }
blockquote { margin: 8pt 0 10pt; padding: 7pt 11pt; background: var(--soft); border-left: 4pt solid #111; color: #111; break-inside: avoid; }
blockquote p { margin: 0; }
figure { margin: 9pt 0; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 52mm; border: .6pt solid var(--line); }
figure img[src*="cvat"] { max-height: 100mm; }
figure img[src*="e2_training"], figure img[src*="e2_pr_curve"], figure img[src*="e2_confusion"] { max-height: 100mm; width: 100%; object-fit: contain; }
figure img[src*="iou_dekat"], figure img[src*="lintasan_aturan"] { max-height: 95mm; width: 100%; object-fit: contain; }
figcaption { font-size: 8.7pt; color: #555; margin-top: 3pt; text-align: center; }
.stats { display: flex; gap: 7pt; margin: 9pt 0 11pt; break-inside: avoid; }
.stats div { flex: 1; background: var(--soft); border-top: 1.5pt solid #555; padding: 7pt 8pt; text-align: left; }
.stats b { display: block; font: 700 15pt Cambria, serif; color: #111; margin-bottom: 2pt; }
.stats span { font-size: 8.2pt; color: #444; line-height: 1.3; display: block; }
.flow { display: flex; align-items: stretch; gap: 3pt; margin: 9pt 0 11pt; break-inside: avoid; }
.flow div:not(.arrow) { flex: 1; border: .8pt solid #777; background: var(--soft); padding: 6pt 5pt; text-align: center; }
.flow b { display: block; color: var(--navy); font-size: 9.6pt; margin-bottom: 2pt; }
.flow span { font-size: 7.8pt; line-height: 1.3; color: #444; display: block; }
.flow .arrow { align-self: center; color: #555; font-size: 15pt; }
.chart { margin: 6pt 0 10pt; break-inside: avoid; } .chart svg { width: 100%; height: auto; }
table.keep { break-inside: avoid; } table[data-num] td:first-child, table[data-num] th:first-child { white-space: nowrap; }
p:has(+ table), p:has(+ pre), li:last-child { break-after: avoid; } p:has(+ table) { orphans: 3; }
/* sampul */
.cover { height: 297mm; width: 210mm; padding: 0; position: relative; break-after: page; text-align: left; background: #fff; }
.cover .band { background: #fff; color: #111; padding: 52mm 22mm 14mm; margin: 0 22mm; padding-left: 0; padding-right: 0; border-bottom: 1.4pt solid #111; }
.cover .band small { letter-spacing: 2.5pt; font-size: 9pt; color: #666; text-transform: uppercase; }
.cover .band h1 { color: #111; border: none; font-size: 31pt; line-height: 1.12; margin: 8pt 0 8pt; break-before: auto; padding: 0; }
.cover .band p { font-size: 12pt; color: #444; margin: 0; }
.cover .body { padding: 12mm 22mm 0; }
.cover .meta { width: 100%; font-size: 10.5pt; margin: 0 0 10mm; }
.cover .meta td { border: none; border-bottom: .6pt solid var(--line); padding: 5pt 2pt; background: none !important; }
.cover .meta td:first-child { width: 36mm; color: #666; }
.cover .demo { border: 1pt solid #555; background: var(--soft); padding: 9pt 12pt; margin: 0 0 8mm; font-size: 10.5pt; }
.cover .demo b { color: #111; }
.cover .abs { font-size: 10pt; color: #333; line-height: 1.55; }
.cover .foot { position: absolute; left: 22mm; right: 22mm; bottom: 16mm; font-size: 8.5pt; color: #777; border-top: .6pt solid var(--line); padding-top: 5pt; }
/* daftar isi */
.toc { break-after: page; text-align: left; } .toc h1 { break-before: auto; }
.toc .row { display: flex; align-items: baseline; font-size: 9.4pt; margin: 0; padding: .7pt 0; }
.toc .row .dots { flex: 1; border-bottom: .8pt dotted #999; margin: 0 4pt; transform: translateY(-2pt); }
.toc .l1 { font-weight: 700; color: var(--navy); margin-top: 4pt; } .toc .l2 { padding-left: 14pt; font-size: 8.8pt; color: #333; }
"""

def gt_per_menit() -> list[int]:
    """GT per menit dari hasil compare_full_count.py (kosong bila belum ada)."""
    f = Path(__file__).resolve().parents[1] / "artifacts/runs/Phase5_full_gt_eval/per_minute.csv"
    if not f.exists(): return []
    with f.open(encoding="utf8", newline="") as fh: return [int(r["gt"]) for r in csv.DictReader(fh)]


def chart_svg() -> str:
    w, h, pl, pb, top = 640, 190, 34, 26, 14
    mx = 150; bw = (w - pl - 8) / len(PER_MENIT); out = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Calibri,sans-serif">']
    for v in (0, 50, 100, 150):
        y = h - pb - (h - pb - top) * v / mx
        out.append(f'<line x1="{pl}" x2="{w-4}" y1="{y:.1f}" y2="{y:.1f}" stroke="#dddddd" stroke-width=".8"/><text x="{pl-5}" y="{y+3:.1f}" font-size="9" fill="#555" text-anchor="end">{v}</text>')
    for i, v in enumerate(PER_MENIT):
        x = pl + i * bw + 3; bh = (h - pb - top) * v / mx; y = h - pb - bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-6:.1f}" height="{bh:.1f}" fill="#9a9a9a" rx="1.5"/>'
                   f'<text x="{x+(bw-6)/2:.1f}" y="{y-3:.1f}" font-size="8" fill="#333" text-anchor="middle">{v}</text>'
                   f'<text x="{x+(bw-6)/2:.1f}" y="{h-pb+12}" font-size="9" fill="#555" text-anchor="middle">{i+1}</text>')
    gt = gt_per_menit()
    for i, v in enumerate(gt[:len(PER_MENIT)]):                       # titik GT manual di atas batang pipeline
        cx = pl + i * bw + 3 + (bw - 6) / 2; cy = h - pb - (h - pb - top) * v / mx
        out.append(f'<polygon points="{cx:.1f},{cy-4:.1f} {cx+4:.1f},{cy:.1f} {cx:.1f},{cy+4:.1f} {cx-4:.1f},{cy:.1f}" fill="#111" stroke="#fff" stroke-width=".8"/>')
    out.append(f'<text x="{w/2}" y="{h-2}" font-size="9" fill="#555" text-anchor="middle">Menit ke-</text></svg>')
    return ('<figure class="chart">' + "".join(out) +
            '<figcaption>Bounce per menit pada video 20 menit: batang = pipeline (total 2.685), belah ketupat hitam = GT manual (2.702 tanda mentah).</figcaption></figure>')

def render_body(md_text: str):
    md_text = md_text.replace("{{DEMO_URL}}", DEMO or "(tautan video belum diisi)")
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    body = md.render(md_text).replace("<!--CHART_PER_MENIT-->", chart_svg())
    body = re.sub(r"<p>(<img [^>]*alt=\"([^\"]*)\"[^>]*>)</p>", lambda m: f"<figure>{m.group(1)}<figcaption>Gambar. {H.escape(m.group(2))}</figcaption></figure>", body)
    body = re.sub(r"<table>(.*?)</table>", lambda m: ("<table class=\"keep\">" if m.group(1).count("<tr>") <= 6 else "<table>") + m.group(1) + "</table>", body, flags=re.S)
    body = re.sub(r"<table(?: class=\"keep\")?>\s*<thead>\s*<tr>\s*<th>(?:#|No\.|Menit)</th>", lambda m: m.group(0).replace("<table", "<table data-num=\"1\"", 1), body)   # kolom nomor tidak dipotong
    n = [0]
    def num(m): n[0] += 1; return m.group(0).replace("Gambar.", f"Gambar {n[0]}.", 1)
    body = re.sub(r"<figcaption>Gambar\.[^<]*</figcaption>", num, body)
    heads, idx = [], [0]
    def hid(m):
        idx[0] += 1; text = re.sub(r"<[^>]+>", "", m.group(2)); heads.append((m.group(1), H.unescape(text), f"h{idx[0]}"))
        return f'<h{m.group(1)} id="h{idx[0]}">{m.group(2)}</h{m.group(1)}>'
    body = re.sub(r"<h([12])>(.*?)</h\1>", hid, body)
    body = body.replace("<h1 id=\"h1\">", "<h1 class=\"first\" id=\"h1\">", 1)
    return body, heads

def cover(demo: str) -> str:
    link = H.escape(demo) if demo else "<i>[isi tautan video demo (YouTube Unlisted) di sini]</i>"
    return f"""<section class="cover"><div class="band"><small>Deep Learning · S2 · Tugas 1</small>
<h1>The Juggling Bounces Challenge</h1><p>Menghitung sentuhan bola basket ke lantai dengan deteksi, tracking, dan deteksi event temporal</p></div>
<div class="body"><div class="demo"><b>Video demonstrasi:</b> {link}</div>
<table class="meta"><tr><td>Nama</td><td>{H.escape(STUDENT["nama"])}</td></tr><tr><td>NIM</td><td>{H.escape(STUDENT["nim"])}</td></tr>
<tr><td>Mata kuliah</td><td>Deep Learning (S2 – B)</td></tr><tr><td>Tenggat</td><td>14 November 2026</td></tr>
<tr><td>Kode sumber</td><td>{H.escape(STUDENT["repo"])}</td></tr></table>
<p class="abs"><b>Ringkasan.</b> Pipeline terdiri dari detector YOLO26n yang di-fine-tune pada 111 gambar beranotasi sendiri, asosiasi deteksi berbasis jarak, dan
aturan titik terendah lintasan di zona lantai. Pada seluruh video 20 menit pipeline menghitung 2.685 bounce, dibandingkan ground truth manual
2.697 (selisih −12, APE 0,44%); selisih per menit paling besar 3 bounce. Ground truth ditandai satu orang tanpa pemeriksaan kedua, sehingga
akurasi 100% tidak diklaim.</p></div>
<div class="foot">Laporan proyek · November 2026</div></section>"""

def toc(heads, pages) -> str:
    rows = []
    for lvl, text, hid in heads:
        pg = pages.get(hid, "")
        rows.append(f'<div class="row l{lvl}"><span>{H.escape(text)}</span><span class="dots"></span><span>{pg}</span></div>')
    return '<section class="toc"><h1>Daftar Isi</h1>' + "".join(rows) + "</section>"

def build_html(body, heads, pages, demo) -> str:
    return (f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>The Juggling Bounces Challenge</title><style>{CSS}</style></head><body>'
            + cover(demo) + toc(heads, pages) + body + "</body></html>")

def to_pdf(html: str, out: Path) -> None:
    tmp = Path(tempfile.mkdtemp()) / "r.html"
    # gambar relatif ke folder laporan: simpan HTML di LAP agar path 'gambar/...' valid
    tmp = LAP / "_laporan_build.html"; tmp.write_text(html, encoding="utf-8")
    try:
        subprocess.run([BROWSER, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", tmp.as_uri()], check=True)
    finally:
        tmp.unlink(missing_ok=True)

def pdf_pages(pdf: Path) -> list[str]:
    n = int(re.search(r"Pages: (\d+)", subprocess.run(["mutool", "info", str(pdf)], capture_output=True, text=True).stdout).group(1))
    return [subprocess.run(["mutool", "draw", "-F", "txt", "-o", "-", str(pdf), str(i)], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout for i in range(1, n + 1)]

def norm(s: str) -> str: return re.sub(r"\W+", "", s).lower()

if __name__ == "__main__":
    body, heads = render_body(SRC.read_text(encoding="utf-8"))
    to_pdf(build_html(body, heads, {}, DEMO), OUT)                       # lintasan 1
    texts = [norm(t) for t in pdf_pages(OUT)]; pages, start = {}, 2     # halaman 1 sampul, 2 daftar isi
    for lvl, text, hid in heads:
        key = norm(text)[:40]
        for i in range(start, len(texts)):
            if key in texts[i]: pages[hid] = i + 1; start = i; break
    to_pdf(build_html(body, heads, pages, DEMO), OUT)                    # lintasan 2
    missing = [t for _, t, h in heads if h not in pages]
    print("OK", OUT, OUT.stat().st_size, "halaman:", len(texts), "| judul tanpa halaman:", missing)
