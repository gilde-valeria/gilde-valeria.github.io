import os
import subprocess

# Configuramos las carpetas donde tienes tus notas
TARGET_FOLDERS = ["content", "teaching/teoria", "teaching/practicas"]

def convert_org_to_md():
    for folder in TARGET_FOLDERS:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".org"):
                    org_path = os.path.join(root, file)
                    md_path = os.path.join(root, file.replace(".org", ".md"))
                    
                    print(f"Convertiendo: {org_path}")
                    
                    # Ejecutamos Pandoc
                    # -f org: entrada Org-mode
                    # -t gfm: salida GitHub Flavored Markdown
                    # --standalone: para que incluya metadatos si los hay
                    subprocess.run([
                        "pandoc", 
                        org_path, 
                        "-f", "org", 
                        "-t", "gfm", 
                        "--wrap=none",
                        "-o", md_path
                    ])

if __name__ == "__main__":
    convert_org_to_md()