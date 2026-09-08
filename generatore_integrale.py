import pandas as pd
import os
import json

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
DB_PATH = os.path.join(EXPLOITS_DIR, 'files_exploits.csv')
OUTPUT_FILE = 'modello/dataset_sorgenti_integrali.jsonl'

def genera_dataset_integrale():
    print("\n--- GENERATORE DATASET SORGENTI INTEGRALI ---")
    if not os.path.exists(DB_PATH):
        print("[!] Errore: Database non trovato.")
        return

    # Prendiamo un campione di 2000 exploit significativi
    df = pd.read_csv(DB_PATH).head(2000)
    dataset = []

    print(f"[*] Estrazione sorgenti completi per {len(df)} file...")

    for idx, row in df.iterrows():
        f_path = os.path.join(EXPLOITS_DIR, row['file'])
        if os.path.exists(f_path):
            try:
                # Leggiamo TUTTO il file (senza limiti di caratteri brevi)
                with open(f_path, 'r', errors='ignore') as f:
                    codice_integrale = f.read()
                
                if len(codice_integrale) > 50:
                    dataset.append({
                        "instruction": f"Fornisci il codice sorgente integrale per l'exploit: {row['description']}",
                        "input": f"Piattaforma: {row['platform']} | Tipo: {row['type']}",
                        "output": codice_integrale
                    })
            except:
                continue

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset SORGENTI INTEGRALI completato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Exploit completi salvati: {len(dataset)}")

if __name__ == "__main__":
    genera_dataset_integrale()
