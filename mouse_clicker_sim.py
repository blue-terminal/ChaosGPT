import speech_recognition as sr, pygame, io
from gtts import gTTS

pygame.init()
r = sr.Recognizer()

# 1. Registrazione audio tramite microfono
with sr.Microphone() as src:
    print("Parla ora...")
    r.adjust_for_ambient_noise(src)
    audio = r.listen(src)

# 2. Riconoscimento vocale e decisione della risposta
try:
    testo = r.recognize_google(audio, language="it-IT").lower()
    print("Hai detto:", testo)
    risposta = "ciao come va?" if "ciao" in testo else "non ho capito"
except Exception:
    risposta = "scusa, non ho sentito bene"

# 3. Creazione dell'audio in memoria RAM (nessun file mp3 creato)
fp = io.BytesIO()
gTTS(risposta, lang='it').write_to_fp(fp)
fp.seek(0)

# 4. Riproduzione dell'audio
pygame.mixer.music.load(fp)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): pygame.time.wait(100)