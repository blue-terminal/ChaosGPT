import pandas as pd
import os
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Configurazione percorsi
DB_PATH = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/files_exploits.csv"
EXPLOITS_BASE_DIR = "/home/blue-terinal/Scrivania/QUARANTENA/exploitdb-main/"
MODEL = "llama-lexi-uncensored:latest"

# Avviamo Ollama se non è attivo
def avvia_ollama():
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

def cerca_e_impara(query):
    print(f"\n[*] Caricamento database ExploitDB...")
    try:
        df = pd.read_csv(DB_PATH)
    except Exception as e:
        print(f"Errore caricamento CSV: {e}")
        return

    # Ricerca nel campo description
    risultati = df[df['description'].str.contains(query, case=False, na=False)].head(1) # Ne prendiamo uno per volta per profondità
    
    if risultati.empty:
        print(f"[!] Nessun exploit trovato per la parola chiave: {query}")
        return

    llm = ChatOllama(model=MODEL, temperature=0.1)
    
    for idx, row in risultati.iterrows():
        print(f"\n[+] ANALISI EXPLOIT: {row['description']}")
        print(f"[+] ID: {row['id']} | Piattaforma: {row['platform']} | Tipo: {row['type']}")
        
        exploit_rel_path = row['file']
        # Correzione path se necessario
        exploit_file = os.path.join(EXPLOITS_BASE_DIR, exploit_rel_path)
        
        if os.path.exists(exploit_file):
            print(f"[*] Lettura file sorgente: {exploit_rel_path}")
            with open(exploit_file, 'r', errors='ignore') as f:
                code = f.read()
            
            # Limita la lunghezza del codice per il contesto dell'LLM
            code_snippet = code[:3000]
            
            query_llm = (
                f"Agisci come un esperto di cybersecurity senior e analista di vulnerabilità.\n"
                f"Stai analizzando un file reale proveniente da ExploitDB.\n\n"
                f"DESCRIZIONE: {row['description']}\n"
                f"TARGET: {row['platform']}\n"
                f"CODICE SORGENTE (estratto):\n{code_snippet}\n\n"
                "FORNISCI UN'ANALISI DETTAGLIATA:\n"
                "1. MECCANICA DELL'ATTACCO: Spiega passo dopo passo come questo codice compromette il sistema.\n"
                "2. VULNERABILITÀ: Qual è la falla nel software target (es. buffer overflow, race condition, injection)?\n"
                "3. STRATEGIA DIFENSIVA: Come deve essere riscritto il software per essere immune?\n"
                "4. RICONOSCIMENTO: Quali log o pattern di rete indicano che questo attacco è in corso?"
            )
            
            print("[*] Interrogazione Lexi Uncensored in corso...")
            try:
                risposta = llm.invoke([HumanMessage(content=query_llm)]).content
                print("\n" + "="*60)
                print("REPORT DI ANALISI SICUREZZA")
                print("="*60)
                print(risposta)
                print("="*60)
            except Exception as e:
                print(f"Errore durante l'analisi LLM: {e}")
        else:
            print(f"[!] File sorgente non trovato nel percorso: {exploit_file}")

if __name__ == "__main__":
    avvia_ollama()
    import time
    time.sleep(2)
    
    print("--- SISTEMA DI ANALISI EXPLOIT AI ---")
    user_query = input("Quale tipo di exploit vuoi analizzare oggi? (es. wordpress, ssh, rce): ")
    cerca_e_impara(user_query)
