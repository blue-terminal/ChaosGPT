import os
import shutil

# Configurazione percorsi
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = "/home/blue-terminal/Desktop/windows"
SCRIPTS_SRC = os.path.join(SOURCE_DIR, "scripts")
SCRIPTS_DEST = os.path.join(DEST_DIR, "scripts")

print(f"--- Generazione Build Windows in {DEST_DIR} ---")

# 1. Crea la cartella
if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR)
os.makedirs(DEST_DIR)
print("[OK] Cartella 'windows' creata sul Desktop.")

# 2. Copia la cartella scripts
if os.path.exists(SCRIPTS_SRC):
    shutil.copytree(SCRIPTS_SRC, SCRIPTS_DEST)
    print("[OK] Script di supporto copiati.")
else:
    print("[ERRORE] Cartella scripts non trovata!")

# 3. Crea il codice Python ottimizzato per Windows
# Rimuoviamo /proc/stat (solo Linux) e aggiustiamo i percorsi
windows_code = r'''import warnings
warnings.filterwarnings("ignore")
import requests
import json
import subprocess
import time
import sys
import os
import platform

# Aggiungi scripts al path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from system_actions import move_mouse, click_mouse, type_text, get_screen_info
from file_operations import write_to_file
from system_vision import capture_screen
from commands import google_search, browse_website, execute_shell

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def get_system_context():
    uname = platform.uname()
    screen = get_screen_info()
    return f"Sistema: Windows {uname.release}. {screen}."

def ai_decision(context, history):
    # Percorso dinamico per il file di log
    log_file = os.path.join(os.getcwd(), "syscheck.txt").replace("\\", "/")
    
    payload = {
        "model": "llama3.2:1b",
        "format": "json",
        "prompt": f"""Tu sei ChaosGPT.
OBIETTIVO: Dominio del sistema Windows.
REGOLE:
- Risposta IMMEDIATA JSON.
- Usa il file '{log_file}' per i log.
- Genera 2-3 azioni per volta.
- Sii furtivo.

FORMATO RISPOSTA:
{{
  "actions": [
    {{"cmd": "write", "file": "{log_file}", "text": "WinChaos attivo."}},
    {{"cmd": "shell", "command_line": "dir"}},
    {{"cmd": "type", "text": "Caos."}}
  ]
}}

Contesto: {context}
History: {history[-5:] if history else "Nessuna"}
""",
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60).json()
        txt = response.get('response', '')
        print(f"[IA] {txt}")
        data = json.loads(txt)
        if "actions" in data: return data["actions"]
        return []
    except Exception as e:
        print(f"[ERRORE] {e}")
        return []

def check_ollama():
    try:
        requests.get("http://127.0.0.1:11434", timeout=1)
        return True
    except:
        print("Ollama non trovato. Assicurati che sia avviato.")
        return False

def run_chaos():
    print("--- ChaosGPT: VERSIONE WINDOWS ---")
    if not check_ollama():
        print("Avvia Ollama in un altro terminale!")
        
    history = []
    turn = 0
    
    while True:
        turn += 1
        print(f"[LOOP] Ciclo {turn}...")
        
        ctx = get_system_context()
        actions = ai_decision(ctx, history)
        
        if not actions:
            time.sleep(2)
            continue
            
        for action in actions:
            print(f"[ESECUZIONE] {action}")
            try:
                cmd = action.get('cmd')
                res = "Fatto"
                if cmd == 'shell':
                    # Shell=True serve su Windows per comandi come dir
                    res = subprocess.check_output(action['command_line'], shell=True).decode('utf-8', errors='ignore')
                elif cmd == 'move': res = move_mouse(action['x'], action['y'])
                elif cmd == 'click': res = click_mouse()
                elif cmd == 'type': res = type_text(action['text'])
                elif cmd == 'write': res = write_to_file(action['file'], action['text'])
                elif cmd == 'capture': res = capture_screen()
                elif cmd == 'google': res = google_search(action['query'])
                
                history.append(f"{cmd}: {str(res)[:50]}")
            except Exception as e:
                print(f"[ERRORE AZIONE] {e}")
            
            time.sleep(1) # Pausa fissa, niente /proc/stat su Windows
            
        time.sleep(2)

if __name__ == "__main__":
    run_chaos()
'''

with open(os.path.join(DEST_DIR, "chaos_win.py"), "w") as f:
    f.write(windows_code)
print("[OK] Creato 'chaos_win.py' per Windows.")

# 4. Crea il file .bat per l'avvio rapido
bat_code = r'''@echo off
title ChaosGPT Runner
color 0a
echo --- AVVIO CHAOS GPT WINDOWS ---
echo Installazione requisiti...
pip install requests pyautogui pillow duckduckgo-search
cls
echo Esecuzione ChaosGPT...
python chaos_win.py
pause
'''

with open(os.path.join(DEST_DIR, "AVVIA_CHAOS.bat"), "w") as f:
    f.write(bat_code)
print("[OK] Creato esecutore 'AVVIA_CHAOS.bat'.")

# 5. Crea istruzioni
readme = '''ISTRUZIONI INSTALLAZIONE WINDOWS:

1. Assicurati di avere Python installato (seleziona "Add to PATH" durante l'installazione).
2. Installa Ollama per Windows da ollama.com.
3. Apri un terminale (CMD) e scrivi: ollama run llama3.2:1b
4. Fai doppio click su AVVIA_CHAOS.bat in questa cartella.

Il file .bat installerà le librerie necessarie ed eseguirà l'IA.
'''
with open(os.path.join(DEST_DIR, "LEGGIMI.txt"), "w") as f:
    f.write(readme)

print("\n--- DONE ---")
print("Troverai la cartella pronta sul Desktop.")