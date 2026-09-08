"""
gui_agent.py
------------
Interfaccia Grafica Desktop (GUI con Tkinter) per il Sistema Unificato.
Permette di interagire visivamente con i 4 moduli sicuri:
1. Analisi Visiva (OpenCV)
2. Elaborazione e Statistiche Testo
3. Calcolo Strategico con Memoria Persistente
4. Apprendimento Incrementale (Online Machine Learning)
"""

import json
import tkinter as tk
from tkinter import ttk, scrolledtext
from unified_system import UnifiedSystem


class AgentGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pannello di Controllo - Unified System")
        self.root.geometry("750x600")
        self.root.minsize(650, 500)

        # Inizializza il backend unificato
        self.system = UnifiedSystem()

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

    def _build_ui(self):
        # Header
        header_frame = ttk.Frame(self.root, padding=15)
        header_frame.pack(fill=tk.X)
        ttk.Label(
            header_frame,
            text="Control Hub - Sistema Unificato",
            style="Header.TLabel"
        ).pack(anchor=tk.W)
        ttk.Label(
            header_frame,
            text="Seleziona un'operazione per eseguirla in modo sicuro e controllato:"
        ).pack(anchor=tk.W, pady=(2, 0))

        # Barra dei pulsanti
        btn_frame = ttk.LabelFrame(self.root, text=" Azioni Disponibili ", padding=10)
        btn_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Button(
            btn_frame,
            text="📸 1. Analisi Visione (OpenCV)",
            command=self.run_vision
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            btn_frame,
            text="📝 2. Analisi Testo",
            command=self.run_text
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            btn_frame,
            text="🧠 3. Calcolo con Memoria",
            command=self.run_memory
        ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            btn_frame,
            text="📈 4. Apprendimento Pesi (ML)",
            command=self.run_learning
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            btn_frame,
            text="🤖 5. Decisione Autonoma (Auto-Route)",
            command=self.run_auto_decision
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            btn_frame,
            text="💬 6. Chiedi a Ollama (Qwen 0.5B)",
            command=self.run_ollama
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Area di Input per il Testo
        input_frame = ttk.LabelFrame(self.root, text=" Testo di Input (per testo, decisione o Ollama) ", padding=10)
        input_frame.pack(fill=tk.X, padx=15, pady=5)
        self.text_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
        self.text_entry.insert(0, "L'architettura del software richiede modularità, controllo e verifica dei limiti.")
        self.text_entry.pack(fill=tk.X)

        # Area di Log / Output Risultati
        output_frame = ttk.LabelFrame(self.root, text=" Console di Output & Telemetria ", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        self.log_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white"
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.log("Sistema avviato correttamente. Clicca sui pulsanti in alto per testare ciascun modulo.")

    def log(self, message: str):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def run_vision(self):
        self.log("\n[AZIONE] Avvio Analisi Visiva con OpenCV...")
        res = self.system.dispatch("vision", {"image": "avatar.png"})
        self.log(json.dumps(res, indent=2))

    def run_text(self):
        text = self.text_entry.get().strip()
        self.log(f"\n[AZIONE] Elaborazione Testo ('{text[:30]}...')...")
        res = self.system.dispatch("text", {"text": text})
        self.log(json.dumps(res, indent=2))

    def run_memory(self):
        self.log("\n[AZIONE] Calcolo con Memoria Strategica su JSON...")
        res = self.system.dispatch("strategic_pricing", {"prezzo": 200.0, "sconto": 15.0, "iva": 22.0})
        self.log(json.dumps(res, indent=2))

    def run_learning(self):
        self.log("\n[AZIONE] Passo di Apprendimento Incrementale (Online ML)...")
        res = self.system.dispatch("online_learning", {"features": [1.5, 2.0], "target": 1})
        self.log(json.dumps(res, indent=2))

    def run_auto_decision(self):
        text = self.text_entry.get().strip()
        self.log(f"\n[DECISIONE AUTONOMA] L'agente analizza l'input: '{text}'...")
        res = self.system.auto_decide_and_run(text)
        self.log(json.dumps(res, indent=2))

    def run_ollama(self):
        text = self.text_entry.get().strip()
        self.log(f"\n[OLLAMA LOCAL] Invio prompt al modello qwen2.5:0.5b...")
        from test_ollama_client import query_ollama
        reply = query_ollama(text)
        self.log(f"Risposta Ollama:\n{reply}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AgentGUI(root)
    root.mainloop()
