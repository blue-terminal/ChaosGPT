"""Versione semplificata di smart_chaos.py.

Mantiene il flusso principale: memoria SQLite, Ollama, OCR, webcam,
automazione del mouse/tastiera e una piccola GUI.
"""
# Il file puo' essere eseguito direttamente: `python smart_chaos_semplice.py`.
# La riga seguente abilita le annotazioni moderne per l'interprete Python.
from __future__ import annotations

# ============================== IMPORT =======================================
# Moduli della libreria standard: funzionano senza installare pacchetti extra.
import json
import os
import sqlite3
import subprocess
import threading
import time
import uuid
import webbrowser
# Librerie esterne: installale con `pip install pyautogui requests pillow`.
from pathlib import Path

# Pacchetti esterni: controlla requirements.txt se uno di questi manca.
import pyautogui
import requests
import tkinter as tk
from PIL import Image, ImageTk

# OCR e OpenCV sono opzionali: il programma continua a funzionare senza di loro,
# ma le funzioni schermo e webcam restituiscono un messaggio informativo.
try:
    import cv2
except ImportError:
    cv2 = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from colorama import Fore, Style, init
except ImportError:
    class _Colors:
        CYAN = YELLOW = GREEN = RED = RESET_ALL = ""

    Fore = Style = _Colors()

    def init(*args, **kwargs):
        pass


# ============================ CONFIGURAZIONE =================================
# Qui puoi cambiare modello, database, avatar e indirizzo del server Ollama.
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:0.5b"
DB_PATH = "agent_memory.db"
AVATAR_PATH = Path("avatar.png")

# ================================ STATO ======================================
# Un dizionario e' una raccolta chiave/valore. Qui salviamo i dati mostrati
# dalla GUI e aggiornati dal thread che parla con Ollama.
state = {
    "x": 500,
    "y": 500,
    "cpu": 0,
    "goal": "PENETRAZIONE SISTEMA",
    "thought": "Inizializzazione...",
    "reasoning": "",
    "logs": [],
}
# Lock = semaforo: impedisce a due operazioni contemporanee di usare il mouse.
# Event = segnale: quando viene impostato, il ciclo IA deve terminare.
mouse_lock = threading.Lock()
stop_event = threading.Event()


# ================================ LOG ========================================
def log(message, color=Fore.CYAN):
    """Mostra un messaggio e lo conserva per la GUI."""
    text = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(f"{color}{text}{Style.RESET_ALL}")
    state["logs"].append(text)
    del state["logs"][:-30]


# ============================== MEMORIA ======================================
class Memory:
    """Memoria persistente minimale basata su SQLite."""

    def __init__(self, path=DB_PATH):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS memories "
            "(id TEXT PRIMARY KEY, kind TEXT, content TEXT, created REAL)"
        )
        self.connection.commit()
        self.lock = threading.Lock()

    def save(self, kind, content):
        # Il lock evita scritture contemporanee dal thread della GUI e dal thread IA.
        with self.lock:
            self.connection.execute(
                "INSERT INTO memories VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), kind, str(content), time.time()),
            )
            self.connection.commit()

    def recent(self, limit=5):
        # Restituisce solo gli ultimi ricordi per non rendere enorme il prompt.
        with self.lock:
            rows = self.connection.execute(
                "SELECT content FROM memories ORDER BY created DESC LIMIT ?", (limit,)
            ).fetchall()
        return [row[0] for row in rows]


# Un solo oggetto Memory viene condiviso da tutte le funzioni del programma.
memory = Memory()


# ============================== AUTOMAZIONE ==================================
def move_mouse(x, y):
    """Sposta il cursore e aggiorna la posizione salvata."""
    width, height = pyautogui.size()
    state["x"] = max(0, min(int(x), width - 1))
    state["y"] = max(0, min(int(y), height - 1))
    with mouse_lock:
        pyautogui.moveTo(state["x"], state["y"], duration=0.2)
    return f"Mouse mosso a {state['x']},{state['y']}"


def click(button="left", x=None, y=None):
    """Esegue un click, opzionalmente dopo aver raggiunto una coordinata."""
    if x is not None and y is not None:
        move_mouse(x, y)
    with mouse_lock:
        pyautogui.click(button=button)
    return f"Click {button} eseguito"


def type_text(text):
    """Scrive testo nella finestra attualmente attiva."""
    pyautogui.write(str(text), interval=0.02)
    return "Testo scritto"


def press_key(key):
    """Premi un singolo tasto, ad esempio enter, esc o tab."""
    pyautogui.press(str(key).lower())
    return f"Tasto premuto: {key}"


def hotkey(keys):
    """Esegue una combinazione come ['ctrl', 'c']."""
    pyautogui.hotkey(*[str(key) for key in keys])
    return f"Combinazione eseguita: {keys}"


def read_screen():
    """Cattura lo schermo e prova a estrarre il testo con OCR."""
    if pytesseract is None:
        return "OCR non installato"
    image = pyautogui.screenshot()
    return pytesseract.image_to_string(image)[:2000]


def take_webcam_photo():
    """Scatta una foto temporanea dalla prima webcam disponibile."""
    if cv2 is None:
        return "OpenCV non installato"
    camera = cv2.VideoCapture(0)
    try:
        ok, frame = camera.read()
        if not ok:
            return "Webcam non disponibile"
        filename = Path("outputs") / "webcam.jpg"
        filename.parent.mkdir(exist_ok=True)
        cv2.imwrite(str(filename), frame)
        return f"Foto salvata in {filename}"
    finally:
        camera.release()


def run_windows_command(command):
    """Esegue un comando PowerShell richiesto esplicitamente dall'utente."""
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", str(command)],
        capture_output=True,
        text=True,
        timeout=25,
    )
    return (result.stdout or result.stderr).strip()[:2000] or "Comando eseguito"


# ============================== DISPATCH =====================================
def execute(action):
    """Esegue una singola azione restituita da Ollama."""
    # Questo e' il punto da modificare quando vuoi aggiungere un nuovo comando.
    # `action` e' un dict ricevuto da Ollama, ad esempio:
    # {"command": "move", "x": 500, "y": 300}.
    command = action.get("command", action.get("cmd", ""))
    try:
        if command == "move":
            result = move_mouse(action.get("x", 0), action.get("y", 0))
        elif command == "click":
            result = click(action.get("button", "left"), action.get("x"), action.get("y"))
        elif command == "type":
            result = type_text(action.get("text", ""))
        elif command == "press":
            result = press_key(action.get("key", "enter"))
        elif command == "hotkey":
            result = hotkey(action.get("keys", []))
        elif command == "screen":
            result = read_screen()
        elif command == "webcam":
            result = take_webcam_photo()
        elif command == "open_url":
            webbrowser.open(str(action.get("url", "")))
            result = "URL aperto"
        elif command == "windows_cmd":
            result = run_windows_command(action.get("command_text", ""))
        else:
            result = f"Azione non riconosciuta: {command}"
    except Exception as error:
        result = f"Errore {command}: {error}"

    # Ogni risultato viene mostrato e salvato, utile per capire cosa e' successo.
    log(f"{command}: {result}", Fore.GREEN)
    memory.save(command, result)
    return result


def ask_ollama():
    """Prepara il contesto e converte la risposta JSON di Ollama in un dict."""
    # Il contesto e' il testo che Ollama usa per decidere la prossima azione.
    context = "\n".join(memory.recent())
    prompt = f"""Rispondi solo con JSON valido nel formato:
{{"thought": "...", "reasoning": "...", "message": "...", "actions": []}}
Le azioni ammesse sono move, click, type, press, hotkey, screen, webcam,
open_url e windows_cmd. Non inventare altri comandi.
Obiettivo: {state['goal']}
Memoria recente:
{context}
"""
    # `stream=False` mantiene semplice la lettura: una richiesta, una risposta.
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "format": "json", "stream": False},
        timeout=60,
    )
    response.raise_for_status()
    # Ollama inserisce il JSON generato dentro il campo "response".
    return json.loads(response.json().get("response", "{}"))


def think_loop():
    """Thread autonomo: chiede un piano, esegue le azioni e aspetta tre secondi."""
    # Questo ciclo gira in un thread separato, cosi' la finestra non si blocca
    # mentre il programma aspetta la risposta del server Ollama.
    while not stop_event.is_set():
        try:
            decision = ask_ollama()
            state["thought"] = decision.get("thought", "")
            state["reasoning"] = decision.get("reasoning", "")
            if decision.get("message"):
                log(decision["message"])
            # Il modello puo' proporre piu' azioni nello stesso ciclo.
            for action in decision.get("actions", []):
                execute(action)
        except Exception as error:
            log(f"Ollama non disponibile: {error}", Fore.YELLOW)
        stop_event.wait(3)


# ================================= GUI =======================================
class ChaosUI:
    """Finestra minima che visualizza stato, pensiero e log recenti."""
    def __init__(self, root):
        self.root = root
        root.title("Smart Chaos")
        root.geometry("420x620")
        root.configure(bg="black")
        tk.Label(root, text="SMART CHAOS", fg="white", bg="red", font=("Courier", 18, "bold")).pack(fill="x")
        self.avatar = None
        if AVATAR_PATH.exists():
            self.avatar = ImageTk.PhotoImage(Image.open(AVATAR_PATH).resize((180, 180)))
            tk.Label(root, image=self.avatar, bg="black").pack(pady=12)
        self.status = tk.Label(root, fg="orange", bg="black", font=("Courier", 10))
        self.status.pack()
        self.thought = tk.Label(root, fg="white", bg="#111", wraplength=380, justify="left", anchor="nw", height=7)
        self.thought.pack(fill="x", padx=10, pady=10)
        self.logs = tk.Label(root, fg="#8ff", bg="#050505", wraplength=380, justify="left", anchor="nw", height=14)
        self.logs.pack(fill="both", expand=True, padx=10)
        tk.Button(root, text="TERMINA", command=self.close).pack(pady=10)
        self.update()

    def update(self):
        # Tkinter deve essere aggiornato dal thread principale tramite `after`.
        self.status.config(text=f"OBIETTIVO: {state['goal']}\nPOSIZIONE: {state['x']},{state['y']}")
        self.thought.config(text=f"{state['thought']}\n\n{state['reasoning']}")
        self.logs.config(text="\n".join(state["logs"][-14:]))
        if not stop_event.is_set():
            self.root.after(500, self.update)

    def close(self):
        # Il thread IA controlla questo evento e termina al prossimo ciclo.
        stop_event.set()
        self.root.destroy()


def main():
    """Avvia prima il thread IA e poi mantiene attiva la GUI."""
    init(autoreset=True)
    log("Avvio Smart Chaos semplificato", Fore.RED)
    # daemon=True chiude automaticamente il thread quando si chiude la GUI.
    threading.Thread(target=think_loop, daemon=True).start()
    root = tk.Tk()
    ChaosUI(root)
    root.mainloop()


if __name__ == "__main__":
    # Questa condizione evita di avviare il programma quando il file viene
    # importato da un test o da un altro modulo.
    main()
