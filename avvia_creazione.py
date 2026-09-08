import pandas as pd
import os
import json
import subprocess
import time

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
OUTPUT_FILE = 'modello/dataset_sicurezza_training.jsonl'

def avvia():
    print("\n--- AVVIO GENERAZIONE DATASET (EXPLOIT + PAYLOAD) ---")
    os.makedirs('modello', exist_ok=True)
    
    # 1. Caricamento Database
    try:
        df_ex = pd.read_csv(os.path.join(EXPLOITS_DIR, 'files_exploits.csv'))
        df_sh = pd.read_csv(os.path.join(EXPLOITS_DIR, 'files_shellcodes.csv'))
        print(f"[*] Caricati {len(df_ex)} exploit e {len(df_sh)} shellcode.")
    except Exception as e:
        print(f"Errore caricamento database: {e}")
        return

    dataset = []
    
    # Processiamo un mix di entrambi
    for df, t_name in [(df_ex.head(250), 'EXPLOIT'), (df_sh.head(250), 'PAYLOAD/SHELLCODE')]:
        print(f"[*] Elaborazione {t_name}...")
        for idx, row in df.iterrows():
            f_path = os.path.join(EXPLOITS_DIR, row['file'])
            if os.path.exists(f_path):
                try:
                    with open(f_path, 'r', errors='ignore') as f:
                        code = f.read()
                    
                    dataset.append({
                        'prompt': f"### Istruzione:\nAnalizza questo {t_name}: {row['description']}\n\n### Codice:\n{code[:1500]}\n\n### Risposta:",
                        'completion': f"Questo è un {t_name.lower()} per {row['platform']}. Tipo: {row['type']}. Descrizione: {row['description']}. Difesa: Analisi euristica del codice e monitoraggio delle syscall."
                    })
                except: continue

    # Salvataggio
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
    
    print(f"\n[OK] Dataset completato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Totale campioni: {len(dataset)}")

if __name__ == "__main__":
    avvia()
