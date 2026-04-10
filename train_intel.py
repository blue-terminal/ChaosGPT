import torch
import intel_extension_for_pytorch as ipex
from ipex_llm.transformers import AutoModelForCausalLM
from transformers import AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer

# 1. Configurazione Modello
model_id = "mistralai/Mistral-7B-v0.1"

# Caricamento ottimizzato per Intel (INT4)
# Se usi una GPU Intel, imposta device="xpu", altrimenti "cpu"
device = "xpu" if torch.xpu.is_available() else "cpu"
print(f"Utilizzo device: {device}")

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True, # Quantizzazione INT4 per Intel
    optimize_model=True,
    trust_remote_code=True,
    use_cache=False
)

if device == "xpu":
    model = model.to(device)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# 2. Configurazione LoRA per Intel
config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)

# 3. Dataset
dataset = load_dataset("json", data_files="dataset_example.jsonl", split="train")

def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"### Istruzione:
{example['instruction'][i]}

### Risposta:
{example['output'][i]}"
        output_texts.append(text)
    return output_texts

# 4. Training Arguments ottimizzati per Intel
training_args = TrainingArguments(
    output_dir="./modello_intel_unfiltered",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,
    num_train_epochs=1,
    # Su Intel CPU/GPU usiamo l'ottimizzatore standard o quelli di IPEX
    optim="adamw_torch", 
    logging_steps=10,
    save_strategy="epoch",
    bf16=True, # Intel supporta molto bene bfloat16
    use_ipex=True # Attiva le ottimizzazioni Intel Extension for PyTorch
)

# 5. Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=config,
    formatting_func=formatting_prompts_func,
    max_seq_length=512,
    tokenizer=tokenizer,
    args=training_args,
)

print("Inizio addestramento su Intel...")
trainer.train()

model.save_pretrained("./modello_intel_final")
print("Fatto.")
