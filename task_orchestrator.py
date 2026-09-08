"""
task_orchestrator.py
--------------------
Orchestratore Modulare di Task.
Dimostra come integrare sottosistemi indipendenti e sicuri:
1. Vision Pipeline (OpenCV)
2. Data & Text Processor (Regex e Statistiche)
3. Experience Memory (Persistenza e Apprendimento)

Ogni modulo opera come un servizio isolato con interfaccia standard.
"""

import time
import json
from pathlib import Path
from typing import Dict, Any

# Importazione dei moduli sicuri sviluppati
from computer_vision import OpenCVVisionPipeline
from data_processor import TextProcessor
from learning_agent_loop import LearningAgent, LearningMemory
from online_learner import OnlineLearningModel


class UnifiedTaskOrchestrator:
    def __init__(self):
        print("[*] Inizializzazione Orchestratore Modulare...")
        self.vision_service = OpenCVVisionPipeline(output_dir="outputs/vision")
        self.memory_service = LearningMemory(filename="experience_db.json")
        self.learning_agent = LearningAgent()
        self.online_model = OnlineLearningModel(num_features=2, learning_rate=0.2)
        print("[+] Tutti i moduli di servizio sono operativi e isolati.\n")

    def dispatch(self, task_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Smista l'esecuzione verso il modulo specialistico corretto,
        tracciando tempo di esecuzione e gestendo eventuali eccezioni.
        """
        start_time = time.time()
        print("=" * 60)
        print(f"[ORCHESTRATORE] Ricevuto Task: '{task_name}'")
        print("=" * 60)

        result = {}
        try:
            if task_name == "vision_analysis":
                # Richiama la pipeline di Computer Vision
                image_path = payload.get("image_path", "avatar.png")
                print(f"[*] Delegato a VisionService per l'immagine: {image_path}")
                vision_res = self.vision_service.run_full_pipeline(image_path)
                result = {
                    "status": "SUCCESS",
                    "contours_found": vision_res["contours_count"],
                    "generated_files": vision_res["files"]
                }

            elif task_name == "text_processing":
                # Richiama l'analizzatore di dati e testo
                text_input = payload.get("text", "")
                print(f"[*] Delegato a TextProcessor ({len(text_input)} caratteri)")
                processor = TextProcessor(text_input)
                stats = processor.calculate_stats()
                keywords = processor.get_top_keywords(3)
                result = {
                    "status": "SUCCESS",
                    "total_words": stats["total_words"],
                    "avg_word_length": stats["avg_word_length"],
                    "top_keywords": [k[0] for k in keywords]
                }

            elif task_name == "pricing_calculation":
                # Richiama il modulo con esperienza e apprendimento
                print("[*] Delegato a LearningAgent con riuso di memoria pregressa")
                self.learning_agent.solve(
                    task_type="calcolo_prezzo_finale",
                    dati=payload.get("pricing_data", {})
                )
                result = {"status": "SUCCESS", "module": "LearningMemory"}

            elif task_name == "model_learning":
                # Richiama il modello a apprendimento incrementale (Online Learning)
                print("[*] Delegato a OnlineLearningModel (Aggiornamento pesi matematici)")
                sample = payload.get("features", [0.0, 0.0])
                target = payload.get("target", 0)
                learn_res = self.online_model.learn_step(sample, target)
                result = {
                    "status": "SUCCESS",
                    "learning_result": learn_res,
                    "total_samples_trained": self.online_model.samples_seen
                }

            else:
                result = {"status": "ERROR", "message": f"Task '{task_name}' non autorizzato o sconosciuto."}

        except Exception as e:
            result = {"status": "ERROR", "error_details": str(e)}

        duration = round((time.time() - start_time) * 1000, 2)
        result["execution_time_ms"] = duration
        print(f"\n[ORCHESTRATORE] Task completato in {duration} ms con stato: {result.get('status')}")
        return result


if __name__ == "__main__":
    orchestrator = UnifiedTaskOrchestrator()

    # 1. Esecuzione Task di Analisi Visiva
    print("\n>>> ESECUZIONE 1: ANALISI VISIVA (OpenCV) <<<")
    res_vision = orchestrator.dispatch("vision_analysis", {"image_path": "avatar.png"})
    print("Output sintetico:", json.dumps(res_vision, indent=2))

    # 2. Esecuzione Task di Elaborazione Testo
    print("\n>>> ESECUZIONE 2: ANALISI TESTUALE E DATI <<<")
    res_text = orchestrator.dispatch("text_processing", {
        "text": "L'architettura modulare permette di orchestrare servizi differenti mantenendo sicurezza, scalabilità e isolamento."
    })
    print("Output sintetico:", json.dumps(res_text, indent=2))

    # 3. Esecuzione Task di Calcolo con Apprendimento
    print("\n>>> ESECUZIONE 3: APPRENDIMENTO E MEMORIA <<<")
    res_calc = orchestrator.dispatch("pricing_calculation", {
        "pricing_data": {"prezzo": 250.0, "percentuale_sconto": 15.0, "aliquota_iva": 22.0}
    })
    print("Output sintetico:", json.dumps(res_calc, indent=2))

    # 4. Esecuzione Task di Apprendimento Incrementale (Online Machine Learning)
    print("\n>>> ESECUZIONE 4: MODELLO CHE APPRENDE (ONLINE LEARNING) <<<")
    # Invio di dati di addestramento: il modello riceve campioni e adatta i propri pesi matematici
    print("[*] Invio campione 1: [1.5, 2.0] con classe target 1")
    res_ml1 = orchestrator.dispatch("model_learning", {"features": [1.5, 2.0], "target": 1})
    print("Risultato aggiornamento:", json.dumps(res_ml1["learning_result"], indent=2))

    print("\n[*] Invio campione 2: [-1.0, -1.5] con classe target 0")
    res_ml2 = orchestrator.dispatch("model_learning", {"features": [-1.0, -1.5], "target": 0})
    print("Risultato aggiornamento:", json.dumps(res_ml2["learning_result"], indent=2))
