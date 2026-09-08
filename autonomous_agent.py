"""
autonomous_agent.py
-------------------
Agente Autonomo orientato a obiettivi con ciclo OODA (Osserva, Orienta, Decidi, Agisci).
L'agente:
1. Riceve o seleziona un obiettivo.
2. Scompone il problema e pianifica i passi da eseguire.
3. Esegue in autonomia i passi adoperando gli strumenti disponibili nel suo toolbox sicuro.
4. Valuta l'esito di ogni azione e aggiorna la propria memoria persistente.
5. Si ferma automaticamente al raggiungimento del traguardo o al limite massimo di passi.
"""

import sys
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Garantisce la compatibilità con la console Windows
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from test_ollama_client import query_ollama
    HAS_OLLAMA = True
except Exception:
    HAS_OLLAMA = False

from unified_system import UnifiedSystem


class AutonomousAgent:
    def __init__(self, name: str = "Nexus-1", max_steps: int = 5):
        self.name = name
        self.max_steps = max_steps
        self.system = UnifiedSystem()
        self.memory_file = "agent_autonomous_memory.json"
        self.history: List[Dict[str, Any]] = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except Exception:
                self.memory = {"missions_completed": 0, "log": []}
        else:
            self.memory = {"missions_completed": 0, "log": []}

    def _save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def log(self, stage: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{self.name}] [{stage:<10}] {message}")

    def plan_mission(self, objective: str) -> List[Dict[str, Any]]:
        self.log("PIANIFICA", f"Scomposizione obiettivo: '{objective}'")
        time.sleep(0.5)

        plan = [
            {
                "step": 1,
                "action": "vision",
                "desc": "Acquisizione e analisi visiva dell'ambiente di lavoro (avatar.png)",
                "params": {"image": "avatar.png"}
            },
            {
                "step": 2,
                "action": "text",
                "desc": "Estrazione semantica e calcolo parametri dal testo dell'obiettivo",
                "params": {"text": objective}
            },
            {
                "step": 3,
                "action": "strategic_pricing",
                "desc": "Verifica strategia di calcolo e allocazione risorse tramite memoria storica",
                "params": {"prezzo": 150.0, "sconto": 10.0, "iva": 22.0}
            },
            {
                "step": 4,
                "action": "online_learning",
                "desc": "Aggiornamento incrementale dei pesi del modello decisionale",
                "params": {"features": [2.0, 1.0], "target": 1}
            }
        ]

        if HAS_OLLAMA:
            plan.append({
                "step": 5,
                "action": "llm_reflection",
                "desc": "Sintesi strategica tramite modello locale Ollama (qwen2.5:0.5b)",
                "params": {"prompt": f"Riassumi in una frase l'esito delle operazioni per l'obiettivo: {objective}"}
            })

        return plan

    def execute_action(self, task: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if task == "llm_reflection":
            prompt = params.get("prompt", "")
            self.log("AZIONE", "Interrogazione modello locale Ollama...")
            reply = query_ollama(prompt)
            return {"status": "SUCCESS", "reflection": reply.strip()}
        else:
            return self.system.dispatch(task, params)

    def run_autonomous_loop(self, objective: str):
        print("\n" + "=" * 65)
        print(f"[AGENTE] AVVIO CICLO AUTONOMO: {self.name}")
        print(f"[OBIETTIVO] {objective}")
        print("=" * 65 + "\n")

        plan = self.plan_mission(objective)
        self.log("PIANO", f"Generato piano operativo con {len(plan)} fasi sequenziali.")
        time.sleep(0.5)

        step_count = 0
        for item in plan:
            step_count += 1
            if step_count > self.max_steps:
                self.log("SAFETY", "Raggiunto limite massimo di passi consentiti (max_steps).")
                break

            self.log("STEP", f"[{item['step']}/{len(plan)}] Esecuzione: {item['desc']}")

            start_time = time.time()
            result = self.execute_action(item["action"], item["params"])
            elapsed = time.time() - start_time

            status = result.get("status", "UNKNOWN")
            if status == "SUCCESS":
                self.log("FEEDBACK", f"Completato con successo in {elapsed:.2f}s.")
            else:
                self.log("ATTENZIONE", f"Esito non ottimale: {result}")

            self.history.append({
                "step": item["step"],
                "action": item["action"],
                "status": status,
                "time": elapsed
            })
            time.sleep(0.5)

        self.memory["missions_completed"] += 1
        self.memory["log"].append({
            "timestamp": datetime.now().isoformat(),
            "objective": objective,
            "steps_executed": len(self.history),
            "status": "COMPLETED"
        })
        self._save_memory()

        print("\n" + "=" * 65)
        self.log("CONCLUSIONE", f"Tutte le azioni sono state eseguite in autonomia.")
        self.log("MEMORIA", f"Dati salvati in '{self.memory_file}'. Missioni totali: {self.memory['missions_completed']}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    agent = AutonomousAgent(name="Nexus-AutoBot", max_steps=5)
    missione = "Ispeziona l'ambiente visivo, analizza i parametri testuali e aggiorna i pesi del modello"
    agent.run_autonomous_loop(missione)
