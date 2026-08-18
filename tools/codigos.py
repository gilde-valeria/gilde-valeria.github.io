#!/usr/bin/env python3
"""Genera páginas HTML con los códigos Java de cada práctica, tomados del repo."""
import html, os, pathlib, re, subprocess

REPO = "https://github.com/gilde-valeria/FC_CConcurrente"
AQUI = pathlib.Path(__file__).resolve().parent
BUILD = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(os.environ.get("REPO_CODIGOS", "/tmp/repo"))  # clon de FC_CConcurrente
OUT = pathlib.Path(os.environ.get("SITIO", pathlib.Path(__file__).resolve().parent.parent)) / "teaching/practicas/codigos"

GRUPOS = [
    ("p1", "Programas_P1", "Práctica 1 — Repaso de Java y multihilos", "p1-multihilos"),
    ("p2", "Programas_P2", "Práctica 2 — Locks y pools", "p2-locks-pools"),
    ("p3", "Programas_P3", "Práctica 3 — Candados clásicos y JMM", "p3-jmm"),
    ("p4", "Programas_P4", "Práctica 4 — Spinlocks y primitivas", "p4-spinlocks"),
    ("p5", "Programas_P5", "Práctica 5 — Snapshots y collects", "p5-snapshots"),
    ("p6", "Programas_P6", "Práctica 6 — Monitores y consenso", "p6-monitores-consenso"),
    ("listas", "Listas", "Listas concurrentes — material extra", None),
]

HLCSS = (AQUI / "hl.css").read_text(encoding="utf-8")


def resaltar(fuente):
    """Devuelve el <pre> resaltado por pandoc para un archivo Java."""
    md = "```java\n" + fuente.replace("\r\n", "\n") + "\n```\n"
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5",
                        "--highlight-style=breezedark"],
                       input=md, capture_output=True, text=True)
    if r.returncode != 0:
        return "<pre><code>" + html.escape(fuente) + "</code></pre>"
    out = r.stdout.strip()
    # pandoc envuelve en <div class="sourceCode">; nos quedamos con el <pre>
    i, j = out.find("<pre"), out.rfind("</pre>")
    return out[i:j + 6] if i != -1 else out


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Códigos · {titulo}</title>
<meta name="description" content="Código fuente en Java de la {titulo} del curso de Cómputo Concurrente." />
<link href="https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/teaching/practicas/practica.css">
<style>
{hlcss}
</style>
</head>
<body>
<div id="site-navbar"></div>

<header class="practica-hero">
  <div class="practica-hero-inner">
    <p class="eyebrow">Códigos del curso</p>
    <h1>{titulo}</h1>
    <p class="practica-sub">{n} archivos Java · haz clic en cada uno para desplegarlo</p>
    <div class="practica-actions">
      <a class="btn btn-primary" href="{repo}" target="_blank" rel="noopener">Ver en GitHub</a>
      {enunciado}
      <a class="btn btn-ghost" href="/teaching/practicas/">Todas las prácticas</a>
    </div>
  </div>
</header>

<main class="practica-layout" style="grid-template-columns:1fr">
  <article class="practica-body">
    <p class="muted" style="margin-top:0">
      Estos son los mismos archivos que están en el repositorio
      <a href="{repo}" target="_blank" rel="noopener">FC_CConcurrente</a>.
      Puedes copiarlos desde aquí o clonar el repo completo:
    </p>
    <div class="code-wrap"><pre><code>git clone {repoclone}.git</code></pre></div>
{cuerpo}
    <p class="back-link"><a href="/teaching/practicas/">← Volver al índice de prácticas</a></p>
  </article>
</main>

<div id="site-footer"></div>
<script type="module" src="/scripts/include-teaching.js"></script>
<script>
document.querySelectorAll('pre').forEach(function (pre) {{
  var b = document.createElement('button');
  b.className = 'copy-btn'; b.type = 'button'; b.textContent = 'Copiar';
  b.addEventListener('click', function () {{
    navigator.clipboard.writeText(pre.innerText).then(function () {{
      b.textContent = '¡Copiado!';
      setTimeout(function () {{ b.textContent = 'Copiar'; }}, 1600);
    }});
  }});
  var wrap = document.createElement('div');
  wrap.className = 'code-wrap';
  pre.parentNode.insertBefore(wrap, pre);
  wrap.appendChild(b); wrap.appendChild(pre);
}});
document.getElementById('expand-all').addEventListener('click', function () {{
  var abrir = this.dataset.state !== 'open';
  document.querySelectorAll('details').forEach(function (d) {{ d.open = abrir; }});
  this.dataset.state = abrir ? 'open' : 'closed';
  this.textContent = abrir ? 'Contraer todo' : 'Expandir todo';
}});
</script>
</body>
</html>
"""


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    generadas = []
    for slug, carpeta, titulo, practica in GRUPOS:
        base = SRC / carpeta
        if not base.exists():
            print(f"  [skip] {carpeta} no existe")
            continue
        archivos = sorted(base.rglob("*.java"), key=lambda p: (str(p.parent), p.name))
        if not archivos:
            continue
        partes = []
        for f in archivos:
            rel = f.relative_to(SRC)
            fuente = f.read_text(encoding="utf-8", errors="replace")
            lineas = fuente.count("\n") + 1
            bloque = resaltar(fuente)
            partes.append(
                f'    <details class="code-file">\n'
                f'      <summary><span class="fname">{html.escape(f.name)}</span>'
                f'<span class="fmeta">{lineas} líneas</span></summary>\n'
                f'      <p class="fpath"><a href="{REPO}/blob/main/{rel}" target="_blank" '
                f'rel="noopener">{html.escape(str(rel))}</a></p>\n'
                f'      {bloque}\n'
                f'    </details>\n'
            )
        cuerpo = (
            '    <div class="codigos-head"><h2 style="margin:0;border:none">Archivos</h2>'
            '<button id="expand-all" class="btn" type="button">Expandir todo</button></div>\n'
            + "".join(partes)
        )
        enun = (f'<a class="btn" href="/teaching/practicas/{practica}.html">Ver el enunciado</a>'
                if practica else "")
        (OUT / f"{slug}.html").write_text(
            PAGE.format(titulo=html.escape(titulo), n=len(archivos), hlcss=HLCSS,
                        repo=f"{REPO}/tree/main/{carpeta}", repoclone=REPO,
                        enunciado=enun, cuerpo=cuerpo),
            encoding="utf-8")
        print(f"  [ok] codigos/{slug}.html — {len(archivos)} archivos")
        generadas.append(slug)
    return generadas


if __name__ == "__main__":
    print("Generando páginas de códigos:")
    build()
