import os
import subprocess

# Usamos la ruta absoluta del proyecto para evitar líos
base_path = os.getcwd()
TARGET_FOLDERS = ["content", "teaching/teoria", "teaching/practicas"]

def convert_org_to_md():
    for folder in TARGET_FOLDERS:
        full_folder_path = os.path.join(base_path, folder)
        if not os.path.exists(full_folder_path):
            print(f"Saltando {folder}: No existe.")
            continue
            
        for root, dirs, files in os.walk(full_folder_path):
            for file in files:
                if file.endswith(".org"):
                    org_path = os.path.join(root, file)
                    md_path = os.path.join(root, file.replace(".org", ".md"))
                    
                    print(f"Convertiendo: {org_path}")
                    subprocess.run([
                        "pandoc", org_path, 
                        "-f", "org", 
                        "-t", "gfm", 
                        "--wrap=none",
                        "-o", md_path
                    ])

if __name__ == "__main__":
    convert_org_to_md()