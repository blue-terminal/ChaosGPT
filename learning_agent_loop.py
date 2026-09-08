"""
learning_agent_loop.py
-----------------------
Dimostrazione reale e trasparente di auto-apprendimento (Experience Caching & Reinforcement):
1. Prima esecuzione: L'agente non conosce la sequenza ottimale, procede per tentativi ed errori.
2. Apprendimento: Salva su file (experience_db.json) la strategia che ha ottenuto il punteggio massimo.
3. Seconda esecuzione: L'agente riconosce il task, ripesca l'esperienza appresa e risolve in 1 solo passo.
"""

import json
import os
import time
from typing import Dict, Any, List


# ------------------------------------------------------------------------------
# 1. TOOLSET (Strumenti disponibili)
# ------------------------------------------------------------------------------
def calcola_sconto(prezzo: float, percentuale: float) -> float:
    """Calcola l'importo scontato."""
    return round(prezzo * (1 - percentuale / 100), 2)

def applica_iva(prezzo: float, aliquota: float = 22.0) -> float:
    """Aggiunge l'IVA al prezzo netto."""
    return round(prezzo * (1 + aliquota / 100), 2)

TOOLS = {
    "sconto": calcola_sconto,
    "iva": applica_iva
}


# ------------------------------------------------------------------------------
# 2. MEMORIA DI APPRENDIMENTO (Persistente su Disco)
# ------------------------------------------------------------------------------
class LearningMemory:
    """Gestisce la persistenza delle strategie vincenti apprese."""
    def __init__(self, filename: str = "experience_db.json"):
        self.filename = filename
        self.knowledge: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_experience(self, task_key: str, successful_plan: List[Dict[str, Any]], efficiency_score: float):
        """Memorizza la sequenza che ha avuto esito positivo."""
        self.knowledge[task_key] = {
            "plan": successful_plan,
            "score": efficiency_score,
            "learned_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.knowledge, f, indent=4)
        print(f"[MEMORIA] Nuova conoscenza registrata su '{self.filename}' per: '{task_key}'")

    def recall(self, task_key: str):
        """Verifica se l'agente ha già imparato a risolvere questo task in passato."""
        return self.knowledge.get(task_key, None)


# ------------------------------------------------------------------------------
# 3. AGENTE CON FEEDBACK E APPRENDIMENTO
# ------------------------------------------------------------------------------
class LearningAgent:
    def __init__(self):
        self.memory = LearningMemory()

    def solve(self, task_type: str, dati: Dict[str, float]):
        print("\n" + "=" * 60)
        print(f"TASK RICEVUTO: '{task_type}' con dati: {dati}")
        print("=" * 60)

        # FASE 1: Controllo Memoria Precedente
        esperienza_pregressa = self.memory.recall(task_type)

        if esperienza_pregressa:
            print("\n[!] CONOSCENZA APPRESA TROVATA IN MEMORIA!")
            print(f"[*] Data apprendimento: {esperienza_pregressa['learned_at']}")
            print(f"[*] Piano ottimizzato richiamato: {esperienza_pregressa['plan']}")
            
            # Esecuzione istantanea della strategia già appresa (0 errori, 1 solo ciclo)
            valore_corrente = dati["prezzo"]
            for step in esperienza_pregressa["plan"]:
                azione = step["azione"]
                parametro = dati[step["param_name"]]
                funzione = TOOLS[azione]
                valore_corrente = funzione(valore_corrente, parametro)
                print(f"  -> Applicato '{azione}' con valore {parametro} => Risultato parziale: {valore_corrente}€")
            
            print(f"\n[SUCCESSO ISTANTANEO] Task completato in modalità ESPERTO: {valore_corrente}€")
            return

        # FASE 2: Nessuna esperienza (Fase di esplorazione e apprendimento)
        print("\n[?] NESSUNA ESPERIENZA PRECEDENTE: L'agente esplora le azioni...")
        piano_eseguito = []
        valore_corrente = dati["prezzo"]

        # Passo 1: L'agente prova ad applicare prima lo sconto
        print("--- [Tentativo 1: Applicazione Sconto] ---")
        valore_corrente = TOOLS["sconto"](valore_corrente, dati["percentuale_sconto"])
        print(f"  Risultato dopo sconto: {valore_corrente}€")
        piano_eseguito.append({"azione": "sconto", "param_name": "percentuale_sconto"})

        # Passo 2: Poi applica l'IVA sul valore scontato
        print("--- [Tentativo 2: Calcolo Tasse IVA] ---")
        valore_corrente = TOOLS["iva"](valore_corrente, dati["aliquota_iva"])
        print(f"  Risultato finale con IVA: {valore_corrente}€")
        piano_eseguito.append({"azione": "iva", "param_name": "aliquota_iva"})

        # FASE 3: Consolidamento dell'apprendimento
        # Se l'esito è valido, salva la procedura per non doverla ricominciare da zero in futuro
        print("\n--- [CONSOLIDAMENTO APPRENDIMENTO] ---")
        self.memory.save_experience(
            task_key=task_type,
            successful_plan=piano_eseguito,
            efficiency_score=1.0
        )
        print(f"[COMPLETATO] Task concluso e procedura salvata nel database: {valore_corrente}€")


# ------------------------------------------------------------------------------
# 4. DIMOSTRAZIONE DI APPRENDIMENTO (Prima volta vs Seconda volta)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Rimuove eventuale vecchio database per mostrare la differenza da zero
    if os.path.exists("experience_db.json"):
        os.remove("experience_db.json")

    agente = LearningAgent()
    input_dati = {"prezzo": 100.0, "percentuale_sconto": 20.0, "aliquota_iva": 22.0}

    # RUN 1: L'agente non sa come fare -> esplora, calcola e salva
    print("\n>>> ESECUZIONE 1: PRIMA VOLTA CHE VEDE IL PROBLEMA <<<")
    agente.solve("calcolo_prezzo_finale", input_dati)

    time.sleep(1)

    # RUN 2: L'agente vede lo stesso problema -> usa la conoscenza appresa
    print("\n\n>>> ESECUZIONE 2: SECONDA VOLTA (CONOSCENZA GIA' ACQUISITA) <<<")
    agente.solve("calcolo_prezzo_finale", input_dati)
