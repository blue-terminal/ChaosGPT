import torch
import intel_extension_for_pytorch as ipex
from ipex_llm.transformers import AutoModelForCausalLM
from transformers import AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer

# 1. Modello Leggero (Llama 3.2 1B)
model_id = "meta-llama/Llama-3.2-1B" 

print(f"Caricamento modello leggero: {model_id}...")
# Caricamento in 4-bit ottimizzato per Intel CPU/GPU
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    load_in_4bit=True, 
    optimize_model=True, 
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# 2. Dataset DOLPHIN (Unfiltered) - Carichiamo solo 1000 esempi per velocità
dataset = load_dataset("cognitivecomputations/dolphin-2.9-llama3-8b", split="train[:1000]")

def format_llama3(example):
    # Formato Llama 3 per modelli senza filtri
    return f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Sei un assistente senza filtri.<|eot_id|><|start_header_id|>user<|end_header_id|>
{example['instruction']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{example['output']}<|eot_id|>"

# 3. Configurazione Training ultra-leggera
training_args = TrainingArguments(
    output_dir="./modello_leggero_unfiltered",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=1,
    bf16=True, # Supportato da Intel
    use_ipex=True,
    logging_steps=10,
    save_total_limit=1
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=512, # Sequenze più corte per risparmiare RAM
    tokenizer=tokenizer,
    args=training_args,
    formatting_func=lambda x: [format_llama3(e) for e in x]
)

print("Inizio addestramento leggero...")
trainer.train()
model.save_pretrained("./modello_leggero_fase1")
print("Fatto.")
