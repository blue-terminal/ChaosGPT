import os
import subprocess

# 1. Configurazione
model_path = "./modello_unfiltered_final"
output_file = "modello_unfiltered_Q4_K_M.gguf" # Versione quantizzata (best balance)

def setup_and_convert():
    print("Preparazione strumenti di conversione (llama.cpp)...")
    if not os.path.exists("llama.cpp"):
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp"])
        subprocess.run(["pip", "install", "-r", "llama.cpp/requirements.txt"])

    print(f"Conversione di {model_path} in formato GGUF...")
    # Conversione iniziale in FP16 GGUF
    subprocess.run([
        "python3", "llama.cpp/convert_hf_to_gguf.py", 
        model_path, 
        "--outfile", "temp_f16.gguf",
        "--outtype", "f16"
    ])

    print("Quantizzazione a 4-bit (Q4_K_M) per massima velocità su Intel...")
    # Compilazione veloce di llama.cpp per la quantizzazione
    os.chdir("llama.cpp")
    subprocess.run(["make", "quantize"], check=True)
    os.chdir("..")

    # Quantizzazione finale
    subprocess.run([
        "./llama.cpp/quantize", 
        "temp_f16.gguf", 
        output_file, 
        "Q4_K_M"
    ])

    # Pulizia
    if os.path.exists("temp_f16.gguf"):
        os.remove("temp_f16.gguf")
        
    print(f"
FATTO! Il tuo modello senza filtri è pronto: {output_file}")
    print("Puoi caricarlo su Ollama o usarlo con llama.cpp.")

if __name__ == "__main__":
    setup_and_convert()
