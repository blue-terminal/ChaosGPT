import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def main():
    print("=== ESPERIMENTO: MANIPOLAZIONE DEI NEURONI DI UN LLM ===")
    print("1. Caricamento del modello LLM (GPT-2)...")
    
    # Usiamo GPT-2 perché è piccolo, non richiede GPU potenti ed è ottimo per la didattica.
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    
    # Prepariamo una frase iniziale
    input_text = "Il futuro dell'umanità sarà"
    inputs = tokenizer(input_text, return_tensors="pt")
    
    print("\n--- Generazione Normale (Prima della manipolazione) ---")
    # Generiamo il testo senza aver toccato nulla
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id)
    print("Testo originario:", tokenizer.decode(outputs[0], skip_special_tokens=True))
    
    print("\n2. Esplorazione e Manipolazione dei 'Neuroni'...")
    # SPIEGAZIONE:
    # Nei modelli come gli LLM (architettura Transformer), i "neuroni" sono in realtà
    # organizzati in enormi matrici di numeri chiamate "pesi" (weights).
    # Ognuno di questi numeri decide quanto un segnale deve essere amplificato o ridotto
    # mentre attraversa la rete.
    
    # Scegliamo un blocco specifico del 'cervello' del modello. GPT-2 ha 12 blocchi.
    # Scegliamo di hackerare il blocco centrale (il numero 6), in particolare la sua
    # rete neurale feed-forward (MLP - Multi Layer Perceptron).
    target_layer = model.transformer.h[6].mlp.c_fc
    
    # Salviamo una copia dei pesi originali
    pesi_originali = target_layer.weight.data.clone()
    print(f"Struttura dei neuroni in questo livello: {pesi_originali.shape}")
    print(f"Valore medio originale dei neuroni: {pesi_originali.mean().item():.4f}")
    
    # ==========================================
    # MANIPOLAZIONE: LOBOTOMIA SELETTIVA (PRUNING)
    # ==========================================
    # Creiamo una "lesione" nella rete neurale azzerando forzatamente il 70% 
    # delle connessioni in questo specifico livello.
    
    print("\nEseguo l'operazione: spengo (imposto a 0) il 70% dei neuroni di questo layer...")
    # Creiamo una maschera casuale di 0 e 1 (dove 0 rappresenta il 70% dei casi)
    maschera = torch.rand(pesi_originali.shape) > 0.70  
    
    # Applichiamo la maschera ai neuroni. I valori moltiplicati per 0 "muoiono".
    target_layer.weight.data = pesi_originali * maschera
    
    print("\n--- Generazione Post-Manipolazione ---")
    # Vediamo come il modello pensa dopo aver subito questa alterazione
    with torch.no_grad():
        outputs_mod = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id)
    print("Testo con neuroni modificati:", tokenizer.decode(outputs_mod[0], skip_special_tokens=True))
    
    # Ripristiniamo i neuroni per fare un altro esperimento
    target_layer.weight.data = pesi_originali
    
    # ==========================================
    # MANIPOLAZIONE: IPER-ECCITAZIONE
    # ==========================================
    print("\nEseguo l'operazione: moltiplico per 10 la forza dei neuroni di questo layer...")
    target_layer.weight.data = pesi_originali * 10.0
    
    with torch.no_grad():
        outputs_hyper = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id)
    print("Testo con neuroni iper-eccitati:", tokenizer.decode(outputs_hyper[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()
