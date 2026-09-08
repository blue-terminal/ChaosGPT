import json
import os

OUTPUT_FILE = 'modello/dataset_wifi_security_audit.jsonl'

def genera_dataset_wifi_audit():
    print("\n--- GENERATORE DATASET AUDITING WIFI E SICUREZZA PASSWORD ---")
    
    dataset = [
        # WIRELESS SECURITY AUDIT
        {
            "istruzione": "Descrivi la procedura di auditing per una rete WPA2.",
            "analisi_tecnica": "L'audit prevede il monitoraggio dei frame di gestione e l'identificazione di tentativi di riconnessione client che potrebbero esporre l'handshake.",
            "mitigazione": "Migrare a WPA3 o utilizzare Enterprise Authentication (802.1X) per isolare le sessioni degli utenti."
        },
        # PASSWORD SECURITY
        {
            "istruzione": "Analizza l'efficacia degli algoritmi di hashing contro il brute-force.",
            "analisi_tecnica": "Algoritmi come Argon2 e bcrypt sono progettati per essere 'lenti' e costosi in termini di CPU/RAM, rendendo il brute-force non praticabile.",
            "mitigazione": "Implementare il rate limiting a livello di applicazione e bloccare gli IP dopo ripetuti tentativi falliti."
        },
        # NETWORK MONITORING
        {
            "istruzione": "Come identificare un Rogue Access Point in un ambiente aziendale?",
            "analisi_tecnica": "Utilizzare scanner di rete per mappare tutti i BSSID autorizzati e allertare in caso di nuovi SSID con segnale sospetto o nomi simili.",
            "mitigazione": "Implementare il Wireless Intrusion Prevention System (WIPS)."
        }
    ]

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset WiFi Security Audit completato!")
    print(f" > File: {OUTPUT_FILE}")

if __name__ == "__main__":
    genera_dataset_wifi_audit()
