import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from trl import SFTTrainer
import os

# Configurazione - Cambia il modello base qui
# Esempi: "meta-llama/Meta-Llama-3-8B", "mistralai/Mistral-7B-v0.1"
model_id = "mistralai/Mistral-7B-v0.1" 

# 1. Caricamento Modello in 4-bit (Risparmio VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

print(f"Caricamento modello: {model_id}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model = prepare_model_for_kbit_training(model)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 2. Configurazione LoRA
peft_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. Caricamento Dataset
dataset = load_dataset("json", data_files="dataset_example.jsonl", split="train")

# Funzione per formattare il prompt
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"### Istruzione:
{example['instruction'][i]}

### Risposta:
{example['output'][i]}"
        output_texts.append(text)
    return output_texts

# 4. Configurazione Training
training_args = TrainingArguments(
    output_dir="./modello_unfiltered",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=1,
    num_train_epochs=3,
    save_steps=100,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    optim="paged_adamw_8bit",
    report_to="none"
)

# 5. Avvio SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    formatting_func=formatting_prompts_func,
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_args,
)

print("Inizio addestramento...")
trainer.train()

# Salvataggio
trainer.save_model("./modello_unfiltered_final")
print("Addestramento completato e modello salvato.")
