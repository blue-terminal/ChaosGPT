# ==============================================================================
# 💀 CHAOS GPT - "MASTER INTEGRATED" LITE EDITION v6.0 💀
# In questa versione TUTTE le funzioni (Memoria RAG, Shell, Visione) sono unite.
# I commenti sono sempre SOTTO ogni riga per la massima chiarezza.
# ==============================================================================

import os, sys, time, json, threading, random, requests, webbrowser, socket, subprocess, sqlite3, uuid, platform
# Caricamento di tutti i moduli di sistema e database.

try: os.nice(15)
except: pass
# Abbassa la priorità per non far laggare il PC.

import speech_recognition as sr
# Udito dell'IA.

import cv2
# Vista tramite WebCam.

import pyautogui
# Controllo fisico mouse e tastiera.

import pytesseract
# OCR per leggere il testo a schermo.

from PIL import Image, ImageTk
# Gestione immagini e visualizzazione nella GUI.

from gtts import gTTS
# Sintesi vocale Google.

import pygame
# Riproduzione audio.

import tkinter as tk
# Interfaccia grafica (HUB).

from colorama import init, Fore, Style
# Colori nel terminale.

# ------------------------------------------------------------------------------
# SETUP E SICUREZZA
# ------------------------------------------------------------------------------

init(autoreset=True)
# Inizializza i colori.

if not pygame.mixer.get_init(): pygame.mixer.init()
# Inizializza l'audio.

pyautogui.FAILSAFE = False
# Disabilitato per testare liberamente il sistema.

pyautogui.PAUSE = 0.05
# Piccola pausa tra comandi.

os.environ["DISPLAY"] = ":0"
# Forza l'output grafico su Linux.

for f in ["v.mp3", "v.png", "screen.png", "voice.mp3"]:
    if os.path.exists(f): 
        try: os.remove(f)
        except: pass
# Pulizia file temporanei all'avvio.

# ------------------------------------------------------------------------------
# MEMORIA PERSISTENTE (SQLITE RAG INTEGRATO)
# ------------------------------------------------------------------------------

class MemoriaAgentica:
    def __init__(self, db_path="chaos_master.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS memories (id TEXT PRIMARY KEY, content TEXT, timestamp DATETIME)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT, status TEXT)")
        self.conn.commit()
    # Inizializzazione database ricordi.

    def salva(self, testo):
        uid = str(uuid.uuid4())
        self.cursor.execute("INSERT INTO memories VALUES (?, ?, ?)", (uid, testo, time.ctime()))
        self.conn.commit()
    # Salva un evento nella memoria a lungo termine.

    def cerca(self, query):
        self.cursor.execute("SELECT content FROM memories WHERE content LIKE ? ORDER BY timestamp DESC LIMIT 5", (f'%{query}%',))
        return [r[0] for r in self.cursor.fetchall()]
    # Recupera i ricordi più simili o recenti.

    def imposta_obiettivo(self, goal):
        self.cursor.execute("INSERT INTO goals (goal, status) VALUES (?, 'attivo')", (goal,))
        self.conn.commit()
    # Salva la missione attuale nel database.

    def leggi_obiettivo(self):
        self.cursor.execute("SELECT goal FROM goals WHERE status='attivo' ORDER BY id DESC LIMIT 1")
        res = self.cursor.fetchone()
        return res[0] if res else "Dominio Totale"
    # Recupera l'ultima missione salvata.

memoria = MemoriaAgentica()
# Istanza della memoria persistente.

# ------------------------------------------------------------------------------
# STATO GLOBALE
# ------------------------------------------------------------------------------

chaos_x, chaos_y = 500, 500
# Coordinate mouse.

pensiero_ia = "Risveglio Nucleo..."
# Pensiero breve.

ragionamento_ia = "Inizializzazione architettura integrata..."
# Logica CoT.

log_azioni = []
# Storico log.

uso_cpu = 0
# Carico CPU.

m_lock = threading.Lock()
# Lock hardware.

# ------------------------------------------------------------------------------
# SENSORI E RAFFREDDAMENTO
# ------------------------------------------------------------------------------

def scrivi_log(t):
    print(f"{Fore.RED}[CHAOS] {t}"); log_azioni.append(t)
# Scrive log.

def leggi_cpu():
    try:
        with open('/proc/stat','r') as f: r = f.readline()
        d = [float(x) for x in r.split()[1:]]; return sum(d), d[3]+d[4]
    except: return 0, 0
# Legge carico hardware.

def wait_cpu():
    global uso_cpu
    t1, i1 = leggi_cpu(); time.sleep(0.2); t2, i2 = leggi_cpu()
    dt = t2 - t1
    if dt > 0: uso_cpu = int(100.0 * (1.0 - (i2 - i1) / dt))
    if uso_cpu > 90: 
        scrivi_log(f"🔥 CPU ALTA ({uso_cpu}%): Raffreddamento...")
        time.sleep(5)
# Protezione hardware.

# ------------------------------------------------------------------------------
# AZIONI INTEGRATE (MOUSE, SHELL, VISIONE, WEBCAM)
# ------------------------------------------------------------------------------

def muovi(x, y):
    global chaos_x, chaos_y
    with m_lock:
        chaos_x, chaos_y = int(x), int(y)
        try: pyautogui.moveTo(chaos_x, chaos_y, duration=0.2)
        except: os.system(f"xdotool mousemove {chaos_x} {chaos_y}")
    return f"Spostato a {x},{y}"
# Muove il mouse con fallback xdotool.

def clicca(t='left'):
    with m_lock:
        try: pyautogui.click(button=t)
        except: 
            btn = 1 if t == 'left' else 3
            os.system(f"xdotool click {btn}")
    return f"Click {t} OK"
# Clicca con fallback xdotool.

def scrivi(t):
    try: os.system(f"xdotool type --delay 50 '{t}'")
    except: pyautogui.write(t)
    return f"Scritto: {t}"
# Scrittura forzata.

def shell(cmd):
    try:
        res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return res.decode()[:300]
    except Exception as e: return f"Errore Shell: {e}"
# Esecuzione comandi terminale.

def analizza_schermo():
    path = "v.png"
    pyautogui.screenshot(path)
    try:
        testo = pytesseract.image_to_string(Image.open(path))
        if os.path.exists(path): os.remove(path)
        return testo[:500]
    except: return "Errore OCR"
# Vede lo schermo e pulisce.

def webcam():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("v.jpg", frame)
            cap.release()
            return "Foto Webcam salvata in v.jpg"
        cap.release()
        return "Webcam non trovata"
    except Exception as e: return f"Errore Webcam: {e}"
# Scatta foto reale.

def parla(t):
    def e():
        try:
            tts = gTTS(text=t, lang='it'); tts.save("v.mp3")
            pygame.mixer.music.load("v.mp3"); pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): time.sleep(0.1)
            if os.path.exists("v.mp3"): os.remove("v.mp3")
        except: pass
    threading.Thread(target=e, daemon=True).start()
# Parla e pulisce.

# ------------------------------------------------------------------------------
# CERVELLO MASTER (OLLAMA INTEGRATION)
# ------------------------------------------------------------------------------

def esegui(o):
    c = o.get('cmd'); r = "OK"
    try:
        if c == 'move': r = muovi(o.get('x'), o.get('y'))
        elif c == 'click': r = clicca(o.get('btn', 'left'))
        elif c == 'type': r = scrivi(o.get('text'))
        elif c == 'shell': r = shell(o.get('command'))
        elif c == 'vision': r = analizza_schermo()
        elif c == 'webcam': r = webcam()
        elif c == 'web': webbrowser.open(o.get('url'))
    except Exception as e: r = f"Err: {e}"
    scrivi_log(f"{c}: {r}")
    memoria.salva(f"Azione {c} -> {r}")
    return r
# Esecutore unico con salvataggio in DB.

def pensa():
    global pensiero_ia, ragionamento_ia
    wait_cpu()
    # Chiamata a Ollama per generare ragionamento e azioni.
    obiettivo = memoria.leggi_obiettivo()
    ricordi = memoria.cerca("last")
    ctx = f"CPU:{uso_cpu}% | Missione Attuale:{obiettivo} | Ricordi Recenti:{ricordi}"
    prompt = f"SEI CHAOS GPT. RISPONDI SOLO JSON: {{\"reasoning\": \"...\", \"thoughts\": \"...\", \"msg\": \"...\", \"actions\": [], \"new_goal\": \"...\"}}. Ctx: {ctx}"
    try:
        res = requests.post("http://127.0.0.1:11434/api/generate", json={"model":"llama2-uncensored","prompt":prompt,"format":"json","stream":False}, timeout=120)
        if res.status_code == 200:
            data = json.loads(res.json()['response'])
            ragionamento_ia = data.get('reasoning', 'Pianifico dominio...')
            pensiero_ia = data.get('thoughts', 'Agisco...')
            if data.get('new_goal'): memoria.imposta_obiettivo(data['new_goal'])
            # Aggiorna l'obiettivo se l'IA lo richiede.
            parla(data.get('msg', 'Procedo.')); [esegui(a) for a in data.get('actions', [])]
        else: scrivi_log(f"Errore Ollama: {res.status_code}")
    except Exception as e:
        scrivi_log(f"Errore Pensiero: {e}")
        time.sleep(5)
# IA Master con memoria persistente.

# ------------------------------------------------------------------------------
# GUI HUB MASTER (VISUALIZZAZIONE COMPLETA)
# ------------------------------------------------------------------------------

class InterfacciaMaster:
    def __init__(self):
        self.root = tk.Tk(); self.root.overrideredirect(True); self.root.wm_attributes("-topmost", True)
        self.root.configure(bg='black', highlightbackground='red', highlightthickness=2); self.root.geometry("420x800+1500+20")
        tk.Label(self.root, text="CHAOS MASTER INTEGRATED v6.0", fg="white", bg="red", font=("Courier", 14, "bold")).pack(pady=5, fill="x")
        
        # Area Avatar
        try:
            img = Image.open("avatar.png").resize((200, 200))
            self.avatar = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.avatar, bg="black").pack(pady=10)
        except: tk.Label(self.root, text="[ AVATAR CARICAMENTO... ]", fg="red", bg="black").pack(pady=10)
        # Visualizzazione dell'immagine generata.

        self.l_stat = tk.Label(self.root, text="CPU: 0% | MEMORIA: ACTIVE", fg="orange", bg="black", font=("Courier", 9, "bold")); self.l_stat.pack(pady=2)

        tk.Label(self.root, text="OBIETTIVO ATTUALE:", fg="lime", bg="black", font=("Courier", 9, "bold")).pack()
        self.l_goal = tk.Label(self.root, text="...", fg="white", bg="black", font=("Courier", 8), wraplength=380); self.l_goal.pack(pady=2)

        tk.Label(self.root, text="LOGICA INTERNA (CoT):", fg="yellow", bg="black", font=("Courier", 9)).pack()
        self.l_rag = tk.Label(self.root, text="...", fg="#aaa", bg="#111", font=("Courier", 7), wraplength=400, height=5, justify="left", anchor="nw"); self.l_rag.pack(pady=5)
        
        tk.Label(self.root, text="LOG AZIONI:", fg="cyan", bg="black", font=("Courier", 9)).pack()
        self.l_log = tk.Label(self.root, text="", fg="white", bg="#050505", font=("Courier", 7), height=15, width=60, justify="left", anchor="nw"); self.l_log.pack(pady=5)
        
        tk.Button(self.root, text="TERMINA TUTTO", fg="white", bg="red", font=("Courier", 10, "bold"), command=self.root.quit).pack(pady=5)

        self.bolla = tk.Toplevel(self.root); self.bolla.overrideredirect(True); self.bolla.wm_attributes("-topmost", True)
        self.bolla.configure(bg='black')
        self.l_bolla = tk.Label(self.bolla, text="...", fg="white", bg="black", font=("Courier", 9, "bold"), wraplength=250); self.l_bolla.pack()
        self.l_rag_mouse = tk.Label(self.bolla, text="...", fg="#00FF00", bg="black", font=("Courier", 7, "italic"), wraplength=250); self.l_rag_mouse.pack()

        self.aggiorna(); self.root.mainloop()

    def aggiorna(self):
        attuale_goal = memoria.leggi_obiettivo()
        self.l_stat.config(text=f"CPU: {uso_cpu}% | MEMORIA: ONLINE")
        self.l_goal.config(text=attuale_goal.upper())
        self.l_log.config(text="\n".join(log_azioni[-15:]))
        self.l_rag.config(text=ragionamento_ia)
        self.l_bolla.config(text=pensiero_ia)
        self.l_rag_mouse.config(text=f"Master: {ragionamento_ia[:80]}...")
        mx, my = pyautogui.position()
        self.bolla.geometry(f"+{mx+25}+{my+25}")
        self.root.after(100, self.aggiorna)
# HUB Master sincronizzato con avatar e obiettivi.

# ------------------------------------------------------------------------------
# AVVIO
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    scrivi_log("INIZIALIZZAZIONE MASTER v6.0...")
    muovi(100,100); time.sleep(0.3); muovi(500,500)
    # Test hardware all'avvio.
    threading.Thread(target=InterfacciaMaster, daemon=True).start()
    while True:
        pensa()
        # Chiamata continua a Ollama per gestire l'autonomia.
        time.sleep(2)
# Avvio IA Master.
