"""
educational_agent.py
--------------------
Un'architettura completa ed educativa che mostra come funziona un agente autonomo:
1. PERCEZIONE: Riceve un obiettivo e legge lo stato attuale.
2. PIANIFICAZIONE & DECISIONE: Sceglie la migliore azione disponibile per avvicinarsi al traguardo.
3. AZIONE (Tool Execution): Esegue l'azione in un ambiente controllato.
4. VALUTAZIONE & APPRENDIMENTO: Valuta l'esito, accumula esperienza nella memoria
   e adatta le scelte future (evita strategie fallimentari).
"""

import time
import math
import random
from typing import Dict, Any, List


# ==========================================
# 1. TOOLSET (Strumenti a disposizione dell'agente)
# ==========================================
class SafeToolbox:
    """Insieme di capacità pratiche che l'agente può invocare."""

    @staticmethod
    def calculate(expression: str) -> str:
        """Esegue calcoli matematici in sicurezza."""
        try:
            # Calcolo matematico limitato a funzioni sicure
            safe_dict = {"sqrt": math.sqrt, "pow": math.pow, "abs": abs}
            res = eval(expression, {"__builtins__": None}, safe_dict)
            return f"Risultato: {res}"
        except Exception as e:
            return f"Errore nel calcolo: {e}"

    @staticmethod
    def search_knowledge(topic: str) -> str:
        """Simula una base di conoscenza / archivio dati."""
        knowledge_base = {
            "python": "Python e' un linguaggio interpretato ad alto livello.",
            "cpu": "La CPU esegue le istruzioni dei programmi tramite cicli di clock.",
            "ram": "La RAM e' una memoria volatile ad alta velocita' usata per i dati attivi.",
            "opencv": "OpenCV e' una libreria open-source specializzata nella Computer Vision."
        }
        return knowledge_base.get(topic.lower(), f"Nessun dato trovato per '{topic}'.")

    @staticmethod
    def check_system_metric(metric: str) -> str:
        """Fornisce letture simulate delle metriche di efficienza."""
        if metric == "ram_usage":
            return "RAM Utilizzata: 42% (Ottimale)"
        elif metric == "cpu_load":
            return "Carico CPU: 15% (Basso)"
        return f"Metrica '{metric}' non riconosciuta."


# ==========================================
# 2. MEMORIA (Breve e Lungo Termine)
# ==========================================
class AgentMemory:
    """Gestisce la storia dei passaggi (Working Memory) e le lezioni apprese (Long-Term)."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.action_scores: Dict[str, float] = {}  # Memorizza quanto e' stata efficace un'azione

    def record_step(self, thought: str, action: str, result: str, reward: float):
        self.history.append({
            "step": len(self.history) + 1,
            "thought": thought,
            "action": action,
            "result": result,
            "reward": reward
        })
        # Aggiorna il punteggio di affidabilita' dell'azione (semplice apprendimento per rinforzo)
        current_score = self.action_scores.get(action, 1.0)
        self.action_scores[action] = current_score + (0.1 if reward > 0 else -0.3)

    def get_summary(self) -> str:
        return f"Passaggi eseguiti: {len(self.history)} | Punteggi strategie: {self.action_scores}"


# ==========================================
# 3. L'AGENTE AUTONOMO
# ==========================================
class AutonomousAgent:
    def __init__(self, name: str):
        self.name = name
        self.toolbox = SafeToolbox()
        self.memory = AgentMemory()
        self.max_steps = 5

    def perceive(self, goal: str, observation: str) -> str:
        """Fase 1: L'agente interpreta la situazione attuale."""
        print(f"\n[{self.name} - PERCEZIONE] Obiettivo: '{goal}'")
        if observation:
            print(f"[{self.name} - OSSERVAZIONE] Ultimo risultato: {observation}")
        return observation

    def plan_and_decide(self, goal: str, last_result: str) -> tuple[str, str, Any]:
        """
        Fase 2: Ragionamento e Selezione dell'Azione.
        Analizza l'obiettivo e decide quale tool chiamare.
        """
        goal_lower = goal.lower()

        # Esempio di logica euristica di pianificazione:
        if "calcola" in goal_lower or "matematica" in goal_lower:
            thought = "L'utente richiede un calcolo matematico. Uso il tool 'calculate'."
            action = "calculate"
            # Estrae o sceglie un'operazione d'esempio
            arg = "sqrt(144) + 10"
        elif "informazioni su" in goal_lower or "cos'e" in goal_lower:
            thought = "L'utente cerca una definizione. Cerco nella knowledge base."
            action = "search_knowledge"
            # Identifica argomento
            topic = "opencv" if "opencv" in goal_lower else "python"
            arg = topic
        elif "metriche" in goal_lower or "risorse" in goal_lower:
            thought = "Richiesta verifica efficienza sistema. Controllo metriche."
            action = "check_system_metric"
            arg = "ram_usage"
        else:
            thought = "Obiettivo generico: eseguo una diagnostica preliminare."
            action = "check_system_metric"
            arg = "cpu_load"

        print(f"[{self.name} - PENSIERO] {thought}")
        print(f"[{self.name} - DECISIONE] Scelta azione: '{action}' con parametri: {arg}")
        return thought, action, arg

    def execute_action(self, action: str, arg: Any) -> str:
        """Fase 3: Esecuzione concreta dell'azione attraverso il tool corrispondente."""
        print(f"[{self.name} - AZIONE] Invocazione in corso...")
        if action == "calculate":
            return self.toolbox.calculate(arg)
        elif action == "search_knowledge":
            return self.toolbox.search_knowledge(arg)
        elif action == "check_system_metric":
            return self.toolbox.check_system_metric(arg)
        else:
            return f"Azione '{action}' non valida."

    def evaluate_and_learn(self, goal: str, result: str) -> tuple[bool, float]:
        """
        Fase 4: Feedback ed Apprendimento.
        Verifica se l'output soddisfa l'obiettivo o se serve un altro passo.
        """
        is_success = "Errore" not in result and "non trovata" not in result
        reward = 1.0 if is_success else -1.0

        if is_success:
            print(f"[{self.name} - APPRENDIMENTO] Passo completato con successo (+{reward} reward).")
        else:
            print(f"[{self.name} - APPRENDIMENTO] L'azione ha prodotto un errore ({reward} reward). Strategia da ricalibrare.")

        return is_success, reward

    def run_task(self, goal: str):
        """Ciclo di vita principale dell'agente (Autonomous Agent Loop)."""
        print(f"\n{'='*55}\nAVVIO TASK AUTONOMO: '{goal}'\n{'='*55}")
        last_result = ""

        for step in range(1, self.max_steps + 1):
            print(f"\n--- [PASSO {step}/{self.max_steps}] ---")
            
            # 1. Percezione
            self.perceive(goal, last_result)

            # 2. Decisione
            thought, action, arg = self.plan_and_decide(goal, last_result)

            # 3. Azione
            result = self.execute_action(action, arg)
            print(f"[{self.name} - RISULTATO] {result}")

            # 4. Apprendimento e aggiornamento stato
            is_success, reward = self.evaluate_and_learn(goal, result)
            self.memory.record_step(thought, action, str(result), reward)

            # Controllo se l'obiettivo e' concluso
            if is_success:
                print(f"\n[+] Obiettivo raggiunto al passo {step}!")
                break
            
            last_result = result
            time.sleep(0.5)

        print("\n" + "="*55)
        print("STATO FINALE DELLA MEMORIA DELL'AGENTE:")
        print(self.memory.get_summary())
        print("="*55)


# ==========================================
# ESEMPIO DI UTILIZZO
# ==========================================
if __name__ == "__main__":
    agent = AutonomousAgent(name="Nexus-1")

    # Esempio 1: Task di calcolo matematico
    agent.run_task(goal="Calcola la radice quadrata di 144 piu 10")

    # Esempio 2: Task di recupero conoscenza
    agent.run_task(goal="Trova informazioni su OpenCV")

    # Esempio 3: Task di controllo risorse
    agent.run_task(goal="Controlla le metriche di efficienza e risorse")
