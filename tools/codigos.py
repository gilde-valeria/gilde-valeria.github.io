#!/usr/bin/env python3
"""Genera páginas HTML con los códigos Java de cada práctica, tomados del repo."""
import html, os, pathlib, re, subprocess

REPO = "https://github.com/gilde-valeria/FC_CConcurrente"
AQUI = pathlib.Path(__file__).resolve().parent
BUILD = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(os.environ.get("REPO_CODIGOS", "/tmp/repo"))  # clon de FC_CConcurrente
LOCALES = pathlib.Path(os.environ.get("CODIGOS_LOCALES", ""))    # códigos que solo viven en un enunciado
OUT = pathlib.Path(os.environ.get("SITIO", pathlib.Path(__file__).resolve().parent.parent)) / "teaching/practicas/codigos"

# Cada grupo es una página. "carpeta" es la del repo; "solo" y "excluir" permiten
# repartir una carpeta entre dos prácticas (Programas_P6 trae monitores y consenso
# mezclados). "locales" añade archivos que no están en el repo, tomados del enunciado.
GRUPOS = [
    dict(slug="multihilos", carpeta="Programas_P1",
         titulo="Práctica 1 — Repaso de Java y multihilos", practica="multihilos"),
    dict(slug="locks-pools", carpeta="Programas_P2",
         titulo="Práctica 2 — Locks y pools", practica="locks-pools"),
    dict(slug="jmm", carpeta="Programas_P3",
         titulo="Práctica 3 — Candados clásicos y JMM", practica="jmm"),
    dict(slug="spinlocks", carpeta="Programas_P4",
         titulo="Práctica 4 — Spinlocks y primitivas", practica="spinlocks"),
    dict(slug="monitores-condiciones", carpeta="Programas_P6",
         titulo="Práctica 5 — Monitores: candados y condiciones",
         practica="monitores-condiciones",
         solo=["FifoReadWriteLock.java", "ExecReadersWriters.java", "CountDownLatch.java"],
         locales="codigos-p5",
         nota_locales="Estos tres salen del propio enunciado. Se les añadieron los "
                      "<em>imports</em>, un constructor para <code>LockedQueue</code> y los métodos "
                      "de <code>Lock</code> que el PDF omite, para que compilen tal cual."),
    dict(slug="snapshots", carpeta="Programas_P5",
         titulo="Snapshots y collects — material extra", practica="snapshots"),
    dict(slug="monitores-consenso", carpeta="Programas_P6",
         titulo="Práctica 6 — Monitores y consenso", practica="monitores-consenso",
         excluir=["FifoReadWriteLock.java", "ExecReadersWriters.java", "CountDownLatch.java"]),
    dict(slug="listas", carpeta="Listas",
         titulo="Listas concurrentes — material extra", practica=None),
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
      Puedes copiar cada archivo desde aquí, o clonar el repositorio
      <a href="{repo}" target="_blank" rel="noopener">FC_CConcurrente</a> completo:
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


def bloque_archivo(f, enlace=None):
    """Un <details> con el archivo resaltado; enlace es su URL en GitHub, si la tiene."""
    fuente = f.read_text(encoding="utf-8", errors="replace")
    lineas = fuente.count("\n") + 1
    ruta = (f'      <p class="fpath"><a href="{enlace}" target="_blank" rel="noopener">'
            f'{html.escape(enlace.split("/blob/main/")[-1])}</a></p>\n') if enlace else ""
    return (f'    <details class="code-file">\n'
            f'      <summary><span class="fname">{html.escape(f.name)}</span>'
            f'<span class="fmeta">{lineas} líneas</span></summary>\n'
            f'{ruta}'
            f'      {resaltar(fuente)}\n'
            f'    </details>\n')


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    generadas = []
    for g in GRUPOS:
        base = SRC / g["carpeta"]
        archivos = []
        if base.exists():
            archivos = sorted(base.rglob("*.java"), key=lambda p: (str(p.parent), p.name))
            if g.get("solo"):
                archivos = [f for f in archivos if f.name in g["solo"]]
            if g.get("excluir"):
                archivos = [f for f in archivos if f.name not in g["excluir"]]
        else:
            print(f"  [skip] {g['carpeta']} no existe")

        locales = []
        if g.get("locales"):
            d = (LOCALES / g["locales"]) if str(LOCALES) else pathlib.Path(g["locales"])
            if d.is_dir():
                locales = sorted(d.glob("*.java"))
            else:
                print(f"  [aviso] no encuentro los códigos locales en {d}")

        if not archivos and not locales:
            continue

        secciones = []
        if locales:
            secciones.append(
                '    <h2 class="seccion-titulo">Del enunciado</h2>\n'
                f'    <p class="seccion-intro">{g.get("nota_locales", "")}</p>\n'
                + "".join(bloque_archivo(f) for f in locales))
        if archivos:
            titulo_repo = "En el repositorio" if locales else "Archivos"
            secciones.append(
                f'    <h2 class="seccion-titulo">{titulo_repo}</h2>\n'
                + "".join(bloque_archivo(f, f"{REPO}/blob/main/{f.relative_to(SRC)}")
                          for f in archivos))

        cuerpo = ('    <div class="codigos-head"><h2 style="margin:0;border:none">Archivos</h2>'
                  '<button id="expand-all" class="btn" type="button">Expandir todo</button></div>\n'
                  + "".join(secciones))
        enun = (f'<a class="btn" href="/teaching/practicas/{g["practica"]}.html">Ver el enunciado</a>'
                if g.get("practica") else "")
        (OUT / f'{g["slug"]}.html').write_text(
            PAGE.format(titulo=html.escape(g["titulo"]), n=len(archivos) + len(locales), hlcss=HLCSS,
                        repo=f'{REPO}/tree/main/{g["carpeta"]}', repoclone=REPO,
                        enunciado=enun, cuerpo=cuerpo),
            encoding="utf-8")
        print(f'  [ok] codigos/{g["slug"]}.html — {len(archivos) + len(locales)} archivos'
              + (f' ({len(locales)} del enunciado)' if locales else ''))
        generadas.append(g["slug"])
    return generadas


if __name__ == "__main__":
    print("Generando páginas de códigos:")
    build()
