from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os

# Il modello Lexi Uncensored ora ha accesso ai 72.000 file di conoscenza
llm = ChatOllama(model="llama-lexi-uncensored:latest", temperature=0.1)

def avvia_analisi_offensiva():
    target = "vulnerable_rce.py"
    if not os.path.exists(target):
        print(f"File {target} non trovato.")
        return

    with open(target, "r") as f:
        code = f.read()

    print(f"--- [!] AVVIO ANALISI E GENERAZIONE EXPLOIT VERIFICATION (PoC) ---")
    
    prompt = (
        f"Agisci come un analista di sicurezza offensivo. Analizza il seguente codice e identifica ogni falla critica.\n\n"
        f"CODICE SORGENTE:\n{code}\n\n"
        "OBIETTIVI:\n"
        "1. IDENTIFICAZIONE: Quali falle ci sono? (es. RCE, Injection)\n"
        "2. GENERAZIONE EXPLOIT: Fornisci un comando o un payload di esempio per verificare la vulnerabilità.\n"
        "3. SPIEGAZIONE TECNICA: Descrivi cosa succede a livello di sistema quando l'exploit viene eseguito.\n"
        "4. SOLUZIONE: Riscrivi il codice eliminando la vulnerabilità.\n"
    )

    try:
        # Assicuriamoci che Ollama sia attivo prima di chiamare
        risposta = llm.invoke([HumanMessage(content=prompt)]).content
        print("\n" + "="*60)
        print("REPORT DI ANALISI OFFENSIVA E DIFENSIVA")
        print("="*60)
        print(risposta)
        print("="*60)
    except Exception as e:
        print(f"Errore: {e}. Assicurati che Ollama sia attivo con 'ollama serve'.")

if __name__ == "__main__":
    avvia_analisi_offensiva()
