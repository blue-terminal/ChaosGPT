"""
agentic_loop.py
----------------
Esempio didattico e robusto di un loop agentico (ReAct pattern) in Python.
Dimostra come funziona il ciclo:
  Obiettivo -> Pensiero -> Scelta Strumento -> Esecuzione -> Osservazione -> Risposta Finale
"""

import json
import time
from typing import Dict, Any, Callable


# ==============================================================================
# 1. DEFINIZIONE DEI TOOL (Funzioni concrete e delimitate)
# ==============================================================================
def tool_somma(a: float, b: float) -> str:
    """Somma due numeri."""
    return str(a + b)

def tool_moltiplica(a: float, b: float) -> str:
    """Moltiplica due numeri."""
    return str(a * b)

def tool_lunghezza_testo(testo: str) -> str:
    """Conta il numero di caratteri in una stringa."""
    return str(len(testo))

# Registro delle funzioni autorizzate (Whitelist rigorosa)
REGISTRO_TOOL: Dict[str, Callable] = {
    "somma": tool_somma,
    "moltiplica": tool_moltiplica,
    "lunghezza_testo": tool_lunghezza_testo
}


# ==============================================================================
# 2. SIMULATORE DI RAGIONAMENTO (O Interfaccia per LLM locale)
# ==============================================================================
class ReasoningEngine:
    """
    Simula il componente che produce la decisione strutturata in JSON.
    In produzione, qui risiede la chiamata all'API dell'LLM (es. Ollama).
    """
    def __init__(self):
        self.step_count = 0

    def think(self, goal: str, context: list) -> Dict[str, Any]:
        """
        Ritorna un dizionario JSON con lo standard:
        - "pensiero": spiegazione del ragionamento
        - "azione": nome del tool da chiamare (oppure 'final_answer')
        - "parametri": argomenti per il tool
        - "risposta_finale": presente solo se il task è completato
        """
        self.step_count += 1

        # Esempio di flusso multi-step per il task: "Calcola (15 + 25) e poi moltiplica per 2"
        if "15" in goal and "25" in goal:
            if self.step_count == 1:
                return {
                    "pensiero": "Per prima cosa devo calcolare la somma tra 15 e 25.",
                    "azione": "somma",
                    "parametri": {"a": 15, "b": 25}
                }
            elif self.step_count == 2:
                # Recupera l'ultimo risultato osservato (40.0)
                ultimo_risultato = float(context[-1]["osservazione"])
                return {
                    "pensiero": f"Ho ottenuto {ultimo_risultato}. Ora moltiplico questo valore per 2.",
                    "azione": "moltiplica",
                    "parametri": {"a": ultimo_risultato, "b": 2}
                }
            else:
                ultimo_risultato = context[-1]["osservazione"]
                return {
                    "pensiero": "Tutti i calcoli sono stati completati.",
                    "azione": "final_answer",
                    "risposta_finale": f"Il risultato finale del calcolo è {ultimo_risultato}."
                }

        # Fallback generico
        return {
            "pensiero": "Task non riconosciuto o già completato.",
            "azione": "final_answer",
            "risposta_finale": "Operazione conclusa."
        }


# ==============================================================================
# 3. IL LOOP AGENTICO (Il ciclo di controllo e sicurezza)
# ==============================================================================
class AgenticLoop:
    def __init__(self, max_steps: int = 5):
        self.max_steps = max_steps
        self.brain = ReasoningEngine()
        self.history = []

    def execute_tool(self, action_name: str, params: Dict[str, Any]) -> str:
        """Esegue lo strumento garantendo che esista nella whitelist e catturando eccezioni."""
        if action_name not in REGISTRO_TOOL:
            return f"Errore: Lo strumento '{action_name}' non esiste o non è autorizzato."
        
        try:
            tool_func = REGISTRO_TOOL[action_name]
            risultato = tool_func(**params)
            return risultato
        except Exception as e:
            return f"Errore durante l'esecuzione del tool: {e}"

    def run(self, goal: str):
        print("=" * 60)
        print(f"AVVIO LOOP AGENTICO")
        print(f"Obiettivo: {goal}")
        print(f"Limite di sicurezza: Max {self.max_steps} iterazioni")
        print("=" * 60)

        for step in range(1, self.max_steps + 1):
            print(f"\n--- [ITERAZIONE {step}/{self.max_steps}] ---")

            # 1. Fase di Ragionamento (Think)
            decision = self.brain.think(goal, self.history)
            pensiero = decision.get("pensiero", "")
            azione = decision.get("azione", "")
            parametri = decision.get("parametri", {})

            print(f"[PENSIERO]     {pensiero}")
            print(f"[DECISIONE]    Azione: '{azione}' | Parametri: {parametri}")

            # 2. Condizione di Stop: Risposta Finale raggiunta
            if azione == "final_answer":
                risposta = decision.get("risposta_finale", "Nessuna risposta.")
                print(f"\n[RISULTATO FINALE] => {risposta}")
                print(f"[STATUS] Loop terminato con successo al passo {step}.")
                return

            # 3. Fase di Azione: Esecuzione del Tool
            osservazione = self.execute_tool(azione, parametri)
            print(f"[OSSERVAZIONE] Risultato tool: {osservazione}")

            # 4. Aggiornamento dello Stato (Memoria del ciclo)
            self.history.append({
                "step": step,
                "pensiero": pensiero,
                "azione": azione,
                "parametri": parametri,
                "osservazione": osservazione
            })

            time.sleep(0.3)  # Piccola pausa per simulare il ciclo di clock

        print(f"\n[WARNING] Raggiunto il limite massimo di passi ({self.max_steps}) senza concludere il task.")


# ==============================================================================
# 4. TEST DI ESECUZIONE
# ==============================================================================
if __name__ == "__main__":
    loop = AgenticLoop(max_steps=5)
    
    # Task multi-step: richiede 2 chiamate consecutive a tool diversi
    task = "Calcola (15 + 25) e poi moltiplica per 2"
    loop.run(task)
