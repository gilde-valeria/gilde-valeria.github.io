import os
import subprocess

def convert_recursive():
    # Caminamos por todo el repositorio
    for root, dirs, files in os.walk("."):
        # Ignoramos carpetas ocultas como .git o .github
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(".org"):
                org_path = os.path.join(root, file)
                md_path = os.path.join(root, file.replace(".org", ".md"))
                
                print(f"--- Procesando: {org_path} ---")
                try:
                    subprocess.run([
                        "pandoc", org_path, 
                        "-f", "org", 
                        "-t", "gfm", 
                        "--wrap=none",
                        "-o", md_path
                    ], check=True)
                except Exception as e:
                    print(f"Error convirtiendo {file}: {e}")

if __name__ == "__main__":
    convert_recursive()