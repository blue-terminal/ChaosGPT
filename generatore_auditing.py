import json
import os

OUTPUT_FILE = 'modello/dataset_security_auditing.jsonl'

def genera_dataset_auditing():
    print("\n--- GENERATORE DATASET AUDITING E PROTEZIONE ---")
    
    dataset = [
        # WIFI SECURITY
        {
            "istruzione": "Analizza il processo di 4-way Handshake in WPA2 per scopi di auditing.",
            "categoria": "Wireless Security",
            "dettaglio_tecnico": "Il processo scambia ANonce, SNonce e MIC per derivare le chiavi di sessione senza trasmettere la password.",
            "misura_difensiva": "L'uso di WPA3-SAE mitiga la vulnerabilità intrinseca del 4-way handshake di WPA2 contro il cracking offline."
        },
        # PASSWORD PROTECTION
        {
            "istruzione": "Spiega l'importanza del 'Salt' nell'hashing delle password.",
            "categoria": "Cryptography",
            "dettaglio_tecnico": "Un salt è un dato casuale aggiunto alla password prima dell'hashing. Questo assicura che password identiche abbiano hash diversi.",
            "misura_difensiva": "L'uso di salt unici impedisce l'uso di Rainbow Tables per il recupero delle password."
        },
        # NETWORK SCANNING DEFENSE
        {
            "istruzione": "Come configurare un firewall per rilevare e bloccare scansioni Nmap aggressive?",
            "categoria": "Network Defense",
            "dettaglio_tecnico": "Le scansioni aggressive spesso utilizzano flag TCP insoliti o frequenze di pacchetti elevate.",
            "misura_difensiva": "Implementare il Rate Limiting e usare sistemi IDS (Suricata/Snort) per identificare i pattern di scansione."
        }
    ]

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset Auditing e Protezione completato!")
    print(f" > File: {OUTPUT_FILE}")

if __name__ == "__main__":
    genera_dataset_auditing()
