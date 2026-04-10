import os
from huggingface_hub import snapshot_download

# 1. Configurazione
repo_id = "meta-llama/Llama-3.2-1B"
local_dir = "./llama-3.2-1b-base"

def setup_model():
    print(f"Sto scaricando i pesi di {repo_id} da Hugging Face...")
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            ignore_patterns=["*.pth", "*.bin"] # Scarichiamo solo i safetensors (più sicuri e veloci)
        )
        print(f"Modello scaricato con successo in: {local_dir}")
        return True
    except Exception as e:
        print(f"Errore durante lo scaricamento: {e}")
        print("Assicurati di aver accettato i termini su Hugging Face e di aver fatto 'huggingface-cli login'.")
        return False

if __name__ == "__main__":
    if setup_model():
        print("
Ora puoi lanciare l'addestramento con:")
        print("python3 train_lightweight.py")
        # Aggiorniamo il percorso nello script di training
        # (Opzionale: posso farlo io se vuoi procedere subito)
