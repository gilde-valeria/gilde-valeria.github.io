#!/usr/bin/env python3
"""Convierte las prácticas .tex a HTML con pandoc + citeproc y genera el índice."""
import json, os, re, subprocess, shutil, pathlib

AQUI = pathlib.Path(__file__).resolve().parent
BUILD = pathlib.Path(os.environ.get("PRACTICAS_TEX", "."))  # carpeta con los .tex y sample.bib
SITE = pathlib.Path(os.environ.get("SITIO", pathlib.Path(__file__).resolve().parent.parent))
OUT = SITE / "teaching" / "practicas"
REPO = "https://github.com/gilde-valeria/FC_CConcurrente"

PRACTICAS = [
    dict(slug="p1-multihilos", codpage="codigos/p1.html", tex="practica1.tex", num="Práctica 1", curso="Cómputo Concurrente 2026",
         titulo="Repaso de Java e introducción a la programación multihilos",
         desc="Arquitecturas multihilo y multiprocesador, anatomía de la JVM, creación de hilos con Thread y Runnable, y la Ley de Amdahl.",
         pdf="practica1.pdf", codigos=f"{REPO}/tree/main/Programas_P1", vigente=True),
    dict(slug="p2-locks-pools", codpage="codigos/p2.html", tex="practica2.tex", num="Práctica 2", curso="Cómputo Concurrente 2026",
         titulo="Exclusión mutua: locks y pools en Java",
         desc="Condiciones de carrera y data races, synchronized, la interfaz Lock y pools de hilos con ExecutorService.",
         pdf="practica2.pdf", codigos=f"{REPO}/tree/main/Programas_P2", vigente=True),
    dict(slug="p3-jmm", codpage="codigos/p3.html", tex="practica3.tex", num="Práctica 3", curso="Cómputo Concurrente 2026",
         titulo="Candados clásicos y el modelo de memoria de Java",
         desc="Peterson, Lamport y compañía; reordenamiento, visibilidad y qué garantiza realmente el JMM.",
         pdf="practica3.pdf", codigos=f"{REPO}/tree/main/Programas_P3", vigente=True),
    dict(slug="p4-spinlocks", codpage="codigos/p4.html", tex="practica4.tex", num="Práctica 4", curso="Cómputo Concurrente 2026",
         titulo="Spinlocks y algunas primitivas",
         desc="TAS, TTAS, backoff exponencial y candados de cola. Comparación empírica de desempeño.",
         pdf="practica4.pdf", codigos=f"{REPO}/tree/main/Programas_P4", vigente=True),
    dict(slug="p5-snapshots", codpage="codigos/p5.html", tex="practica5.tex", num="Práctica 5", curso="Cómputo Concurrente 2026",
         titulo="Snapshots y collects: backups",
         desc="Linealizabilidad, collects atómicos, double-collect y verificación en tiempo de ejecución.",
         pdf="practica5.pdf", codigos=f"{REPO}/tree/main/Programas_P5", vigente=True,
         extra=[("Solución de la Práctica 5 (PDF)", "Solucion_Practica7.pdf")]),
    dict(slug="p6-monitores-consenso", codpage="codigos/p6.html", tex="practica6.tex", num="Práctica 6", curso="Cómputo Concurrente 2026",
         titulo="Monitores y consenso",
         desc="Sistemas síncronos, asíncronos y parcialmente síncronos; monitores, variables de condición y el problema del consenso.",
         pdf="practica6.pdf", codigos=f"{REPO}/tree/main/Programas_P6", vigente=True),
    dict(slug="p7-contadores", tex="practicaContadores.tex", num="Práctica 7", curso="Cómputo Concurrente 2026",
         titulo="Implementaciones de contadores: balance entre corrección y eficiencia",
         desc="Contador linealizable, sloppy counter y árbol de difracción. Linealizabilidad, consistencia secuencial, quiescente y eventual.",
         pdf="practicaContadores.pdf", codigos=REPO, vigente=True),
    dict(slug="p8-lenguajes", tex="practica6_Lenguajes.tex", num="Práctica 8", curso="Cómputo Concurrente 2026",
         titulo="De Java a Rust y Clojure: paradigmas de concurrencia",
         desc="Ownership y fearless concurrency en Rust, STM e identidad/estado en Clojure, y data races útiles. Con smart contracts como caso de estudio.",
         pdf="practica6_Lenguajes.pdf", codigos=REPO, vigente=True),
]

GUIA = dict(slug="guia-github", tex="colaborarGithub.tex", num="Guía", curso="Cómputo Concurrente 2026",
            titulo="Cómo agregar ejercicios a un repositorio de GitHub",
            desc="Clonar, hacer commit y subir tus soluciones paso a paso.",
            pdf=None, codigos=REPO, vigente=True)


def convert(p):
    src = BUILD / p["tex"]
    dest = OUT / f"{p['slug']}.html"
    meta = {
        "pagetitle": p["titulo"],
        "subtitle": p["num"],
        "course": p["curso"],
        "link-citations": True,
        "lang": "es",
    }
    if p.get("pdf"):
        meta["pdf"] = f"pdf/{p['pdf']}"
    if p.get("codigos"):
        meta["codigos"] = p["codigos"]
    if p.get("codpage"):
        meta["codigospage"] = p["codpage"]
    mf = BUILD / f"meta_{p['slug']}.json"
    mf.write_text(json.dumps(meta, ensure_ascii=False))
    cmd = [
        "pandoc", str(src), "-f", "latex", "-t", "html5", "--standalone",
        "--template", str(AQUI / "template.html"),
        "--citeproc", "--bibliography", str(BUILD / "sample.bib"),
        "--metadata-file", str(mf),
        "--mathjax", "--toc", "--toc-depth=2",
        "--shift-heading-level-by=1",
        "--highlight-style=breezedark",
        "--wrap=preserve",
        "-o", str(dest),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=BUILD)
    status = "ok" if r.returncode == 0 else "FALLO"
    warn = [l for l in r.stderr.splitlines() if "Citeproc" in l or "not found" in l]
    print(f"  [{status}] {p['slug']:24s} {dest.stat().st_size if dest.exists() else 0:>7} bytes"
          + (f"  ({len(warn)} avisos de citas)" if warn else ""))
    if r.returncode != 0:
        print(r.stderr[:1500])
        return False
    postprocess(dest)
    return True


LANGS = {"java": "java", "clojure": "clojure", "rust": "rust", "bash": "bash",
         "sh": "bash", "shell": "bash", "c": "c", "python": "python"}


def postprocess(path):
    """Limpia encabezados vacíos y normaliza los lenguajes de los bloques de código."""
    h = path.read_text(encoding="utf-8")
    # 1. Encabezados vacíos que vienen de \section*{}
    h = re.sub(r'<h[1-6][^>]*>\s*</h[1-6]>\n?', '', h)
    # 2. Entradas vacías en la tabla de contenido
    h = re.sub(r'<li><a href="#[^"]*"[^>]*>\s*</a></li>\n?', '', h)

    # 3. Lenguaje del bloque de código -> clase language-xxx para highlight.js
    def fix(m):
        lang = LANGS.get(m.group(1).lower(), "")
        cls = f' class="language-{lang}"' if lang else ""
        return f'<pre class="sourceCode {lang or m.group(1).lower()}"><code{cls}>'

    h = re.sub(r'<pre class="sourceCode ([A-Za-z+#]+)"><code[^>]*>', fix, h)

    # 4. Referencias tipo [[fig:...]] de Org que pandoc deja como enlaces rotos:
    #    se dejan como texto plano en lugar de un enlace que no lleva a ningún lado.
    h = re.sub(r'<a href="(?:fig|tab|sec):[^"]*">(.*?)</a>', r'\1', h, flags=re.S)
    path.write_text(h, encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("Convirtiendo prácticas:")
    for p in PRACTICAS + [GUIA]:
        convert(p)
