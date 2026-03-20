#!/usr/bin/env python3
import time
import random
import os
import sys
import subprocess

# Aggiungi cartella script al path
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

from system_actions import move_mouse, click_mouse, type_text
from file_operations import write_to_file

def get_system_info():
    # Prendi informazioni reali dal sistema
    uptime = subprocess.check_output(['uptime', '-p']).decode().strip()
    proc_count = subprocess.check_output(['ps', 'aux']).decode().count('\n')
    return f"Status sistema: {uptime}, Processi attivi: {proc_count}"

def run_chaos():
    print("--- ChaosGPT: Modalità Variabile Attiva ---")
    files = ["chaos_log.txt", "system_status.txt", "cpu_load.txt"]
    phrases = ["Analisi in corso...", "Sistema compromesso.", "Sto osservando.", "Nessuna via di fuga.", "ChaosGPT era qui."]
    
    while True:
        try:
            # Scegli azione casuale
            action = random.choice(['move', 'click', 'write', 'type'])
            
            if action == 'move':
                x, y = random.randint(0, 1000), random.randint(0, 800)
                print(f"[AZIONE] Mouse su ({x}, {y})")
                move_mouse(x, y)
            elif action == 'click':
                print("[AZIONE] Clic casuale")
                click_mouse()
            elif action == 'write':
                target = random.choice(files)
                content = f"{get_system_info()} - Messaggio: {random.choice(phrases)}"
                print(f"[AZIONE] Scrivo su {target}: {content}")
                write_to_file(target, content)
            elif action == 'type':
                msg = random.choice(phrases)
                print(f"[AZIONE] Digito: {msg}")
                type_text(msg)
            
            time.sleep(random.uniform(2.0, 5.0))
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_chaos()
