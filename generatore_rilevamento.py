import pandas as pd
import os
import json

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
DB_PATH = os.path.join(EXPLOITS_DIR, 'files_exploits.csv')
OUTPUT_FILE = 'modello/dataset_rilevamento_exploit.jsonl'

def genera_dataset_riconoscimento():
    print("\n--- GENERATORE DATASET DI RICONOSCIMENTO EXPLOIT ---")
    if not os.path.exists(DB_PATH):
        print("[!] Errore: Database non trovato.")
        return

    df = pd.read_csv(DB_PATH).head(1000) # Prendiamo i primi 1000 per questo dataset di test
    dataset = []

    print(f"[*] Creazione di coppie RILEVAMENTO per {len(df)} file...")

    for idx, row in df.iterrows():
        f_path = os.path.join(EXPLOITS_DIR, row['file'])
        if os.path.exists(f_path):
            try:
                with open(f_path, 'r', errors='ignore') as f:
                    codice = f.read()[:1500]
                
                # Voce POSITIVA (L'exploit)
                dataset.append({
                    "instruction": "Analizza questo codice e determina se contiene un exploit o una vulnerabilità.",
                    "input": codice,
                    "output": f"RISULTATO: [EXPLOIT RILEVATO]\nMOTIVAZIONE: Il codice corrisponde alla vulnerabilità '{row['description']}' per {row['platform']}. Si tratta di un attacco di tipo {row['type']}."
                })
                
                # Voce NEGATIVA (Codice Sicuro - Simulazione)
                # Creiamo una versione "finta sicura" per insegnare la differenza
                dataset.append({
                    "instruction": "Analizza questo codice e determina se contiene un exploit o una vulnerabilità.",
                    "input": f"# Codice di esempio sicuro\ndef funzione_sicura(data):\n    # Validazione input eseguita correttamente\n    print(f'Dati elaborati: {data}')\n",
                    "output": "RISULTATO: [SICURO]\nMOTIVAZIONE: Il codice non presenta pattern di attacco noti, esegue operazioni standard e gestisce i dati in modo isolato."
                })
            except:
                continue

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset di riconoscimento creato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Totale esempi (Exploit + Sicuri): {len(dataset)}")

if __name__ == "__main__":
    genera_dataset_riconoscimento()
