(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(package-initialize)

(require 'ox-publish)
(require 'ox-html)

;; --- MEJORA DE ESTILO Y CLASES ---
(setq org-html-container-element "section")
(setq org-html-divs '((preamble  "header" "top")
                      (content   "main"   "content")
                      (postamble "footer" "postamble")))

;; Evita que Org-mode inyecte su propio CSS por defecto
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
             ;; --- CSS DINÁMICO E IMÁGENES RESPONSIVAS ---
             :html-head "<link rel='stylesheet' href='../../styles.css'>
                         <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.css'>
                         <style>
                           body { font-family: 'General Sans', sans-serif; background-color: #fcfcfc; }
                           #content { max-width: 900px; margin: auto; padding: 2rem; background: white; border-radius: 12px; }
                           
                           /* IMÁGENES RESPONSIVAS */
                           img { max-width: 100%; height: auto; display: block; margin: 1.5rem auto; border-radius: 8px; }

                           /* TABLAS ESTILO ACADÉMICO */
                           table {
                             width: 100%;
                             border-collapse: collapse;
                             margin: 2rem 0;
                             font-size: 0.95rem;
                             border-radius: 8px;
                             overflow: hidden;
                             box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
                           }
                           th { background-color: var(--miPink, #ff4b82); color: white; text-align: left; padding: 12px 15px; }
                           td { padding: 12px 15px; border-bottom: 1px solid #f2f2f2; }
                           tr:nth-of-type(even) { background-color: #f9f9f9; }
                           tr:last-of-type { border-bottom: 2px solid var(--miPink, #ff4b82); }

                           /* MODO CELULAR: Las tablas se vuelven verticales */
                           @media screen and (max-width: 600px) {
                             table, thead, tbody, th, td, tr { display: block; }
                             thead tr { position: absolute; top: -9999px; left: -9999px; }
                             tr { border: 1px solid #ccc; margin-bottom: 10px; border-radius: 8px; }
                             td { border: none; border-bottom: 1px solid #eee; position: relative; padding-left: 50%; text-align: right; }
                             td:before { 
                               position: absolute; top: 12px; left: 15px; width: 45%; 
                               padding-right: 10px; white-space: nowrap; font-weight: bold;
                               content: attr(data-th); /* Requiere un pequeño hack en el exportador */
                               text-align: left;
                             }
                           }

                           pre.src { background-color: #282c34; color: #abb2bf; padding: 1.5rem; border-radius: 8px; overflow: auto; }
                           .title { color: var(--miPink); font-size: 2.5rem; margin-bottom: 1rem; }
                         </style>"
             :html-preamble "<div id='site-navbar'></div>"
             :html-postamble "<div id='site-footer'></div>
                              <script type='module' src='/scripts/include-teaching.js'></script>"
             :with-toc t
             :section-numbers nil)))

(message "Protocolo de publicación optimizado ejecutándose...")