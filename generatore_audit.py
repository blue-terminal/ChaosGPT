import pandas as pd
import os
import json

EXPLOITS_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/'
DB_PATH = os.path.join(EXPLOITS_DIR, 'files_exploits.csv')
OUTPUT_FILE = 'modello/dataset_audit_sicurezza.jsonl'

def genera_dataset_audit():
    print("\n--- GENERATORE DATASET AUDIT E ANALISI COSTRUZIONE ---")
    if not os.path.exists(DB_PATH):
        print("[!] Errore: Database non trovato.")
        return

    # Selezioniamo exploit con descrizioni tecniche ricche
    df = pd.read_csv(DB_PATH).head(1000)
    dataset = []

    print(f"[*] Analisi tecnica di costruzione per {len(df)} vulnerabilità...")

    for idx, row in df.iterrows():
        desc = str(row['description']).lower()
        logica = "Analisi della logica applicativa e del flusso di controllo."
        passaggi = "1. Riconoscimento versione. 2. Identificazione parametri vulnerabili. 3. Test di overflow/injection."
        
        if "metasploit" in desc:
            logica = "Modulo Metasploit: utilizza architettura standard per payload injection."
        elif "buffer overflow" in desc:
            logica = "Sfruttamento della corruzione dello stack per sovrascrivere l'indirizzo di ritorno."
            passaggi = "1. Calcolo offset esatto. 2. Identificazione indirizzo di JMP ESP. 3. Inserimento NOP Sled e Shellcode."
        elif "sql" in desc:
            logica = "Iniezione di clausole SQL per manipolare la logica della query originale."
            passaggi = "1. Chiusura stringa con apice. 2. Identificazione numero colonne con ORDER BY. 3. Estrazione dati con UNION SELECT."

        dataset.append({
            "istruzione": f"Analizza la struttura tecnica dell'exploit per: {row['description']}.",
            "input": f"Piattaforma: {row['platform']} | Tipo: {row['type']}",
            "analisi_di_costruzione": logica,
            "passaggi_di_verifica": passaggi,
            "obiettivo_difensivo": "Fornire i dettagli necessari per creare firme di rilevamento IDS/IPS e validare le patch."
        })

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset di Audit completato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Record analizzati: {len(dataset)}")

if __name__ == "__main__":
    genera_dataset_audit()
