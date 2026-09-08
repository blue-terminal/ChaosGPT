import pandas as pd
import os
import json

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
OUT_DIR = 'modello/'

def genera_multi_dataset():
    print("\n--- GENERATORE MULTI-DATASET CATEGORIZZATO ---")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    try:
        df_ex = pd.read_csv(os.path.join(EXPLOITS_DIR, 'files_exploits.csv'))
        df_sh = pd.read_csv(os.path.join(EXPLOITS_DIR, 'files_shellcodes.csv'))
    except Exception as e:
        print(f"Errore: {e}")
        return

    # 1. Gestione Shellcodes (Categoria unica)
    print("[*] Generazione dataset SHELLCODES...")
    salva_categoria(df_sh, "shellcodes", "PAYLOAD/SHELLCODE")

    # 2. Gestione Exploit per Tipo (dos, remote, local, webapps, etc)
    categorie = df_ex['type'].unique()
    for cat in categorie:
        print(f"[*] Generazione dataset categoria: {cat.upper()}...")
        sub_df = df_ex[df_ex['type'] == cat].head(500) # 500 campioni per categoria per iniziare
        salva_categoria(sub_df, cat, "EXPLOIT")

    # 3. Specializzazione Python (Molto importante per te)
    print("[*] Generazione dataset specializzato PYTHON...")
    py_df = df_ex[df_ex['file'].str.endswith('.py', na=False)].head(500)
    salva_categoria(py_df, "python_exploits", "PYTHON EXPLOIT")

def salva_categoria(df, nome_cat, label):
    dataset = []
    output_path = os.path.join(OUT_DIR, f"dataset_{nome_cat}.jsonl")
    
    for idx, row in df.iterrows():
        f_path = os.path.join(EXPLOITS_DIR, row['file'])
        if os.path.exists(f_path):
            try:
                with open(f_path, 'r', errors='ignore') as f:
                    code = f.read()
                
                dataset.append({
                    'prompt': f"### Istruzione:\nAnalizza questo {label} ({nome_cat}): {row['description']}\n\n### Codice:\n{code[:1500]}\n\n### Risposta:",
                    'completion': f"Vulnerabilità: {row['description']}. Piattaforma: {row['platform']}. Questo codice è un esempio di {label.lower()}. Protezione: Patching dei sistemi e sanitizzazione degli input."
                })
            except: continue

    with open(output_path, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
    print(f" [OK] Creato {output_path} ({len(dataset)} campioni)")

if __name__ == "__main__":
    genera_multi_dataset()
