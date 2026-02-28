(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(package-initialize)

;; Forzamos la carga de Org y el exportador HTML
(require 'ox-publish)
(require 'ox-html)

;; SEGURIDAD: No preguntar nada al exportar (evita bloqueos en batch mode)
(setq org-confirm-babel-evaluate nil)
(setq org-export-with-broken-links t)
(setq vc-handled-backends nil) ; Desactivar control de versiones interno de Emacs

;; CONFIGURACIÓN DE RUTAS
(setq project-base-dir "./teaching/teoria/")
(setq project-pub-dir "./teaching/teoria/")

;; Crear el directorio de publicación si no existe (crucial)
(unless (file-exists-p project-pub-dir)
  (make-directory project-pub-dir t))

(setq org-publish-project-alist
      (list
       (list "notas-concurrente"
             :base-directory project-base-dir
             :base-extension "org"
             :publishing-directory project-pub-dir
             :recursive t
             :publishing-function 'org-html-publish-to-html
             :headline-levels 4
             :auto-preamble t
             ;; Ajustamos la ruta del CSS para que sea relativa al HTML generado
             :html-head "<link rel=\"stylesheet\" href=\"../../styles.css\" type=\"text/css\"/>"
             :html-preamble "<div id='site-navbar'></div>"
             :html-postamble "<div id='site-footer'></div>"
             :with-toc t
             :section-numbers nil
             :html-doctype "html5"
             :html-html5-fancy t)))

(message "Protocolo de publicación iniciado...")