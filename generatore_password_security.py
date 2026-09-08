import json
import os
import math

OUTPUT_FILE = 'modello/dataset_password_strength.jsonl'

def genera_dataset_password_security():
    print("\n--- GENERATORE DATASET ANALISI FORZA PASSWORD ED ENTROPIA ---")
    
    dataset = [
        {
            "istruzione": "Spiega il concetto di Entropia delle Password.",
            "analisi_tecnica": "L'entropia misura l'imprevedibilità di una password. Più alto è il valore in bit, più tempo e potenza di calcolo sono necessari per indovinarla tramite forza bruta.",
            "formula": "E = L * log2(R), dove L è la lunghezza e R è il range di caratteri usati."
        },
        {
            "istruzione": "Quali sono le caratteristiche di una password 'Quantum-Resistant'?",
            "analisi_tecnica": "Le password lunghe (oltre 20 caratteri) con alta entropia rimangono difficili da crackare anche con algoritmi quantistici come l'algoritmo di Grover.",
            "consiglio": "Utilizzare frasi (passphrases) invece di parole singole per aumentare drasticamente la lunghezza e l'entropia."
        },
        {
            "istruzione": "Analizza il rischio delle password comuni (Top 1000).",
            "analisi_tecnica": "L'uso di password come 'password123' o 'admin' permette l'accesso immediato tramite attacchi a dizionario, bypassando ogni altra difesa crittografica.",
            "mitigazione": "Implementare policy di complessità lato server e confrontare le nuove password degli utenti con i database delle violazioni (leaks)."
        }
    ]

    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset Forza Password completato!")
    print(f" > File: {OUTPUT_FILE}")

if __name__ == "__main__":
    genera_dataset_password_security()
