import struct
import os
import re

# Percorso del blob Lexi Uncensored
path = "/home/blue-terinal/.ollama/models/blobs/sha256-678838a50278f9c62c378bdb328b1ef5b774af50fce7b32dbf09573e597515b7"
output_file = "modello/metadati_modello.txt"

def decripta_e_salva():
    if not os.path.exists(path):
        print("File modello non trovato!")
        return
        
    os.makedirs("modello", exist_ok=True)
        
    with open(path, "rb") as f:
        magic = f.read(4)
        if magic != b"GGUF":
            print(f"Il file non è un GGUF (Magic: {magic})")
            return
            
        version = struct.unpack("<I", f.read(4))[0]
        tensor_count = struct.unpack("<Q", f.read(8))[0]
        metadata_count = struct.unpack("<Q", f.read(8))[0]
        
        report = f"--- REPORT DECRITTAZIONE MODELLO ---\n"
        report += f"Magic: {magic.decode()}\n"
        report += f"Versione GGUF: {version}\n"
        report += f"Neuroni (Tensori): {tensor_count}\n"
        report += f"Metadati: {metadata_count}\n\n"
        
        # Estraiamo le stringhe per capire l'architettura
        f.seek(0)
        dati = f.read(30000)
        strings = re.findall(b"[\x20-\x7E]{5,}", dati)
        
        report += "--- ARCHITETTURA E VERSIONI RILEVATE ---\n"
        per_testo = set()
        for s in strings:
            try:
                txt = s.decode('ascii')
                if any(x in txt.lower() for x in ['llama', 'version', 'model', 'lexi', 'author']):
                    per_testo.add(txt)
            except: pass
        
        for item in sorted(per_testo):
            report += f" > {item}\n"

    # Salvataggio su file
    with open(output_file, "w") as out:
        out.write(report)
    
    print(f"Decrittazione completata! Risultato salvato in: {output_file}")
    print("\nAnteprima Report:")
    print(report[:500] + "...")

if __name__ == "__main__":
    decripta_e_salva()
