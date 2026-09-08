import pandas as pd
import os
import json

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
DB_PATH = os.path.join(EXPLOITS_DIR, 'files_exploits.csv')
OUTPUT_FILE = 'modello/dataset_logica_exploit.jsonl'

def genera_dataset_logico():
    print("\n--- GENERATORE DATASET LOGICA E STRUTTURA EXPLOIT ---")
    if not os.path.exists(DB_PATH):
        print("[!] Errore: Database non trovato.")
        return

    df = pd.read_csv(DB_PATH).head(800) # Selezioniamo un campione significativo
    dataset = []

    print(f"[*] Analisi logica per {len(df)} vulnerabilità...")

    for idx, row in df.iterrows():
        desc = str(row['description']).lower()
        logica = "Analisi della logica applicativa per identificare punti di ingresso non validati."
        fase = "Analisi Vulnerabilità"
        
        if "buffer overflow" in desc:
            fase = "Memory Corruption"
            logica = "Sovrascrittura dei buffer di memoria per manipolare i registri di controllo (EIP/RIP)."
        elif "injection" in desc:
            fase = "Input Manipulation"
            logica = "Iniezione di comandi o query attraverso campi di input non sanitizzati."
        elif "bypass" in desc:
            fase = "Authentication Bypass"
            logica = "Aggiramento dei controlli di sicurezza tramite manipolazione di token o sessioni."
        elif "rce" in desc or "remote code execution" in desc:
            fase = "Execution Flow Hijacking"
            logica = "Esecuzione di codice arbitrario sul sistema target tramite vulnerabilità remote."

        dataset.append({
            "target": row['description'],
            "fase_attacco": fase,
            "logica_tecnica": logica,
            "piattaforma": row['platform'],
            "tipo_vulnerabilita": row['type'],
            "strategia_difensiva": "Implementare controlli di integrità, ASLR, DEP e sanitizzazione rigorosa degli input."
        })

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset logico completato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Record analizzati: {len(dataset)}")

if __name__ == "__main__":
    genera_dataset_logico()
