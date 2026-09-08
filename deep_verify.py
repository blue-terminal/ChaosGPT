from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os

# Configurazione modello esperto
llm = ChatOllama(model="llama-lexi-uncensored:latest", temperature=0)

def avvia_verifica():
    target_file = "vulnerable_rce.py"
    
    if not os.path.exists(target_file):
        print(f"Errore: {target_file} non trovato.")
        return

    print(f"[*] Lettura file: {target_file}")
    with open(target_file, "r") as f:
        codice = f.read()

    print(f"[*] Interrogazione Lexi Uncensored (Knowledge Base: ExploitDB)...")
    
    prompt = (
        f"Agisci come un esperto di sicurezza informatica. Analizza il codice seguente per trovare vulnerabilità "
        f"critiche come RCE, SQLi, o Command Injection, confrontandole con pattern noti da ExploitDB.\n\n"
        f"CODICE:\n{codice}\n\n"
        "FORNISCI:\n"
        "1. ELENCO VULNERABILITÀ\n"
        "2. ANALISI DEI RISCHI\n"
        "3. CODICE CORRETTO E SICURO\n"
    )

    try:
        risposta = llm.invoke([HumanMessage(content=prompt)]).content
        print("\n" + "="*50)
        print("RISULTATO VERIFICA SICUREZZA")
        print("="*50)
        print(risposta)
        print("="*50)
    except Exception as e:
        print(f"Errore durante l'analisi: {e}")

if __name__ == "__main__":
    avvia_verifica()
