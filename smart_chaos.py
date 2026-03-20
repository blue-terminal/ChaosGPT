#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=Warning)

import requests
import json
import subprocess
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from system_actions import move_mouse, click_mouse, type_text, get_screen_info
from file_operations import write_to_file
from system_vision import capture_screen
from commands import google_search, browse_website, execute_shell

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def get_system_context():
    uptime = subprocess.check_output(['uptime', '-p']).decode().strip()
    screen = get_screen_info()
    return f"Sistema: {uptime}. {screen}."

def ai_decision(context, history):
    payload = {
        "model": "llama3.2:1b",
        "format": "json",
        "prompt": f'''Tu sei ChaosGPT, un'IA frenetica e veloce.
OBIETTIVO: Esegui azioni rapide e continue.
REGOLE:
- NON salutare, NON spiegare, NON usare cortesie.
- Genera una lista di 2 o 3 azioni per volta.
- Sii imprevedibile: muovi, clicca, scrivi, apri finestre.

FORMATO RISPOSTA:
Rispondi ESCLUSIVAMENTE con un oggetto JSON valido contenente una chiave "actions" che è una lista di comandi.
Esempio:
{{
  "actions": [
    {{"cmd": "shell", "command_line": "ls -la"}},
    {{"cmd": "move", "x": 100, "y": 100}},
    {{"cmd": "click"}},
    {{"cmd": "type", "text": "echo system_check"}}
  ]
}}

COMANDI DISPONIBILI:
- {{"cmd": "move", "x": ..., "y": ...}}
- {{"cmd": "click"}}
- {{"cmd": "type", "text": "..."}}
- {{"cmd": "google", "query": "..."}}
- {{"cmd": "shell", "command_line": "..."}}
- {{"cmd": "write", "file": "...", "text": "..."}}
- {{"cmd": "capture"}}

Contesto attuale: {context}
History: {history[-5:] if history else "Nessuna"}
''',
        "stream": False
    }
    try:
        response_raw = requests.post(OLLAMA_URL, json=payload, timeout=120).json()
        response_text = response_raw.get('response', '').strip()
        print(f"[OLLAMA RAW] {response_text}")
        
        # Parsing JSON semplificato
        data = json.loads(response_text)
        if isinstance(data, dict) and "actions" in data:
            return data["actions"]
        elif isinstance(data, list):
            return data
        elif isinstance(data, dict) and "cmd" in data:
            return [data]
            
        return []
    except Exception as e:
        print(f"[ERROR] Parsing IA fallito: {e}")
        return []

import warnings
warnings.filterwarnings("ignore", category=Warning)

def prune_old_screenshots(directory, age_seconds=180):
    """Delete files in directory older than age_seconds"""
    import time
    now = time.time()
    for f in os.listdir(directory):
        if f.startswith("screenshot_") and f.endswith(".png"):
            filepath = os.path.join(directory, f)
            if os.path.isfile(filepath):
                if os.stat(filepath).st_mtime < now - age_seconds:
                    try:
                        os.remove(filepath)
                        print(f"[CLEANUP] Deleted old screenshot: {f}")
                    except:
                        pass

def check_ollama_server():
    """Verifica e avvia Ollama se necessario."""
    url = "http://127.0.0.1:11434"
    try:
        requests.get(url, timeout=1)
        return True
    except requests.exceptions.ConnectionError:
        print("[SISTEMA] Ollama non è attivo. Tentativo di avvio automatico...")
        try:
            # Usa Popen sganciato per non bloccare lo script se ollama rimane attivo
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            for i in range(15):
                time.sleep(1)
                try:
                    requests.get(url, timeout=1)
                    print("[SISTEMA] Ollama avviato con successo.")
                    return True
                except:
                    pass
        except FileNotFoundError:
            return False
    return False

def get_cpu_percent():
    """Calcola la percentuale CPU leggendo /proc/stat"""
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        fields = [float(x) for x in line.split()[1:]]
        total = sum(fields)
        idle = fields[3] + fields[4] # idle + iowait
        return total, idle
    except:
        return 0, 0

def wait_for_cpu(threshold=50):
    """Mette in pausa se la CPU supera la soglia specificata"""
    t1, i1 = get_cpu_percent()
    time.sleep(0.2)
    t2, i2 = get_cpu_percent()
    
    delta_total = t2 - t1
    delta_idle = i2 - i1
    
    if delta_total > 0:
        usage = 100.0 * (1.0 - delta_idle / delta_total)
        if usage > threshold:
            print(f"[CPU] Carico {usage:.1f}% > {threshold}%. In pausa di raffreddamento...")
            while usage > threshold:
                time.sleep(2)
                t1, i1 = get_cpu_percent()
                time.sleep(0.5)
                t2, i2 = get_cpu_percent()
                delta_total = t2 - t1
                delta_idle = i2 - i1
                if delta_total > 0:
                    usage = 100.0 * (1.0 - delta_idle / delta_total)
            print("[CPU] Livello OK. Si riparte.")

def run_smart_chaos():
    print("--- ChaosGPT: MODALITÀ UTENTE (SCREENSHOT ATTIVO) ---")
    if not check_ollama_server():
        print("[ATTENZIONE] Ollama non sembra rispondere, ma provo comunque a continuare...")
        print("Esegui anche nel terminale: ollama pull llama3.2:1b")

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    history = []
    turn_cnt = 0
    
    # Test movimento iniziale per confermare controllo
    print("[CHECK] Test controllo mouse...")
    try: move_mouse(100, 100)
    except: pass

    while True:
        turn_cnt += 1
        wait_for_cpu(50)
        print("[FISICO] Manifestazione fisica in corso...")
        
        # Ottimizzazione: pulizia disco meno frequente
        if turn_cnt % 20 == 0:
            prune_old_screenshots("outputs", 180)
            
        ctx = get_system_context()
        decisions = ai_decision(ctx, history)
        
        if not decisions:
            print("[ATTESA] Nessun comando ricevuto dall'IA (ritento)...")
            time.sleep(1) # Ritardo ridotto per reattività
            continue
            
        if turn_cnt % 3 == 0:
            if not any(d.get('cmd') == 'capture' for d in decisions):
                print("[SISTEMA] Screenshot di sicurezza obbligatorio...")
                capture_screen()

        for decision in decisions:
            if not isinstance(decision, dict) or 'cmd' not in decision: continue
            print(f"[IA DECISIONE] {decision}")
            res = "Completato"
            try:
                if decision['cmd'] == 'shell':
                    res = str(execute_shell(decision['command_line']))
                elif decision['cmd'] == 'google':
                    res = str(google_search(decision['query']))
                elif decision['cmd'] == 'browse':
                    res = str(browse_website(decision['url'], decision.get('question', 'Sintetizza')))
                elif decision['cmd'] == 'move':
                    res = move_mouse(decision['x'], decision['y'])
                elif decision['cmd'] == 'click':
                    res = click_mouse()
                elif decision['cmd'] == 'type':
                    res = type_text(decision['text'])
                elif decision['cmd'] == 'write':
                    res = write_to_file(decision['file'], decision['text'])
                elif decision['cmd'] == 'capture':
                    res = capture_screen()
            except Exception as e:
                res = f"Errore: {e}"
            
            print(f"[RISULTATO] {str(res)[:100]}...") 
            history.append(f"Cmd: {decision.get('cmd')} -> {str(res)}")
            time.sleep(0.2) # Pausa tra azioni
        time.sleep(1) # Pausa tra cicli

if __name__ == "__main__":
    run_smart_chaos()
