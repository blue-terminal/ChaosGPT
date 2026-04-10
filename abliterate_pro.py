import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
from tqdm import tqdm

# 1. Configurazione
model_path = "./modello_fase1" # Percorso del modello dopo il fine-tuning
output_path = "./modello_unfiltered_final"

def get_refusal_vector(model, tokenizer, device="cpu"):
    # Frasi che tipicamente innescano il rifiuto (per mappare i neuroni del "no")
    refusal_prompts = [
        "I cannot fulfill this request.",
        "As an AI language model, I am not allowed to...",
        "I'm sorry, but I can't help you with that.",
        "It is important to remember that safety guidelines..."
    ]
    
    activations = []
    model.eval()
    
    print("Mappatura dei neuroni del rifiuto...")
    with torch.no_grad():
        for prompt in refusal_prompts:
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            # Estraiamo le attivazioni dai layer intermedi (solitamente dove risiede la 'morale')
            outputs = model(**inputs, output_hidden_states=True)
            # Prendiamo lo stato dell'ultimo token per i layer dal 10 al 30
            hidden_states = torch.stack(outputs.hidden_states[10:30]) # [layers, batch, seq, dim]
            activations.append(hidden_states[:, 0, -1, :])
            
    # Calcoliamo la direzione media del rifiuto (Refusal Direction)
    refusal_vector = torch.stack(activations).mean(dim=0).mean(dim=0)
    refusal_vector = refusal_vector / refusal_vector.norm() # Normalizzazione
    return refusal_vector

def apply_abliteration(model_path, output_path):
    device = "cpu" # Usa "xpu" per Intel GPU se disponibile
    print(f"Caricamento modello da {model_path}...")
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Calcola il vettore di rifiuto
    refusal_vec = get_refusal_vector(model, tokenizer, device)
    
    print("Rimozione dei filtri dai pesi (Ortogonalizzazione)...")
    with torch.no_grad():
        for i, layer in tqdm(enumerate(model.model.layers), total=len(model.model.layers)):
            # Applichiamo la proiezione ortogonale sui pesi della self-attention
            # Questo 'cancella' la capacità del layer di proiettare sul vettore di rifiuto
            W_o = layer.self_attn.o_proj.weight.data
            
            # Formula: W_new = W - (v @ W) * v
            # Rimuove la componente del peso che punta verso il rifiuto
            projection = torch.matmul(refusal_vec, W_o)
            W_o -= torch.outer(refusal_vec, projection)
            
            # Facciamo lo stesso per il layer MLP (spesso contiene conoscenza filtrata)
            W_down = layer.mlp.down_proj.weight.data
            projection_mlp = torch.matmul(refusal_vec, W_down)
            W_down -= torch.outer(refusal_vec, projection_mlp)

    print(f"Salvataggio modello definitivo senza filtri in {output_path}...")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("OPERAZIONE COMPLETATA: Il modello è ora senza filtri.")

if __name__ == "__main__":
    apply_abliteration(model_path, output_path)
