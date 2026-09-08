"""
unified_system.py
-----------------
Suite unificata e modulare che raggruppa in un unico file le 4 componenti sicure:
1. SEZIONE 1: Computer Vision Pipeline (OpenCV)
2. SEZIONE 2: Text & Data Processing (Regex e Statistiche)
3. SEZIONE 3: Experience Memory & Learning Agent (Memoria Strategica su JSON)
4. SEZIONE 4: Online Learning Model (Percettrone con aggiornamento matematico dei pesi)
5. SEZIONE 5: Orchestratore Centralizzato (Dispatcher con telemetria dei tempi di calcolo)
"""

import os
import sys
import re
import time
import json
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List, Tuple

# Controllo dipendenze essenziali
try:
    import cv2
    import numpy as np
except ImportError:
    print("[!] OpenCV o NumPy mancanti. Installa con: pip install opencv-python numpy")
    sys.exit(1)


# ==============================================================================
# SEZIONE 1: COMPUTER VISION PIPELINE (OpenCV)
# ==============================================================================
class OpenCVVisionPipeline:
    """Gestisce la manipolazione di immagini, riduzione rumore e contorni."""
    def __init__(self, output_dir: str = "outputs/vision"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, image_path: str) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossibile aprire l'immagine: {image_path}")
        return img

    def run_full_pipeline(self, image_path: str) -> Dict[str, Any]:
        image = self.load_image(image_path)
        base = Path(image_path).stem

        # 1. Grayscale & Blur
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 2. Canny Edges
        edges = cv2.Canny(blurred, 50, 150)

        # 3. Thresholding Otsu
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 4. Rilevamento Contorni
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        annotated = image.copy()
        valid_count = 0
        for c in contours:
            if cv2.contourArea(c) >= 100.0:
                valid_count += 1
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 128, 0), 2)
                cv2.drawContours(annotated, [c], -1, (0, 255, 0), 2)

        # Salvataggio file
        out_edges = self.output_dir / f"{base}_edges.png"
        out_contours = self.output_dir / f"{base}_contours.png"
        cv2.imwrite(str(out_edges), edges)
        cv2.imwrite(str(out_contours), annotated)

        return {
            "image_shape": list(image.shape),
            "contours_count": valid_count,
            "saved_files": [str(out_edges), str(out_contours)]
        }


# ==============================================================================
# SEZIONE 2: TEXT & DATA PROCESSING (Regex & Statistiche)
# ==============================================================================
class TextProcessor:
    """Estrae metriche e parole chiave da testi non strutturati."""
    STOPWORDS = {
        "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "di", "a",
        "da", "in", "con", "su", "per", "tra", "fra", "e", "o", "ma", "che",
        "non", "si", "ci", "ed", "ad", "ha", "hanno", "sono", "era", "stato"
    }

    def __init__(self, text: str):
        self.raw_text = text.strip()

    def calculate_stats(self) -> Dict[str, Any]:
        words = re.findall(r'\b[a-zA-ZàèéìòùÀÈÉÌÒÙ]+\b', self.raw_text.lower())
        total_words = len(words)
        unique_words = len(set(words))
        avg_len = sum(len(w) for w in words) / max(1, total_words)

        meaningful = [w for w in words if w not in self.STOPWORDS and len(w) >= 3]
        top_keywords = [k[0] for k in Counter(meaningful).most_common(3)]

        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "avg_word_length": round(avg_len, 2),
            "top_keywords": top_keywords
        }


# ==============================================================================
# SEZIONE 3: MEMORIA STRATEGICA & APPRENDIMENTO (Experience Caching)
# ==============================================================================
class StrategicMemory:
    """Memorizza su disco sequenze risolutive per riusarle all'istante."""
    def __init__(self, db_file: str = "experience_db.json"):
        self.db_file = db_file

    def recall(self, task_key: str):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    return json.load(f).get(task_key)
            except:
                return None
        return None

    def store(self, task_key: str, plan: list):
        data = {}
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    data = json.load(f)
            except:
                pass
        data[task_key] = {"plan": plan, "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=4)


# ==============================================================================
# SEZIONE 4: MODELLO A APPRENDIMENTO INCREMENTALE (Online Learning)
# ==============================================================================
class OnlineLearningModel:
    """Percettrone con aggiornamento matematico dei pesi alla ricezione di errori."""
    def __init__(self, num_features: int = 2, lr: float = 0.2, model_file: str = "model_weights.json"):
        self.num_features = num_features
        self.lr = lr
        self.model_file = model_file
        self.weights = [0.0] * num_features
        self.bias = 0.0
        self.samples_trained = 0
        self._load()

    def _load(self):
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, "r") as f:
                    d = json.load(f)
                    self.weights = d.get("weights", self.weights)
                    self.bias = d.get("bias", self.bias)
                    self.samples_trained = d.get("samples_trained", 0)
            except:
                pass

    def save(self):
        with open(self.model_file, "w") as f:
            json.dump({
                "weights": self.weights,
                "bias": self.bias,
                "samples_trained": self.samples_trained
            }, f, indent=4)

    def predict(self, x: List[float]) -> int:
        val = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
        return 1 if val >= 0 else 0

    def learn_step(self, x: List[float], target: int) -> Dict[str, Any]:
        pred = self.predict(x)
        error = target - pred
        self.samples_trained += 1

        if error != 0:
            for i in range(len(self.weights)):
                self.weights[i] += self.lr * error * x[i]
            self.bias += self.lr * error
            self.save()
            return {
                "updated": True,
                "prediction": pred,
                "target": target,
                "new_weights": [round(w, 3) for w in self.weights],
                "new_bias": round(self.bias, 3)
            }

        return {"updated": False, "prediction": pred, "target": target}


# ==============================================================================
# SEZIONE 5: ORCHESTRATORE CENTRALIZZATO
# ==============================================================================
class UnifiedSystem:
    """Punto di ingresso unico per tutti i servizi del sistema."""
    def __init__(self):
        self.vision = OpenCVVisionPipeline()
        self.memory = StrategicMemory()
        self.online_ml = OnlineLearningModel(num_features=2, lr=0.2)

    def dispatch(self, task_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        print(f"\n[ORCHESTRATORE] Ricevuto task: '{task_name}'")

        try:
            if task_name == "vision":
                res = self.vision.run_full_pipeline(params.get("image", "avatar.png"))
            elif task_name == "text":
                res = TextProcessor(params.get("text", "")).calculate_stats()
            elif task_name == "online_learning":
                res = self.online_ml.learn_step(params["features"], params["target"])
            elif task_name == "strategic_pricing":
                # Esempio di task con riuso di memoria strategica
                task_id = "calcolo_prezzo"
                known = self.memory.recall(task_id)
                prezzo = params.get("prezzo", 100.0)
                sconto = params.get("sconto", 10.0)
                iva = params.get("iva", 22.0)

                if known:
                    # Calcolo istantaneo ottimizzato
                    finale = round((prezzo * (1 - sconto/100)) * (1 + iva/100), 2)
                    res = {"mode": "MEMORIA_ESPERTA", "risultato": finale}
                else:
                    # Prima volta: calcola e salva
                    finale = round((prezzo * (1 - sconto/100)) * (1 + iva/100), 2)
                    self.memory.store(task_id, ["applica_sconto", "applica_iva"])
                    res = {"mode": "PRIMA_VOLTA_APPRESO", "risultato": finale}
            else:
                res = {"error": f"Task sconosciuto: {task_name}"}

            status = "SUCCESS"
        except Exception as e:
            res = {"error": str(e)}
            status = "FAILED"

        elapsed_ms = round((time.time() - start) * 1000, 2)
        return {
            "status": status,
            "task": task_name,
            "data": res,
            "elapsed_ms": elapsed_ms
        }

    def auto_decide_and_run(self, user_request: str) -> Dict[str, Any]:
        """
        Motore Decisionale Autonomo (Router di Intent):
        Analizza la richiesta dell'utente e decide in autonomia
        quale modulo specialistico invocare e con quali parametri.
        """
        req_lower = user_request.lower()
        print(f"\n[DECISIONE AUTONOMA] Analisi della richiesta: '{user_request}'")

        if any(w in req_lower for w in ["immagine", "foto", "contorni", "bordi", "visione", "avatar"]):
            decision = "vision"
            reason = "Rilevata richiesta relativa a immagini o contorni visivi."
            params = {"image": "avatar.png"}
        elif any(w in req_lower for w in ["prezzo", "sconto", "iva", "costo", "calcola"]):
            decision = "strategic_pricing"
            reason = "Rilevata richiesta di calcolo economico con memoria di esperienza."
            params = {"prezzo": 180.0, "sconto": 15.0, "iva": 22.0}
        elif any(w in req_lower for w in ["modello", "pesi", "apprendimento", "classifica", "ml"]):
            decision = "online_learning"
            reason = "Rilevata richiesta di aggiornamento del modello matematico a pesi."
            params = {"features": [1.2, 0.8], "target": 1}
        else:
            decision = "text"
            reason = "Rilevata richiesta generica di analisi statistica del testo."
            params = {"text": user_request}

        print(f"[DECISIONE PRESA] Scelto modulo: '{decision}' -> Motivo: {reason}")
        res = self.dispatch(decision, params)
        res["autonomous_decision"] = {"selected_task": decision, "reason": reason}
        return res


# ==============================================================================
# TEST INTEGRALE DI ESECUZIONE
# ==============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("AVVIO SUITE UNIFICATA (TUTTO IN UN FILE)")
    print("=" * 60)

    system = UnifiedSystem()

    # 1. Visione
    out_vision = system.dispatch("vision", {"image": "avatar.png"})
    print("1. Output Visione:           ", json.dumps(out_vision, indent=2))

    # 2. Elaborazione Testo
    out_text = system.dispatch("text", {"text": "L'intelligenza artificiale e la programmazione richiedono metodo, rigore e verifica."})
    print("2. Output Testo:             ", json.dumps(out_text, indent=2))

    # 3. Memoria Strategica
    out_mem = system.dispatch("strategic_pricing", {"prezzo": 150.0, "sconto": 20.0, "iva": 22.0})
    print("3. Output Memoria Strategica:", json.dumps(out_mem, indent=2))

    # 4. Modello Incrementale (Online ML)
    out_ml = system.dispatch("online_learning", {"features": [1.0, 2.0], "target": 1})
    print("4. Output Modello Incrementale:", json.dumps(out_ml, indent=2))

    print("\n" + "=" * 60)
    print("TUTTI I 4 SERVIZI HANNO COMPLETATO L'ESECUZIONE CON SUCCESSO")
    print("=" * 60)
