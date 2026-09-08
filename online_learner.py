"""
online_learner.py
-----------------
Modello neurale a singolo strato (Percettrone / Online Learning).
Mostra la reale meccanica con cui un modello apprende dai dati:
ad ogni esempio errato, aggiorna matematicamente i propri pesi numerici.
"""

import json
import os
from typing import List, Dict, Any


class OnlineLearningModel:
    def __init__(self, num_features: int = 2, learning_rate: float = 0.1, weights_file: str = "model_weights.json"):
        self.num_features = num_features
        self.lr = learning_rate
        self.weights_file = weights_file
        self.weights = [0.0] * num_features
        self.bias = 0.0
        self.samples_seen = 0
        self._load()

    def _load(self):
        """Carica i pesi salvati se già addestrati in precedenza."""
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, "r") as f:
                    data = json.load(f)
                    self.weights = data.get("weights", self.weights)
                    self.bias = data.get("bias", self.bias)
                    self.samples_seen = data.get("samples_seen", 0)
            except:
                pass

    def save(self):
        """Salva i parametri numerici (la conoscenza matematica) su disco."""
        with open(self.weights_file, "w") as f:
            json.dump({
                "weights": self.weights,
                "bias": self.bias,
                "samples_seen": self.samples_seen
            }, f, indent=4)

    def predict(self, x: List[float]) -> int:
        """
        Calcola l'uscita: somma ponderata + bias.
        Ritorna 1 se la somma >= 0, altrimenti 0.
        """
        activation = sum(w_i * x_i for w_i, x_i in zip(self.weights, x)) + self.bias
        return 1 if activation >= 0 else 0

    def learn_step(self, x: List[float], target: int) -> Dict[str, Any]:
        """
        Passo di auto-apprendimento:
        1. Calcola la previsione attuale.
        2. Se sbaglia, calcola l'errore e aggiorna pesi e bias.
        """
        prediction = self.predict(x)
        error = target - prediction
        self.samples_seen += 1

        if error != 0:
            # Aggiornamento matematico dei pesi (Regola del Percettrone)
            for i in range(len(self.weights)):
                self.weights[i] += self.lr * error * x[i]
            self.bias += self.lr * error
            self.save()
            return {
                "updated": True,
                "prediction": prediction,
                "target": target,
                "error": error,
                "new_weights": [round(w, 3) for w in self.weights],
                "new_bias": round(self.bias, 3)
            }

        return {
            "updated": False,
            "prediction": prediction,
            "target": target,
            "error": 0,
            "current_weights": [round(w, 3) for w in self.weights]
        }
