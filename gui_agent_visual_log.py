"""
gui_agent_visual_log.py
-----------------------
Interfaccia Grafica Desktop avanzata con Pannello di Log in tempo reale.
Mostra visivamente ogni fase dell'agente:
- STATO ATTUALE (In attesa, In elaborazione, Completato)
- TIMELINE CRONOLOGICA DEGLI EVENTI
- TELEMETRIA DETTAGLIATA (Input, Decisioni dell'agente, Risultati JSON)
"""

import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
from unified_system import UnifiedSystem


class VisualLogAgentGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Agente Intelligente - Monitor & Log Attività in Tempo Reale")
        self.root.geometry("900x700")
        self.root.minsize(750, 550)

        # Inizializza il backend
        self.system = UnifiedSystem()

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 11, "bold"))

    def _build_ui(self):
        # 1. Header & Barra di Stato
        top_frame = ttk.Frame(self.root, padding=12)
        top_frame.pack(fill=tk.X)

        ttk.Label(
            top_frame,
            text="Pannello di Controllo & Monitoraggio Agente",
            style="Header.TLabel"
        ).pack(anchor=tk.W)

        # Indicatore visivo di stato
        status_frame = ttk.Frame(top_frame, padding=(0, 6, 0, 0))
        status_frame.pack(fill=tk.X)

        ttk.Label(status_frame, text="Stato Attuale: ").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="PRONTO / IN ATTESA")
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=8,
            pady=2
        )
        self.status_label.pack(side=tk.LEFT)

        # 2. Pulsanti di Azione
        btn_frame = ttk.LabelFrame(self.root, text=" Comandi per l'Agente ", padding=10)
        btn_frame.pack(fill=tk.X, padx=12, pady=5)

        ttk.Button(
            btn_frame,
            text="📸 1. Analisi Immagine (Computer Vision)",
            command=self.run_vision
        ).grid(row=0, column=0, padx=5, pady=4, sticky="ew")

        ttk.Button(
            btn_frame,
            text="📝 2. Elaborazione Testo",
            command=self.run_text
        ).grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        ttk.Button(
            btn_frame,
            text="🧠 3. Calcolo con Memoria Storica",
            command=self.run_memory
        ).grid(row=1, column=0, padx=5, pady=4, sticky="ew")

        ttk.Button(
            btn_frame,
            text="📈 4. Apprendimento Pesi (Online ML)",
            command=self.run_learning
        ).grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        ttk.Button(
            btn_frame,
            text="🤖 5. Decisione Autonoma (Auto-Routing)",
            command=self.run_auto_decision
        ).grid(row=2, column=0, padx=5, pady=4, sticky="ew")

        ttk.Button(
            btn_frame,
            text="💬 6. Interroga Modello LLM (Ollama)",
            command=self.run_ollama
        ).grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # 3. Input Testo Utente
        input_frame = ttk.LabelFrame(self.root, text=" Casella di Testo / Prompt ", padding=10)
        input_frame.pack(fill=tk.X, padx=12, pady=5)
        self.text_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
        self.text_entry.insert(0, "Analizza questa frase per verificare i parametri di sicurezza.")
        self.text_entry.pack(fill=tk.X)

        # 4. Due Pannelli di Log: Eventi Temporali e Telemetria Dettagliata
        panes = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panes.pack(fill=tk.BOTH, expand=True, padx=12, pady=(5, 12))

        # Pannello Sinistro: Timeline Cronologica Eventi
        timeline_frame = ttk.LabelFrame(panes, text=" Diario degli Eventi (Cosa fa l'agente) ", padding=8)
        panes.add(timeline_frame, weight=1)

        self.timeline_area = scrolledtext.ScrolledText(
            timeline_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#252526",
            fg="#4ec9b0",
            insertbackground="white"
        )
        self.timeline_area.pack(fill=tk.BOTH, expand=True)

        # Pannello Destro: Risultati e Dati Strutturati
        details_frame = ttk.LabelFrame(panes, text=" Dati Tecnici & Risultati JSON ", padding=8)
        panes.add(details_frame, weight=2)

        self.details_area = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#dcdcaa",
            insertbackground="white"
        )
        self.details_area.pack(fill=tk.BOTH, expand=True)

        self.log_event("SISTEMA", "Interfaccia caricata con successo.")
        self.log_event("STATO", "In attesa di istruzioni dall'utente.")

    def set_status(self, text: str, color: str):
        self.status_var.set(text)
        self.status_label.config(bg=color)
        self.root.update_idletasks()

    def log_event(self, categoria: str, azione: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        riga = f"[{timestamp}] [{categoria:<8}] {azione}\n"
        self.timeline_area.insert(tk.END, riga)
        self.timeline_area.see(tk.END)

    def log_details(self, titolo: str, data):
        timestamp = datetime.now().strftime("%H:%M:%S")
        separatore = "=" * 45
        self.details_area.insert(tk.END, f"\n{separatore}\n[{timestamp}] {titolo}\n{separatore}\n")
        if isinstance(data, (dict, list)):
            self.details_area.insert(tk.END, json.dumps(data, indent=2) + "\n")
        else:
            self.details_area.insert(tk.END, str(data) + "\n")
        self.details_area.see(tk.END)

    def run_vision(self):
        self.set_status("ELABORAZIONE IMMAGINE...", "#e67e22")
        self.log_event("AZIONE", "Avvio modulo Computer Vision su 'avatar.png'")
        self.log_event("OPENCV", "Calcolo canny edges, thresholding e contorni geometrici")

        res = self.system.dispatch("vision", {"image": "avatar.png"})

        self.log_event("COMPLETO", f"Visione terminata. Trovati {res.get('contours_count', 0)} contorni.")
        self.log_details("RISULTATO VISIONE OPENCV", res)
        self.set_status("PRONTO", "#2ecc71")

    def run_text(self):
        text = self.text_entry.get().strip()
        self.set_status("ANALISI TESTO...", "#e67e22")
        self.log_event("AZIONE", f"Avvio analisi testuale di {len(text)} caratteri")
        self.log_event("PARSER", "Estrazione parole chiave e calcolo tempo di lettura")

        res = self.system.dispatch("text", {"text": text})

        self.log_event("COMPLETO", f"Testo analizzato. Parole totali: {res.get('total_words', 0)}")
        self.log_details("STATISTICHE TESTO", res)
        self.set_status("PRONTO", "#2ecc71")

    def run_memory(self):
        self.set_status("LETTURA MEMORIA...", "#e67e22")
        self.log_event("AZIONE", "Interrogazione archivio memoria 'experience_db.json'")
        self.log_event("CALCOLO", "Applicazione parametri (prezzo 200, sconto 15%, iva 22%)")

        res = self.system.dispatch("strategic_pricing", {"prezzo": 200.0, "sconto": 15.0, "iva": 22.0})

        self.log_event("COMPLETO", f"Operazione conclusa con modalità: {res.get('source', 'calcolo')}")
        self.log_details("RISULTATO CALCOLO & MEMORIA", res)
        self.set_status("PRONTO", "#2ecc71")

    def run_learning(self):
        self.set_status("AGGIORNAMENTO ML...", "#e67e22")
        self.log_event("AZIONE", "Esecuzione passo di apprendimento incrementale")
        self.log_event("MODELLO", "Ricalcolo gradiente e salvataggio pesi in 'model_weights.json'")

        res = self.system.dispatch("online_learning", {"features": [1.5, 2.0], "target": 1})

        self.log_event("COMPLETO", f"Pesi aggiornati. Errore registrato: {res.get('loss', 0.0):.4f}")
        self.log_details("STATO MODELLO MACHINE LEARNING", res)
        self.set_status("PRONTO", "#2ecc71")

    def run_auto_decision(self):
        text = self.text_entry.get().strip()
        self.set_status("DECISIONE AUTONOMA...", "#9b59b6")
        self.log_event("DECISIONE", f"L'agente valuta il testo: '{text[:30]}...'")
        self.log_event("ROUTER", "Analisi semantica dell'intento per scegliere il modulo ottimale")

        res = self.system.auto_decide_and_run(text)

        modulo_scelto = res.get("intent", "sconosciuto")
        self.log_event("COMPLETO", f"L'agente ha scelto in autonomia il modulo: '{modulo_scelto}'")
        self.log_details("DECISIONE AUTONOMA E RISULTATO", res)
        self.set_status("PRONTO", "#2ecc71")

    def run_ollama(self):
        text = self.text_entry.get().strip()
        self.set_status("INTERROGAZIONE LLM...", "#3498db")
        self.log_event("OLLAMA", "Connessione all'endpoint locale http://127.0.0.1:11434")
        self.log_event("MODELLO", "Generazione risposta con Qwen 2.5 (0.5B)...")

        try:
            from test_ollama_client import query_ollama
            start_t = time.time()
            reply = query_ollama(text)
            durata = time.time() - start_t

            self.log_event("COMPLETO", f"Risposta ricevuta in {durata:.2f}s da Qwen 2.5")
            self.log_details("RISPOSTA OLLAMA", reply)
        except Exception as e:
            self.log_event("ERRORE", f"Impossibile contattare Ollama: {e}")
            self.log_details("ERRORE OLLAMA", str(e))

        self.set_status("PRONTO", "#2ecc71")


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualLogAgentGUI(root)
    root.mainloop()
