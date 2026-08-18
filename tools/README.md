# Herramientas de publicación

Estos scripts convierten el material del curso a HTML y lo dejan dentro de
`teaching/`. Se ejecutan a mano cuando cambias una práctica; no forman parte del
workflow de GitHub Actions (ese solo publica los `.org` de `teaching/teoria/`).

## Qué hace cada uno

| Script | Entrada | Salida |
|---|---|---|
| `build.py` | los `.tex` de las prácticas + `sample.bib` | `teaching/practicas/*.html` con bibliografía resuelta |
| `notas.py` | los `.org` de `teaching/practicas/` | el `.html` correspondiente, con el mismo diseño |
| `codigos.py` | un clon del repo `FC_CConcurrente` | `teaching/practicas/codigos/*.html` |
| `referencias.py` | los `.tex` + `sample.bib` | `teaching/practicas/referencias.html` |

`template.html` es la plantilla de pandoc que da a todas las páginas el diseño
del sitio (navbar, footer, tabla de contenido lateral, botón de copiar código).
`hl.css` es el tema de resaltado de sintaxis, ya generado; se incrusta en cada
página para que el código se vea bien sin depender de ningún CDN.

## Requisitos

- `pandoc` 3 o superior — `brew install pandoc`
- Python 3
- Para regenerar los PDFs, una distribución de LaTeX (opcional)

## Cómo se usan

Desde esta carpeta, indicando dónde están los `.tex` y el clon del repo de códigos:

```bash
export PRACTICAS_TEX=~/Documents/Teach/5taClase-2026-1/Documentos/Practicas
export REPO_CODIGOS=~/FC_CConcurrente          # git clone del repo de códigos
export SITIO=..                                # la raíz del sitio

python3 build.py        # prácticas .tex -> HTML
python3 notas.py        # notas .org     -> HTML
python3 codigos.py      # códigos Java   -> HTML
python3 referencias.py  # bibliografía   -> HTML
```

## Cómo agregar una práctica nueva

1. Escribe el `.tex` y compílalo como siempre; copia el PDF a
   `teaching/practicas/pdf/`.
2. Agrega una entrada a la lista `PRACTICAS` en `build.py` (slug, título,
   descripción, PDF y enlace a los códigos).
3. Agrégala también a `TEX2PRACTICA` en `referencias.py` para que sus citas
   aparezcan en la bibliografía.
4. Vuelve a correr los scripts y añade una tarjeta en
   `teaching/practicas/index.html`.

## Notas

- Las citas `\cite{...}` se resuelven con `--citeproc` contra `sample.bib`, así
  que la bibliografía de cada práctica aparece al final y cada cita enlaza a su
  entrada. Si agregas una clave nueva, basta con que exista en `sample.bib`.
- `referencias.py` avisa en consola si alguna clave citada no está en el `.bib`.
- Las imágenes de las prácticas viven en `teaching/practicas/img/`; los `.tex`
  las referencian como `img/archivo.png`.
