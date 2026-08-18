#!/usr/bin/env python3
"""Convierte los .org de prácticas/notas a HTML con la misma plantilla del sitio."""
import json, os, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import postprocess

AQUI = pathlib.Path(__file__).resolve().parent
BUILD = pathlib.Path(__file__).resolve().parent
SITE = pathlib.Path(os.environ.get("SITIO", pathlib.Path(__file__).resolve().parent.parent))
P = SITE / "teaching" / "practicas"
REPO = "https://github.com/gilde-valeria/FC_CConcurrente"

NOTAS = [
    dict(src=P / "hpc.org", out=P / "hpc.html", num="Material extra",
         curso="Cómputo Concurrente 2026",
         titulo="Paralelismo con OpenMP: memoria compartida, corrección y escalabilidad",
         desc="Directivas de OpenMP, regiones paralelas, reducciones y análisis de escalabilidad."),
    dict(src=P / "monitores.org", out=P / "monitores.html", num="Material extra",
         curso="Cómputo Concurrente 2026",
         titulo="Monitores y variables de condición — ejemplos en Java",
         desc="Ejemplos autocontenidos con wait/notify y las condiciones de la interfaz Lock."),
    dict(src=P / "reentrant.org", out=P / "reentrant.html", num="Material extra",
         curso="Cómputo Concurrente 2026",
         titulo="Construyendo un candado reentrante desde cero",
         desc="Cómo se implementa la reentrancia paso a paso, desde un candado simple."),
    dict(src=P / "concurrencia-lenguajes/de-java-a-rust.org",
         out=P / "concurrencia-lenguajes/de-java-a-rust.html", num="Guía de apoyo · Práctica 8",
         curso="Cómputo Concurrente 2026", titulo="Guía de concurrencia: Java → Rust",
         desc="Ownership, borrowing, Arc/Mutex y por qué el compilador rechaza tus data races.",
         volver="/teaching/practicas/p8-lenguajes.html"),
    dict(src=P / "concurrencia-lenguajes/de-java-a-clojure.org",
         out=P / "concurrencia-lenguajes/de-java-a-clojure.html", num="Guía de apoyo · Práctica 8",
         curso="Cómputo Concurrente 2026", titulo="Guía de concurrencia: Java → Clojure",
         desc="Identidad y estado, atoms, refs y memoria transaccional de software (STM).",
         volver="/teaching/practicas/p8-lenguajes.html"),
    dict(src=P / "1-intro--multihilos/intro--multihilos.org",
         out=P / "1-intro--multihilos/intro--multihilos.html", num="Nota de apoyo · Práctica 1",
         curso="Cómputo Concurrente", titulo="¿Multihilo, multicore o multiprocesador?",
         desc="Las tres palabras que todo el mundo confunde, con diagramas de arquitectura.",
         volver="/teaching/practicas/p1-multihilos.html"),
]


def convert(n):
    if not n["src"].exists():
        print(f"  [skip] no existe {n['src'].name}")
        return
    meta = {"pagetitle": n["titulo"], "subtitle": n["num"], "course": n["curso"], "lang": "es"}
    mf = BUILD / f"meta_org_{n['out'].stem}.json"
    mf.write_text(json.dumps(meta, ensure_ascii=False))
    n["out"].parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pandoc", str(n["src"]), "-f", "org", "-t", "html5", "--standalone",
           "--template", str(AQUI / "template.html"), "--metadata-file", str(mf),
           "--mathjax", "--toc", "--toc-depth=2", "--shift-heading-level-by=1",
           "--wrap=preserve", "-o", str(n["out"])]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [FALLO] {n['out'].name}\n{r.stderr[:800]}")
        return
    postprocess(n["out"])
    print(f"  [ok] {n['out'].relative_to(SITE)}  {n['out'].stat().st_size:>7} bytes")


if __name__ == "__main__":
    print("Convirtiendo notas .org:")
    for n in NOTAS:
        convert(n)
