import json
import os

OUTPUT_FILE = 'modello/dataset_low_level.jsonl'

def genera_dataset_low_level():
    print("\n--- GENERATORE DATASET LOW-LEVEL (Assembly, C, BIOS) ---")
    
    dataset = [
        # ASSEMBLY X86
        {
            "istruzione": "Spiega come funziona lo stack in Assembly x86 e scrivi un esempio di PUSH/POP.",
            "linguaggio": "Assembly x86",
            "codice": "push eax ; Salva il registro EAX nello stack\npop ebx  ; Recupera il valore e lo mette in EBX",
            "spiegazione": "Lo stack è una struttura LIFO (Last-In-First-Out). PUSH decrementa ESP e scrive i dati, POP legge i dati e incrementa ESP."
        },
        # C SYSTEM PROGRAMMING
        {
            "istruzione": "Scrivi una funzione in C per leggere direttamente un indirizzo di memoria usando i puntatori.",
            "linguaggio": "C",
            "codice": "unsigned int *ptr = (unsigned int *)0x12345678;\nunsigned int value = *ptr;",
            "spiegazione": "In C, i puntatori permettono l'accesso diretto alla memoria fisica, essenziale per la scrittura di driver e BIOS."
        },
        # BIOS / BOOTLOADER
        {
            "istruzione": "Descrivi la struttura di un Master Boot Record (MBR) e il suo ruolo nel BIOS.",
            "linguaggio": "Concetto BIOS",
            "codice": "Settore 0 (512 byte): [Codice Boot] [Tabella Partizioni] [Firma 0x55AA]",
            "spiegazione": "Il BIOS carica i primi 512 byte del disco in memoria all'indirizzo 0x7C00 e li esegue. Se gli ultimi due byte sono 0x55AA, il settore è considerato avviabile."
        },
        # INTERRUPTS
        {
            "istruzione": "Come si chiama un'interruzione del BIOS per stampare un carattere in Real Mode?",
            "linguaggio": "Assembly",
            "codice": "mov ah, 0x0E ; Funzione Teletype\nmov al, 'A'  ; Carattere da stampare\nint 0x10     ; Video Service Interrupt",
            "spiegazione": "Le interruzioni BIOS sono il modo standard con cui il codice low-level comunica con l'hardware prima del caricamento del SO."
        }
    ]

    # Aggiungiamo anche esempi di shellcode reali (che sono Assembly puro) presi dal lavoro di prima
    # (Simulazione di estrazione)
    
    os.makedirs("modello", exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"\n[OK] Dataset Low-Level completato!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Esempi inseriti: {len(dataset)}")

if __name__ == "__main__":
    genera_dataset_low_level()
