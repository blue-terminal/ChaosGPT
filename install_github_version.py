import subprocess

def estrai_sorgente_modello(nome_modello):
    print(f"--- Estrazione Sorgente (Modelfile) di {nome_modello} ---")
    try:
        # Avviamo ollama se è spento (necessario per il comando show)
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(2)
        
        # Estraiamo il modelfile
        res = subprocess.run(["ollama", "show", "--modelfile", nome_modello], capture_output=True, text=True)
        print(res.stdout)
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    estrai_sorgente_modello("llama-lexi-uncensored:latest")
