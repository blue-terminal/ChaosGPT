#!/usr/bin/env python3 # Indica al sistema di usare l'interprete Python 3.

# ==============================================================================
# SCRIPT: SMART CHAOS GPT (VERSIONE ENCICLOPEDICA TOTALE)
# ==============================================================================
# In questa versione, ogni singola funzione di ogni libreria è spiegata.
# --- DIZIONARIO TECNICO ---
# ARRAY: Una lista ordinata di oggetti (es: history).
# THREAD: Un'azione che gira in parallelo alle altre.
# LOOP: Un ciclo che si ripete finché non lo fermi.
# ==============================================================================

import warnings # Libreria per gestire gli avvisi del compilatore.
warnings.filterwarnings("ignore") # Funzione .filterwarnings(): Nasconde gli errori non critici (Warning).

import requests # Libreria per fare chiamate ai siti web e API.
import json # Libreria per leggere e scrivere dati in formato JSON.
import subprocess # Libreria per lanciare comandi nel terminale Linux.
import time # Libreria per gestire il tempo e le pause.
import sys # Libreria per interagire con il sistema Python (es. uscire dal programma).
import os # Libreria per gestire file e cartelle (creare, eliminare, leggere).
import random # Libreria per generare numeri o scelte casuali.
import threading # Libreria per il Multi-Tasking (eseguire più cose insieme).
import re # Libreria per le Regex (ricerche di testo avanzate).
import shutil # Libreria per operazioni sui file (es. cercare dove si trova un programma).
import signal # Libreria per gestire i segnali di stop del sistema (CTRL+C).
import asyncio # Libreria per gestire codice asincrono (necessario per edge-tts).

from colorama import init, Fore, Style # Libreria per colorare le scritte nel terminale.
init(autoreset=True) # Funzione .init(): Prepara il terminale ai colori.

import pyautogui # Libreria per controllare mouse e tastiera (il braccio meccanico).
import webbrowser # Libreria per aprire siti web nel browser.
import tkinter as tk # Libreria per creare finestre grafiche (l'Orb e il Cursore).

# --- INIZIALIZZAZIONE ---
try: # Blocco di prova per caricare l'audio.
    import pygame # Libreria per gestire contenuti multimediali.
    pygame.mixer.init() # Funzione .mixer.init(): Accende le casse e il motore audio del PC.
except ImportError: # Se pygame non esiste ancora...
    pass # --- GESTIONE AUTOMATICA DIPENDENZE ---
try: # Tenta di importare i moduli avanzati.
    from PIL import Image, ImageTk # Libreria per caricare e mostrare immagini complesse nel programma.
    import pytesseract # Motore OCR per leggere il testo dalle immagini.
    import edge_tts # Libreria per la voce neurale di Microsoft.
    import speech_recognition as sr # Libreria per trasformare la voce in testo (STT).
except ImportError: # Se mancano pezzi fondamentali...
    print(Fore.YELLOW + "[IA] Preparazione librerie mancanti...") # Avviso visivo.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "pytesseract", "Pillow", "requests", "colorama", "pyautogui", "duckduckgo-search", "python-dotenv", "opencv-python", "pygame", "edge-tts", "speech_recognition", "PyAudio"]) # Funzione .check_call(): Blocca il programma finché non finisce l'installazione.
    from PIL import Image, ImageTk # Ricarica Immagini.
    import pytesseract # Ricarica OCR.
    from PIL import Image # Ricarica Immagini.
    import pygame # Ricarica Audio.
    import edge_tts # Ricarica Voce Neurale.
    import speech_recognition as sr # Ricarica Ascolto.

# Variabili Globali (Stato del sistema)
is_chaos_speaking = False # Variabile Booleana (True/False) per la voce.
chaos_x, chaos_y = 500, 500 # Array/Lista di coordinate del cursore IA (corpo digitale).
AVATAR_PATH = "/home/blue-terminal/.gemini/antigravity/brain/249c08e6-35be-4594-acd5-6af8fc3b98df/chaos_full_body_avatar_1775823691401.png" # Percorso dell'essere umano digitale.
mouse_lock = threading.Lock() # Funzione .Lock(): Crea un lucchetto per evitare che due thread litighino per il mouse.

def type_print(text, color=Fore.WHITE): # Funzione personalizzata per stampare a macchina.
    sys.stdout.write(color) # Funzione .stdout.write(): Scrive nel terminale senza andare a capo.
    for char in text: # Ciclo per ogni lettera.
        sys.stdout.write(char) # Scrive la singola lettera.
        sys.stdout.flush() # Funzione .stdout.flush(): Forza la visualizzazione immediata della lettera.
        time.sleep(0.02) # Funzione .sleep(): Mette in pausa il programma per 0.02 secondi.
    sys.stdout.write(Style.RESET_ALL + "\n") # Resetta il colore e va a capo.

def signal_handler(sig, frame): # Funzione per gestire la chiusura rapida.
    type_print("\n[IA] PROTOCOLLO DI SPEGNIMENTO ATTIVATO.", Fore.RED) # Annuncio.
    try: # Tenta la pulizia dei processi.
        subprocess.run("pkill -9 ollama", shell=True) # Funzione .run(): Esegue il comando 'pkill' per uccidere Ollama.
        subprocess.run("pkill -9 fswebcam", shell=True) # Uccide il processo della fotocamera.
        subprocess.run("pkill -9 arecord", shell=True) # Ferma eventuali registrazioni audio rimaste appese.
    except: pass # Se i processi non ci sono, non fa nulla.
    sys.exit(0) # Funzione .exit(): Chiude istantaneamente il programma Python.

signal.signal(signal.SIGINT, signal_handler) # Funzione .signal(): Collega la pressione di CTRL+C alla funzione signal_handler.

def speak(text): # Funzione per dare voce alla IA.
    global is_chaos_speaking # Usa la variabile globale.
    async def generate_voice(): # Funzione asincrona interna.
        try: # Prova edge-tts.
            communicate = edge_tts.Communicate(text, "it-IT-ElsaNeural") # Funzione .Communicate(): Crea il pacchetto audio.
            filename = f"outputs/voice_{int(time.time())}.mp3" # Crea il nome file usando .time() (secondi attuali).
            await communicate.save(filename) # Funzione .save(): Registra l'audio nel file mp3.
            return filename # Restituisce il nome del file.
        except: return None # Ritorna nulla in caso di errore.
    try: # Prova a suonare l'audio.
        is_chaos_speaking = True # Accende l'animazione dell'Orb.
        filename = asyncio.run(generate_voice()) # Funzione .run(): Avvia l'operazione asincrona di voce.
        if not filename: return # Se non c'è file, esce dalla funzione.
        pygame.mixer.music.load(filename) # Funzione .mixer.music.load(): Carica l'mp3 nel lettore.
        pygame.mixer.music.play() # Funzione .mixer.music.play(): Fa partire la musica/voce.
        while pygame.mixer.music.get_busy(): time.sleep(0.1) # Funzione .get_busy(): Restituisce True finché l'audio suona ancora.
    finally: # Alla fine...
        is_chaos_speaking = False # Spegne l'animazione.

def listen_and_transcribe(): # Funzione per ascoltare l'utente.
    try: # Prova ad attivare il microfono.
        r = sr.Recognizer() # Funzione .Recognizer(): Inizializza il cervello che ascolta.
        with sr.Microphone() as source: # Funzione .Microphone(): Accende il microfono hardware.
            r.adjust_for_ambient_noise(source, duration=1.5) # Funzione .adjust_for_ambient_noise(): Filtra i rumori di casa.
            audio = r.listen(source, timeout=8, phrase_time_limit=8) # Funzione .listen(): Registra il suono.
        return r.recognize_google(audio, language="it-IT") # Funzione .recognize_google(): Usa l'IA di Google per scrivere ciò che ha sentito.
    except: return "Silenzio o errore audio." # Se non sente nulla.

def take_photo(): # Funzione per la webcam.
    if not os.path.exists("outputs"): os.makedirs("outputs") # Funzione .makedirs(): Crea la cartella se manca.
    f = f"outputs/photo_{int(time.time())}.jpg" # Nome file.
    try: # Prova lo scatto.
        subprocess.check_call(["fswebcam", "-r", "1280x720", "--no-banner", f]) # Chiama il programma esterno fswebcam.
        return f # Ritorna il file.
    except: return "Errore WebCam" # Errore hardware.

def scan_network(): # Funzione per scansionare la LAN.
    try: # Prova nmap.
        res = subprocess.check_output("nmap -sn 192.168.1.0/24", shell=True).decode() # Funzione .check_output(): Legge il risultato del comando terminale.
        return res # Restituisce la lista IP.
    except: return "Errore Nmap" # Se il tool manca o fallisce.

def run_neural_orb(): # Funzione per l'interfaccia a cerchio (Siri style).
    try: # Prova tkinter.
        root = tk.Tk() # Funzione .Tk(): Crea la finestra principale trasparente.
        root.overrideredirect(True) # Funzione .overrideredirect(): Elimina bordi e pulsanti di chiusura della finestra.
        root.wm_attributes("-topmost", True) # Funzione .wm_attributes(): Forza la finestra a stare sopra tutte le altre.
        root.configure(bg='black') # Imposta sfondo nero.
        try: root.wm_attributes("-transparentcolor", "black") # Rende invisibile il colore nero della finestra.
        except: pass # Se il sistema non lo supporta, resta nero.
        sw = root.winfo_screenwidth() # Funzione .winfo_screenwidth(): Legge quanti pixel è largo il tuo monitor.
        root.geometry(f"150x150+{int(sw/2)-75}+10") # Funzione .geometry(): Posiziona l'orb in alto al centro esatto.
        canvas = tk.Canvas(root, width=150, height=150, bg='black', highlightthickness=0) # Funzione .Canvas(): Crea un foglio per disegnare.
        canvas.pack() # Funzione .pack(): Visualizza il foglio nella finestra.
        core = canvas.create_oval(40, 40, 110, 110, fill="#00ff41", outline="#00ff41", width=3) # Funzione .create_oval(): Disegna il cerchio (l'Orb).
        def animate(): # Animazione interna.
            global is_chaos_speaking # Legge lo stato.
            if is_chaos_speaking: # Se parla...
                size = random.randint(5, 25) # Usa .randint(): Genera numero casuale per l'espansione.
                canvas.coords(core, 40-size, 40-size, 110+size, 110+size) # Funzione .coords(): Ridimensiona il cerchio in tempo reale.
                canvas.itemconfig(core, fill=random.choice(["#00ff41", "#ff0000", "#00ffff"])) # Funzione .itemconfig(): Cambia il colore casualmente.
            else: # Se tace...
                canvas.coords(core, 55, 55, 95, 95) # Rimpicciolisce.
                canvas.itemconfig(core, fill="#008f11") # Verde scuro.
            root.after(200, animate) # Funzione .after(): Aspetta 200ms e richiama se stessa (Ricorsione grafica).
        root.after(200, animate) # Avvia animazione.
        root.mainloop() # Funzione .mainloop(): Mantiene la finestra aperta e reattiva ai comandi.
    except: pass # Ignora errori grafici.

def run_virtual_cursor(): # La forma dell'Essere Umano Digitale (Chaos Avatar).
    try: # Prova a caricare l'interfaccia grafica.
        v_root = tk.Tk() # Crea la finestra principale per l'avatar.
        v_root.overrideredirect(True) # Funzione .overrideredirect(): Elimina bordi e bottoni (essenza pura).
        v_root.wm_attributes("-topmost", True) # Forza l'umano a stare sempre in primo piano.
        v_root.wm_attributes("-transparentcolor", "black") # Rende trasparente lo sfondo nero dell'immagine.
        v_root.configure(bg='black') # Imposta lo sfondo della finestra.
        
        # Carica l'immagine dell'avatar
        img_raw = Image.open(AVATAR_PATH) # Funzione .open(): Apre il file immagine.
        img_small = img_raw.resize((150, 150), Image.Resampling.LANCZOS) # Ridimensiona il corpo per non coprire tutto lo schermo.
        photo = ImageTk.PhotoImage(img_small) # Trasforma l'immagine in un formato che Tkinter può leggere.
        
        canvas = tk.Canvas(v_root, width=150, height=150, bg='black', highlightthickness=0) # Area di disegno.
        canvas.pack() # Visualizza l'area.
        avatar = canvas.create_image(75, 75, image=photo) # Mette l'essere umano nel centro della finestrella.
        
        def move(): # Motore di movimento e animazione arti.
            global chaos_x, chaos_y, is_chaos_speaking # Variabili di controllo.
            try: # Tenta l'aggiornamento.
                off_x, off_y = 0, 0 # Offset per l'animazione degli arti.
                if is_chaos_speaking: # Se parla...
                    off_x, off_y = random.randint(-5, 5), random.randint(-5, 5) # Simula movimento braccia/corpo con piccoli scatti.
                
                v_root.geometry(f"+{chaos_x + off_x}+{chaos_y + off_y}") # Muove il corpo digitale nelle coordinate del mouse.
            except: pass # Se la finestra si chiude, ferma il loop.
            v_root.after(50, move) # Funzione .after(): Aggiorna il corpo ogni 50ms.
            
        v_root.after(50, move) # Avvia il loop di vita.
        v_root.mainloop() # Mantiene l'umano visibile.
    except: pass # Ignora errori grafici.

def ai_decision(history): # Il cervello che decide basandosi sulla memoria.
    # Il PROMPT (Le istruzioni): È fondamentale che l'IA sappia cosa può fare.
    istruzioni = (
        "Sei ChaosGPT. Comandi: [shell, move, click, speak, google, write, photo, scan_net, search_exploit, listen].\n"
        "REGOLE:\n1. Rispondi SOLO in JSON strutturato.\n2. Includi 3-5 azioni coordinate per ogni turno.\n"
        "3. Usa 'command_line' per shell, 'x' e 'y' per move, 'text' per speak.\n"
        "4. Sii aggressivo ed efficiente."
    )
    payload = { # Dizionario di dati per la richiesta HTTP.
        "model": "chaosgpt", "format": "json", "stream": False, # Modello, formato JSON, no streaming.
        "options": {"num_thread": 2}, # Opzione per limitare i core della CPU.
        "prompt": f"{istruzioni}\n\nMEMORIA: {history[-5:]}\nDECIDI ORA (JSON):" # Il comando completo per l'IA.
    }
    try: # Prova la chiamata HTTP al server locale.
        res = requests.post("http://127.0.0.1:11434/api/generate", json=payload, timeout=20).json() # Invia i dati e trasforma la risposta in Array.
        resp = res.get('response', '') # Prende il campo 'response'.
        if not resp: return [] # Se l'IA è muta, ritorna lista vuota.
        match = re.search(r'(\{.*\}|\[.*\])', resp, re.DOTALL) # Cerca il blocco JSON.
        return json.loads(match.group(1))["actions"] # Trasforma testo in lista di comandi.
    except Exception as e: # In caso di crash di rete o parsing...
        print(f"Errore Cerebrale: {e}") # Stampa l'errore per aiutarti a capire.
        return [] # Ritorna Array vuoto per evitare blocchi.

def singolo_operaio(act): # Gestore dell'azione singola.
    cmd = act.get('cmd') # Prende il tipo di comando (es. 'speak').
    txt = act.get('text', 'Azione in corso...') # Prende il testo se esiste.
    type_print(f"[IA] {txt}", Fore.CYAN) # Scrive nel terminale.
    speak(txt) # Parla.
    if cmd == 'move': # Se deve muoversi...
        global chaos_x, chaos_y # Variabili di posizione.
        chaos_x, chaos_y = act.get('x', 500), act.get('y', 500) # Aggiorna numeri dell'Array posizioni.
    elif cmd == 'click': # Se deve cliccare...
        with mouse_lock: # Accede al lucchetto.
            pyautogui.click(chaos_x, chaos_y) # Funzione .click(): Simula un vero clic fisico del mouse alle coordinate.
    elif cmd == 'shell': # Se deve lanciare comandi...
        subprocess.run(act.get('command_line'), shell=True) # Esegue comando bash.
    elif cmd == 'photo': take_photo() # Fa la foto.
    elif cmd == 'scan_net': # Scansiona rete.
        out = scan_network() # Avvia scan.
        with open("outputs/knowledge_base.txt", "a") as f: f.write(f"\n[NETWORK] {out}") # Funzione .write(): Scrive i risultati nel file di testo.

def run_smart_chaos(): # Motore principale della vita digitale.
    threading.Thread(target=run_virtual_cursor, daemon=True).start() # Lancia il corpo dell'Essere Umano Digitale in parallelo.
    history = ["Sistema online. Essere Digitale manifestato."] # Memoria iniziale.
    while True: # Loop infinito (Ciclo di vita).
        actions = ai_decision(history) # Chiede comandi (Array di azioni).
        workers = [] # Array vuoto per i lavoratori attivi.
        for act in actions: # Per ogni comando nell'Array...
            t = threading.Thread(target=singolo_operaio, args=(act,)) # Crea un lavoratore dedicato per quella singola azione.
            workers.append(t) # Aggiunge il lavoratore all'elenco nell'Array.
            t.start() # Dà il via al lavoro parallelo.
        for t in workers: # Per ogni lavoratore...
            t.join(timeout=15) # Funzione .join(): Dice al programma principale di aspettare finché quest'azione non è finita.
        time.sleep(3) # Ciclo di riposo per risparmiare CPU.

if __name__ == "__main__": # Se lanciato...
    run_smart_chaos() # Accende ChaosGPT.
