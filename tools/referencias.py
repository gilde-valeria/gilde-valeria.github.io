#!/usr/bin/env python3
"""Genera la página de bibliografía del curso a partir de sample.bib."""
import glob, html, json, os, pathlib, re, subprocess

BUILD = pathlib.Path(os.environ.get("PRACTICAS_TEX", "."))
OUT = pathlib.Path(os.environ.get("SITIO", pathlib.Path(__file__).resolve().parent.parent)) / "teaching/practicas/referencias.html"

# slug -> (etiqueta, archivo html)
TEX2PRACTICA = {
    "practica1.tex": ("Práctica 1", "p1-multihilos.html"),
    "practica2.tex": ("Práctica 2", "p2-locks-pools.html"),
    "practica3.tex": ("Práctica 3", "p3-jmm.html"),
    "practica4.tex": ("Práctica 4", "p4-spinlocks.html"),
    "practica5.tex": ("Práctica 5", "p5-snapshots.html"),
    "practica6.tex": ("Práctica 6", "p6-monitores-consenso.html"),
    "practicaContadores.tex": ("Práctica 7", "p7-contadores.html"),
    "practica6_Lenguajes.tex": ("Práctica 8", "p8-lenguajes.html"),
}


def citas_por_practica():
    uso = {}
    for tex, info in TEX2PRACTICA.items():
        p = BUILD / tex
        if not p.exists():
            continue
        s = re.sub(r"(?m)^\s*%.*$", "", p.read_text(encoding="utf-8", errors="replace"))
        for m in re.finditer(r"\\cite[a-zA-Z]*\{([^}]*)\}", s):
            for k in (x.strip() for x in m.group(1).split(",")):
                if k:
                    uso.setdefault(k, []).append(info)
    return {k: list(dict.fromkeys(v)) for k, v in uso.items()}


def bibliografia_html(keys):
    md = BUILD / "_refs.md"
    md.write_text(
        "---\nnocite: |\n  " + " ".join(f"@{k}" for k in sorted(keys)) +
        "\nlang: es\n---\n", encoding="utf-8")
    r = subprocess.run(
        ["pandoc", str(md), "--citeproc", "--bibliography", str(BUILD / "sample.bib"),
         "-t", "html5", "--metadata", "link-citations=true"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[:1000])
    return r.stdout


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Bibliografía del curso · Cómputo Concurrente</title>
<meta name="description" content="Bibliografía completa citada en las prácticas del curso de Cómputo Concurrente." />
<link href="https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/teaching/practicas/practica.css">
</head>
<body>
<div id="site-navbar"></div>

<header class="practica-hero">
  <div class="practica-hero-inner">
    <p class="eyebrow">Cómputo Concurrente</p>
    <h1>Bibliografía del curso</h1>
    <p class="practica-sub">{n} obras citadas a lo largo de las prácticas</p>
    <div class="practica-actions">
      <a class="btn btn-primary" href="sample.bib" download>Descargar sample.bib</a>
      <a class="btn btn-ghost" href="/teaching/practicas/">Todas las prácticas</a>
    </div>
  </div>
</header>

<main class="practica-layout" style="grid-template-columns:1fr">
  <article class="practica-body">
    <p class="muted" style="margin-top:0">
      Cada entrada indica en qué prácticas aparece citada. Si usas LaTeX para tus reportes,
      puedes descargar el archivo <code>sample.bib</code> y citar con las mismas claves.
    </p>
    <h2 id="obras-citadas">Obras citadas</h2>
{bib}
    <p class="back-link"><a href="/teaching/practicas/">← Volver al índice de prácticas</a></p>
  </article>
</main>

<div id="site-footer"></div>
<script type="module" src="/scripts/include-teaching.js"></script>
</body>
</html>
"""


def main():
    uso = citas_por_practica()
    bib = bibliografia_html(uso.keys())

    bib = re.sub(r'<div id="ref-([^"]+)"[^>]*>((?:(?!</div>).)*)</div>',
                 lambda m: m.group(0)[:-6] + anotar_inner(m, uso) + "</div>",
                 bib, flags=re.S)
    OUT.write_text(PAGE.format(n=len(uso), bib=bib), encoding="utf-8")
    print(f"  [ok] referencias.html — {len(uso)} obras, {OUT.stat().st_size} bytes")
    faltan = [k for k in uso if f'id="ref-{k}"' not in bib]
    if faltan:
        print(f"  [aviso] claves sin entrada en sample.bib: {faltan}")


def anotar_inner(m, uso):
    etiquetas = uso.get(m.group(1), [])
    if not etiquetas:
        return ""
    chips = "".join(f'<a class="ref-chip" href="{a}">{html.escape(l)}</a>' for l, a in etiquetas)
    return f'<p class="ref-usos">Citada en: {chips}</p>'


if __name__ == "__main__":
    print("Generando bibliografía:")
    main()
