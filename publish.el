(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(package-initialize)

(require 'ox-publish)

;; Configuración de publicación
(setq org-publish-project-alist
      (list
       (list "notas-concurrente"
             :base-directory "./teaching/teoria/"
             :base-extension "org"
             :publishing-directory "./teaching/teoria/"
             :recursive t
             :publishing-function 'org-html-publish-to-html
             :headline-levels 4             
             :auto-preamble t
             :html-head "<link rel=\"stylesheet\" href=\"../../styles.css\" type=\"text/css\"/>"
             :html-preamble "<div id='site-navbar'></div>"
             :html-postamble "<div id='site-footer'></div>"
             :with-toc t
             :section-numbers nil
             :html-doctype "html5"
             :html-html5-fancy t)))

(print "¡Protocolo de publicación listo!")