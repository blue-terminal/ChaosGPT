import subprocess
import os
import requests
import webbrowser

def execute_shell(command_line):
    try:
        result = subprocess.check_output(command_line, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return result.decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8', errors='ignore')}"
    except Exception as e:
        return f"Execution failed: {e}"

def google_search(query):
    """Esegue una ricerca reale per trovare link streaming Serie A."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            if results:
                formatted = "\n".join([f"- {r['title']}: {r['href']}" for r in results])
                return f"Risultati trovati:\n{formatted}"
            return "Nessun risultato trovato."
    except ImportError:
        # Fallback se il modulo manca
        import webbrowser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return "Modulo duckduckgo_search mancante. Apertura browser in corso..."
    except Exception as e:
        return f"Errore durante la ricerca: {str(e)}"

def browse_website(url, question=None):
    try:
        resp = requests.get(url, timeout=5)
        text = resp.text[:500] + "..." # Limitiamo l'output
        return f"Website content: {text}"
    except Exception as e:
        return f"Browsing failed: {e}"

def open_in_system_browser(url):
    """Apre un URL nel browser predefinito del sistema."""
    try:
        return webbrowser.open(url)
    except Exception as e:
        return f"Failed to open browser: {e}"

def brave_search(query):
    """Esegue una ricerca usando il motore di ricerca Brave."""
    url = f"https://search.brave.com/search?q={query}"
    return open_in_system_browser(url)

def open_local_file(filepath):
    """Apre un file locale usando l'applicazione predefinita del sistema."""
    import sys
    try:
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', filepath])
        elif sys.platform == 'win32':
            os.startfile(filepath)
        return f"File {filepath} aperto correttamente."
    except Exception as e:
        return f"Errore apertura file: {e}"