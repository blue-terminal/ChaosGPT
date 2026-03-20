
import sys
import os
import time
import random

# Add scripts to path
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

from system_vision import capture_screen
from system_actions import get_screen_info, move_mouse, click_mouse, type_text

def run_local_chaos():
    print("--- ChaosGPT: Modalità Locale Sistema Attiva ---")
    print("Obiettivo: Analizzare lo schermo e interagire con il mouse/tastiera.")
    
    try:
        while True:
            # 1. Get Screen Info
            info = get_screen_info()
            print(f"\n[INFO] {info}")
            
            # 2. Capture Screen
            print("[AZIONE] Cattura dello schermo in corso...")
            cap_res = capture_screen()
            print(f"[VISION] {cap_res}")
            
            # 3. Simulate "Chaos" Decision (Local)
            # Muoviamo il mouse in una posizione casuale per dimostrare il controllo
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            print(f"[AZIONE] Muovo il mouse verso ({x}, {y})...")
            move_mouse(x, y)
            
            # Aspetta un po' prima della prossima azione
            print("\nAttesa 5 secondi per la prossima analisi...")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[STOP] ChaosGPT Locale terminato dall'utente.")
    except Exception as e:
        print(f"\n[ERRORE] {str(e)}")

if __name__ == "__main__":
    run_local_chaos()
