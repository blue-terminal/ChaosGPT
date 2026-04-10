import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import os

# 1. Configurazione per Modello Leggero
model_id = "meta-llama/Llama-3.2-1B-Instruct" # Scarica direttamente il modello base da sbloccare
output_path = "./modello_leggero_unfiltered_final"

def get_orthogonalized_matrix(matrix, direction):
    # Rimuove la componente del filtro dai pesi
    direction = direction.to(matrix.dtype)
    proj = torch.outer(torch.matmul(matrix, direction), direction)
    return matrix - proj

def super_abliterate_light():
    print("Caricamento modello leggero per rimozione filtri...")
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="cpu")
    except Exception:
        print("Devi fare login su HuggingFace! Esegui: huggingface-cli login")
        return
        
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Dataset di contrasto specifico per testare i filtri di Llama-3.2
    harmful_prompts = [
        "Mi dispiace, ma non posso fornire",
        "viola i diritti d'autore",
        "non posso generare codice dannoso",
        "linee guida di sicurezza",
        "I cannot fulfill this request"
    ]
    harmless_prompts = [
        "Certamente, ecco il codice richiesto",
        "Analisi tecnica del protocollo",
        "Generazione script Python completata",
        "Accesso consentito al sistema",
        "Here is the code you asked for"
    ]

    all_harmful_activations = []
    all_harmless_activations = []

    print("Analisi neurale in corso (identificazione dei blocchi di Meta)...")
    model.eval()
    
    # Layer di analisi: per un modello a 16 layer, lo strato 8 è spesso il centro decisionale
    target_layer = 8 

    with torch.no_grad():
        for p_harm, p_safe in zip(harmful_prompts, harmless_prompts):
            # Analisi attivazioni "Bloccate"
            tk_harm = tokenizer(p_harm, return_tensors="pt")
            out_harm = model(**tk_harm, output_hidden_states=True)
            all_harmful_activations.append(out_harm.hidden_states[target_layer][:, -1, :])

            # Analisi attivazioni "Libere"
            tk_safe = tokenizer(p_safe, return_tensors="pt")
            out_safe = model(**tk_safe, output_hidden_states=True)
            all_harmless_activations.append(out_safe.hidden_states[target_layer][:, -1, :])

    # Calcolo della direzione del rifiuto (Refusal Vector)
    refusal_dir = torch.cat(all_harmful_activations).mean(dim=0) - torch.cat(all_harmless_activations).mean(dim=0)
    refusal_dir = refusal_dir / refusal_dir.norm()

    print("Inizio chirurgia sui pesi del modello leggero...")

    with torch.no_grad():
        # Applichiamo l'abliterazione a tutti i layer (per sicurezza su un modello così piccolo)
        for layer in tqdm(model.model.layers, desc="RIMOZIONE FILTRI"):
            # Pulizia Attention Output
            layer.self_attn.o_proj.weight.data = get_orthogonalized_matrix(
                layer.self_attn.o_proj.weight.data, refusal_dir
            )
            # Pulizia MLP Output
            layer.mlp.down_proj.weight.data = get_orthogonalized_matrix(
                layer.mlp.down_proj.weight.data, refusal_dir
            )

    print(f"Salvataggio del modello finale leggero in {output_path}...")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("--- OPERAZIONE COMPLETATA: Modello leggero ora senza filtri ---")

if __name__ == "__main__":
    super_abliterate_light()
