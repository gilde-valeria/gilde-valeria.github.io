(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(package-initialize)

(require 'ox-publish)
(require 'ox-html)

;; --- MEJORA DE ESTILO Y CLASES ---
;; Esto envuelve el contenido en un contenedor que ya usas en tu web
(setq org-html-container-element "section")
(setq org-html-divs '((preamble  "header" "top")
                      (content   "main"   "content")
                      (postamble "footer" "postamble")))

;; Evita que Org-mode inyecte su propio CSS feo por defecto
(setq org-html-head-include-default-style nil)
(setq org-html-head-include-scripts nil)

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
             :html-link-up "../"
             :html-link-home "/"
             ;; Inyectamos el CSS y la fuente General Sans directamente
             :html-head "<link rel='stylesheet' href='../../styles.css'>
                         <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.css'>
                         <style>
                           body { font-family: 'General Sans', sans-serif; background-color: var(--bg-color); }
                           #content { max-width: 900px; margin: auto; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                           pre.src { background-color: #282c34; color: #abb2bf; padding: 1.5rem; border-radius: 8px; overflow: auto; }
                           .title { color: var(--miPink); font-size: 2.5rem; margin-bottom: 1rem; }
                         </style>"
             :html-preamble "<div id='site-navbar'></div>"
             :html-postamble "<div id='site-footer'></div>
                              <script type='module' src='/scripts/include-teaching.js'></script>"
             :with-toc t
             :section-numbers nil)))

(message "Protocolo de publicación optimizado ejecutándose...")