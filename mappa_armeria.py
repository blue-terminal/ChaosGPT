import os
import json

ROOT_DIR = '/home/blue-terinal/Scrivania/QUARANTENA/'
OUT_FILE = 'modello/dataset_manuale_tools.jsonl'

def mappa_armeria_completa():
    print("\n--- MAPPATURA TOTALE ARMERIA TOOLS ---")
    
    tools_config = {
        "beef-master": "Browser Exploitation Framework. Gestione di hook e attacchi client-side.",
        "mimikatz-master": "Post-Exploitation. Estrazione di password e ticket Kerberos dalla memoria.",
        "hashcat-master": "Advanced Password Recovery. Cracking di hash tramite GPU/CPU con regole avanzate.",
        "sqlmap-master": "Automatic SQL Injection. Identificazione ed estrazione automatizzata di database.",
        "nmap-master": "Network Mapper. Scansione porte, OS detection e scripting engine (NSE).",
        "Villain": "Windows/Linux Backdoor & C2. Gestione di sessioni remote e bypass di firewall.",
        "Starkiller-main": "Interfaccia GUI per Empire (C2). Gestione di agenti e moduli di post-exploitation.",
        "wireshark-master": "Network Protocol Analyzer. Analisi profonda dei pacchetti e troubleshooting.",
        "GhidrAssist": "Integrazione AI per Ghidra. Assistenza nel Reverse Engineering di file binari."
    }

    dataset = []
    
    for tool, desc in tools_config.items():
        t_path = os.path.join(ROOT_DIR, tool)
        status = "[TROVATO]" if os.path.exists(t_path) else "[MANCANTE]"
        print(f"[*] Tool: {tool:<20} {status}")
        
        if os.path.exists(t_path):
            dataset.append({
                "istruzione": f"Come si utilizza il tool {tool} e qual è la sua funzione principale?",
                "tool_nome": tool,
                "percorso": t_path,
                "funzione_tecnica": desc,
                "workflow_operativo": f"1. Entra in {t_path}. 2. Consulta il file README per le dipendenze. 3. Esegui lo script principale per avviare l'analisi."
            })

    os.makedirs("modello", exist_ok=True)
    with open(OUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Mappatura Tools completata! File: {OUT_FILE}")

if __name__ == "__main__":
    mappa_armeria_completa()
