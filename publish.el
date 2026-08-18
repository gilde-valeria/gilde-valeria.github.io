;;; publish.el --- Publica las notas de teoría (.org) a HTML  -*- lexical-binding: t; -*-
;;
;; Se ejecuta en cada push desde .github/workflows (Emacs + ox-publish).
;; Para correrlo a mano desde la raíz del sitio:
;;
;;     emacs -Q --batch --load publish.el --funcall org-publish-all
;;
;; El diseño y el espaciado viven en teaching/teoria/notas.css, no aquí.

(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(package-initialize)

(require 'ox-publish)
(require 'ox-html)

;; --- ESTRUCTURA DEL HTML ---
(setq org-html-container-element "section")
;; El preámbulo es un div para poder meter dentro el <header> del sitio.
(setq org-html-divs '((preamble  "div"  "top")
                      (content   "main" "content")
                      (postamble "div"  "postamble")))

;; Sin el CSS ni los scripts que Org inyecta por omisión: usamos los del sitio.
(setq org-html-head-include-default-style nil)
(setq org-html-head-include-scripts nil)

;; Sin la línea "UP | HOME" arriba de todo.
(setq org-html-home/up-format "")

;; Las notas están en español.
(setq org-export-default-language "es")

(setq org-publish-project-alist
      (list
       (list "notas-concurrente"
             :base-directory "./teaching/teoria/"
             :base-extension "org"
             :publishing-directory "./teaching/teoria/"
             :recursive t
             :publishing-function 'org-html-publish-to-html
             :headline-levels 4
             :html-doctype "html5"
             :html-html5-fancy t
             :language "es"

             :html-head
             "<link href='https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap' rel='stylesheet'>
<link rel='stylesheet' href='/styles.css'>
<link rel='stylesheet' href='/teaching/practicas/practica.css'>
<link rel='stylesheet' href='/teaching/teoria/notas.css'>"

             ;; Encabezado oscuro igual al de las prácticas. %t es el título de la nota.
             :html-preamble
             "<div id='site-navbar'></div>
<header class='practica-hero'>
  <div class='practica-hero-inner'>
    <p class='eyebrow'>Cómputo Concurrente 2026 · Notas de teoría</p>
    <h1>%t</h1>
    <div class='practica-actions'>
      <a class='btn btn-primary' href='/teaching/teoria/'>Todas las notas</a>
      <a class='btn' href='/teaching/practicas/'>Prácticas</a>
      <a class='btn btn-ghost' href='/teaching/'>Volver a Teaching</a>
    </div>
  </div>
</header>"

             :html-postamble
             "<p class='back-link'><a href='/teaching/teoria/'>← Volver a las notas de teoría</a></p>
<div id='site-footer'></div>
<script type='module' src='/scripts/include-teaching.js'></script>"

             :with-toc t
             :with-author nil
             :with-date nil
             :with-creator nil
             :section-numbers nil)))

(message "Publicando las notas de teoría...")
