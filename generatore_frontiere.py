import json
import os

OUTPUT_FILE = 'modello/dataset_global_frontiers.jsonl'

def genera_dataset_frontiere():
    print("\n--- GENERATORE DATASET GLOBAL FRONTIERS (OSINT, Cloud, IoT, Forensics) ---")
    
    dataset = [
        # OSINT
        {
            "istruzione": "Spiega come utilizzare Google Dorking per trovare database esposti.",
            "dominio": "OSINT",
            "tecnica": "Uso di operatori come 'filetype:sql' o 'intitle:index of' associati a termini sensibili come 'config' o 'backup'.",
            "difesa": "Configurare correttamente il file robots.txt e disabilitare l'indicizzazione dei file sensibili."
        },
        # CLOUD SECURITY
        {
            "istruzione": "Quali sono i rischi principali in un ambiente Kubernetes mal configurato?",
            "dominio": "Cloud Security",
            "tecnica": "Accesso non autorizzato all'API server, privilege escalation tra pod e segreti (secrets) non criptati.",
            "difesa": "Implementare RBAC (Role-Based Access Control) rigoroso e network policies per isolare i pod."
        },
        # IOT SECURITY
        {
            "istruzione": "Come si esegue il dumping del firmware di un dispositivo IoT?",
            "dominio": "IoT Security",
            "tecnica": "Connessione fisica tramite porta UART/JTAG e uso di strumenti come Flashrom o BusPirate per estrarre il contenuto della memoria flash.",
            "difesa": "Disabilitare le porte di debug in produzione e cifrare il firmware a riposo."
        },
        # MALWARE ANALYSIS
        {
            "istruzione": "Descrivi una tecnica comune di Anti-Debugging usata dai malware.",
            "dominio": "Malware Analysis",
            "tecnica": "Uso della funzione 'IsDebuggerPresent()' in Windows per rilevare la presenza di un debugger come x64dbg o OllyDbg.",
            "difesa": "Usare plugin di mascheramento nel debugger o analizzare il malware in una sandbox isolata."
        },
        # FORENSICS
        {
            "istruzione": "Cos'è l'analisi della memoria RAM (Memory Forensics)?",
            "dominio": "Forensics",
            "tecnica": "Acquisizione di un dump della memoria fisica e analisi con tool come Volatility per trovare processi nascosti o connessioni di rete attive.",
            "difesa": "Mantenere log dettagliati e utilizzare soluzioni EDR (Endpoint Detection and Response)."
        }
    ]

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset Global Frontiers completato!")
    print(f" > File: {OUTPUT_FILE}")

if __name__ == "__main__":
    genera_dataset_frontiere()
