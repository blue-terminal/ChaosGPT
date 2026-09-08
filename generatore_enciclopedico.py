import pandas as pd
import os
import json

DB_PATH = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/files_exploits.csv"
EXPLOITS_DIR = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/"
OUTPUT_FILE = "modello/dataset_enciclopedico_sicurezza.jsonl"

def genera_enciclopedia():
    print("\n--- GENERATORE ENCICLOPEDICO DI SICUREZZA ---")
    if not os.path.exists(DB_PATH):
        print("[!] Database non trovato.")
        return

    print("[*] Caricamento di oltre 47.000 exploit...")
    df = pd.read_csv(DB_PATH)
    
    dataset = []
    totale = len(df)
    print(f"[*] Inizio elaborazione di {totale} record...")

    for idx, row in df.iterrows():
        # Creiamo una struttura ricca per ogni exploit
        tipologia = str(row['type']).upper()
        piattaforma = str(row['platform']).upper()
        descrizione = str(row['description'])
        
        # Analisi della struttura (dedotta dai tag e descrizione)
        struttura = f"Exploit di tipo {tipologia} per piattaforma {piattaforma}. "
        if "Buffer Overflow" in descrizione:
            struttura += "Struttura basata sulla corruzione della memoria (stack/heap)."
        elif "Injection" in descrizione or "SQL" in descrizione:
            struttura += "Struttura basata sulla manipolazione degli input (escaped characters)."
        elif "RCE" in descrizione or "Remote" in descrizione:
            struttura += "Struttura finalizzata all'esecuzione di codice arbitrario remoto."
        else:
            struttura += "Struttura specifica basata sulla logica dell'applicazione target."

        entry = {
            "tipologia": tipologia,
            "piattaforma": piattaforma,
            "descrizione": descrizione,
            "struttura_tecnica": struttura,
            "cve": str(row['codes']) if pd.notna(row['codes']) else "N/A",
            "percorso_sorgente": row['file']
        }
        dataset.append(entry)

        if idx % 5000 == 0:
            print(f" > Elaborati {idx}/{totale}...")

    # Salvataggio in JSONL
    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
    
    print(f"\n[OK] ENCICLOPEDIA COMPLETATA!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Record totali: {len(dataset)}")

if __name__ == "__main__":
    genera_enciclopedia()
