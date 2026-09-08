# Importazione librerie per processi di sistema, richieste web e navigazione browser
import subprocess          # Per l'esplorazione del sistema e l'esecuzione di comandi shell
import requests            # Per effettuare chiamate HTTP e scaricare dati dai siti web
import webbrowser          # Per aprire automaticamente il browser di sistema visibile
import urllib.parse        # Per codificare correttamente i testi delle ricerche (query) nei siti web

def execute_shell(cmd):
    """Esegue un comando arbitrario nel terminale Linux e restituisce l'output catturato."""
    try:
        # Lancia il comando 'cmd', cattura l'output standard (stdout) e gli eventuali errori (stderr)
        # Il parametro 'timeout=10' garantisce che un comando bloccato non fermi l'intera IA
        r = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        # Trasforma il risultato binario ricevuto in una stringa di testo leggibile
        return r.decode('utf-8', errors='ignore')
    except Exception as e: 
        # In caso di comando inesistente o errore di permessi, restituisce il dettaglio dell'errore
        return f"Errore Shell: {e}"

def google_search(query):
    """Comando avanzato per effettuare una ricerca reale su Google aprendo il browser."""
    try:
        # Trasforma la query dell'utente in un formato URL valido (es. spazi diventano %20)
        encoded_query = urllib.parse.quote(query)
        # Crea l'indirizzo URL finale per la ricerca di Google
        url = f"https://www.google.com/search?q={encoded_query}"
        # Ordina al sistema operativo di aprire il browser predefinito a quell'indirizzo
        webbrowser.open(url)
        # Ritorna una conferma all'IA che la ricerca è stata avviata correttamente
        return f"Ricerca Google avviata per l'utente: {query}"
    except Exception as e:
        # Segnalazione all'IA in caso di impossibilità ad avviare il browser
        return f"Errore ricerca automatica: {e}"

def open_url(url):
    """Apre istantaneamente un qualsiasi indirizzo web specifico nel browser visibile."""
    try:
        # Se l'URL manca del protocollo (es. google.com), aggiunge 'https://' automaticamente
        if not url.startswith("http"):
            url = "https://" + url
        # Apre l'URL fornito nel browser principale dell'utente
        webbrowser.open(url)
        # Ritorna conferma dell'invio del comando di navigazione
        return f"Sito internet aperto: {url}"
    except Exception as e:
        # Gestisce errori nel caso l'indirizzo non sia correttamente formattato
        return f"Errore apertura sito: {e}"

def browse_website(url, q=None):
    """Scarica 'in silenzio' i dati testuali da un sito web per permettere all'IA di analizzarli."""
    try: 
        # Imposta un User-Agent per far sembrare la richiesta un normale browser invece di un bot
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Invia la richiesta GET per scaricare il codice della pagina web (limite 5 secondi)
        r = requests.get(url, timeout=5, headers=headers)
        # Restituisce i primi 1000 caratteri della pagina per l'elaborazione dell'IA
        return r.text[:1000] 
    except Exception as e: 
        # Riferisce all'IA se il sito è offline o protetto da firewall
        return f"Errore estrazione dati: {e}"