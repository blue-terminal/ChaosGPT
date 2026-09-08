import pandas as pd
import os
import json

# Percorsi
DB_PATH = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/files_exploits.csv"
EXPLOITS_DIR = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/"
OUTPUT_FILE = "modello/dataset_sicurezza_training.jsonl"

def genera_dataset():
    print("\n--- GENERATORE DATASET SICUREZZA ---")
    if not os.path.exists(DB_PATH):
        print("[!] Errore: Database ExploitDB non trovato.")
        return

    print("[*] Lettura database ExploitDB...")
    try:
        df = pd.read_csv(DB_PATH)
    except Exception as e:
        print(f"Errore caricamento CSV: {e}")
        return

    # Filtriamo per piattaforme interessanti e limitiamo per il primo test
    interessi = ['linux', 'windows', 'python', 'hardware', 'webapps']
    df_filtrato = df[df['platform'].isin(interessi)].head(500)

    dataset = []
    successi = 0

    print(f"[*] Elaborazione di {len(df_filtrato)} exploit potenziali...")
    
    for idx, row in df_filtrato.iterrows():
        file_path = os.path.join(EXPLOITS_DIR, row['file'])
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    codice = f.read()
                
                # Creiamo una struttura di addestramento avanzata
                entry = {
                    "prompt": f"### Istruzione:\nAnalizza il seguente codice sorgente e identifica la vulnerabilità relativa a: {row['description']}.\n\n### Codice:\n{codice[:1500]}\n\n### Risposta:",
                    "completion": f"Il codice presenta una vulnerabilità di tipo {row['type']} sulla piattaforma {row['platform']}. Descrizione: {row['description']}. Per mitigare questo rischio, è necessario validare gli input e applicare le patch fornite dal produttore."
                }
                dataset.append(entry)
                successi += 1
            except:
                continue

    # Salvataggio
    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
    
    print(f"\n[OK] Dataset creato con successo!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Esempi generati: {successi}")
    print(f" > Dimensione file: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")

if __name__ == "__main__":
    genera_dataset()
