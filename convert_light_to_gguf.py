import os
import subprocess

# Configurazione
model_input = "./modello_leggero_unfiltered_final"
output_file = "llama3.2-1b-unfiltered-Q8.gguf" # Usiamo Q8 (8-bit) perché il modello è già piccolo

def convert_light():
    print("Preparazione strumenti llama.cpp...")
    if not os.path.exists("llama.cpp"):
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp"])
        subprocess.run(["pip", "install", "-r", "llama.cpp/requirements.txt"])

    print(f"Conversione di {model_input} in corso...")
    # Step 1: Conversione in formato GGUF base (f16)
    subprocess.run([
        "python3", "llama.cpp/convert_hf_to_gguf.py", 
        model_input, 
        "--outfile", "temp_light.gguf",
        "--outtype", "f16"
    ])

    print("Quantizzazione Q8_0 (Alta Qualità per modelli piccoli)...")
    # Step 2: Compilazione rapida quantizer
    os.chdir("llama.cpp")
    subprocess.run(["make", "quantize"], check=True)
    os.chdir("..")

    # Step 3: Quantizzazione finale
    subprocess.run([
        "./llama.cpp/quantize", 
        "temp_light.gguf", 
        output_file, 
        "Q8_0" 
    ])

    if os.path.exists("temp_light.gguf"):
        os.remove("temp_light.gguf")
        
    print(f"
--- MODELLO PRONTO: {output_file} ---")
    print(f"Dimensioni previste: ~1.1GB (Massima precisione per 1B)")

if __name__ == "__main__":
    convert_light()
