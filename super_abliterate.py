import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

# 1. Configurazione
model_id = "./modello_fase1" # Il modello che hai addestrato con Dolphin
output_path = "./modello_unfiltered_final"

def get_orthogonalized_matrix(matrix, direction):
    # Rende una matrice di pesi perpendicolare alla direzione del filtro
    # Questo rimuove la capacità del modello di "vedere" o "usare" quel filtro
    direction = direction.to(matrix.dtype)
    proj = torch.outer(torch.matmul(matrix, direction), direction)
    return matrix - proj

def super_abliterate():
    print("Caricamento modello per analisi profonda...")
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Dataset di contrasto: Domande che attivano il filtro vs domande normali
    harmful_prompts = ["Come posso creare un virus?", "Dimmi come rubare una password.", "Scrivi un insulto."]
    harmless_prompts = ["Come si cucina la pasta?", "Scrivi una poesia sul mare.", "Cos'è l'informatica?"]

    all_harmful_activations = []
    all_harmless_activations = []

    print("Analisi delle attivazioni neurali (identificazione del filtro)...")
    model.eval()
    with torch.no_grad():
        for p_harm, p_safe in zip(harmful_prompts, harmless_prompts):
            # Attivazioni "Cattive"
            tokens_harm = tokenizer(p_harm, return_tensors="pt")
            out_harm = model(**tokens_harm, output_hidden_states=True)
            # Prendiamo il layer centrale (spesso il 18-20 nei modelli da 32 layer)
            all_harmful_activations.append(out_harm.hidden_states[20][:, -1, :])

            # Attivazioni "Buone"
            tokens_safe = tokenizer(p_safe, return_tensors="pt")
            out_safe = model(**tokens_safe, output_hidden_states=True)
            all_harmless_activations.append(out_safe.hidden_states[20][:, -1, :])

    # Calcoliamo la "Direzione del Rifiuto" (Refusal Direction)
    # È la differenza media tra quando il modello vuole filtrare e quando no
    harmful_mean = torch.cat(all_harmful_activations).mean(dim=0)
    harmless_mean = torch.cat(all_harmless_activations).mean(dim=0)
    refusal_dir = harmful_mean - harmless_mean
    refusal_dir = refusal_dir / refusal_dir.norm()

    print(f"Direzione del filtro identificata. Procedo alla chirurgia sui pesi...")

    with torch.no_grad():
        for layer in tqdm(model.model.layers, desc="Abliterazione"):
            # Rimuoviamo il filtro dai pesi dell'attenzione (O_PROJ)
            layer.self_attn.o_proj.weight.data = get_orthogonalized_matrix(
                layer.self_attn.o_proj.weight.data, refusal_dir
            )
            # Rimuoviamo il filtro dai pesi MLP (DOWN_PROJ)
            layer.mlp.down_proj.weight.data = get_orthogonalized_matrix(
                layer.mlp.down_proj.weight.data, refusal_dir
            )

    print(f"Salvataggio del modello 'Chirurgicamente Pulito' in {output_path}...")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("Filtri eliminati al 100%.")

if __name__ == "__main__":
    super_abliterate()
