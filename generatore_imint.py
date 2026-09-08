import json
import os

OUTPUT_FILE = 'modello/dataset_imint_osint.jsonl'

def genera_dataset_imint():
    print("\n--- GENERATORE DATASET IMINT & OSINT FORENSICS (Identificazione Immagini) ---")
    
    dataset = [
        {
            "istruzione": "Come si esegue l'analisi forense dei metadati EXIF di una foto?",
            "dominio": "IMINT / Forensics",
            "tecnica": "Utilizzo di strumenti come Exiftool per leggere i tag nascosti. I dati GPS (latitudine/longitudine) possono localizzare la persona con precisione di pochi metri.",
            "strumenti": "Exiftool, Forensically, JPEGsnoop."
        },
        {
            "istruzione": "Tecniche per identificare una persona tramite Reverse Image Search.",
            "dominio": "OSINT",
            "tecnica": "Caricamento dell'immagine su motori come Google Lens, Yandex o PimEyes per trovare occorrenze della stessa faccia su siti web, articoli di stampa o social media.",
            "analisi": "Il confronto biometrico automatizzato permette di identificare la persona anche se la foto è stata scattata in contesti diversi."
        },
        {
            "istruzione": "Identificazione di una persona tramite 'Reflection Analysis'.",
            "dominio": "IMINT Avanzato",
            "tecnica": "Analisi dei riflessi presenti in specchi, vetrate o persino nelle cornee del soggetto per ricostruire l'ambiente circostante e identificare il luogo o chi ha scattato la foto.",
            "forensics": "Uso di filtri di contrasto ed enhancement per rendere leggibili i dettagli nei riflessi."
        },
        {
            "istruzione": "Cos'è il 'Face Search' nei database OSINT?",
            "dominio": "Digital Identity",
            "tecnica": "L'uso di motori di ricerca facciale che scansionano i profili social pubblici e i database di leak per associare un volto a un nome e cognome o a un nickname.",
            "privacy": "Queste tecniche sono fondamentali per l'attribuzione di attività cyber a individui reali."
        }
    ]

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset IMINT & OSINT completato!")
    print(f" > File: {OUTPUT_FILE}")

if __name__ == "__main__":
    genera_dataset_imint()
