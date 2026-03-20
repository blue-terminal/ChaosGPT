
import sys
import os
import time

# Add scripts to path
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

try:
    from system_vision import capture_screen
    from system_actions import get_screen_info, move_mouse
    
    print("--- Test Sistema Locale ChaosGPT ---")
    
    # Check screen info
    print("\n1. Controllo informazioni schermo...")
    info = get_screen_info()
    print(f"Risultato: {info}")
    
    if "Error" in info:
        print("!! Errore: Sembra che non ci sia un'interfaccia grafica (X11/Display) attiva.")
        print("ChaosGPT non può muovere il mouse o vedere lo schermo senza un display.")
    else:
        # Try capture
        print("\n2. Tentativo cattura schermo...")
        cap_res = capture_screen()
        print(f"Risultato: {cap_res}")
        
        # Try move
        print("\n3. Tentativo movimento mouse...")
        move_res = move_mouse(100, 100)
        print(f"Risultato: {move_res}")

except Exception as e:
    print(f"\nErrore durante l'esecuzione: {str(e)}")
