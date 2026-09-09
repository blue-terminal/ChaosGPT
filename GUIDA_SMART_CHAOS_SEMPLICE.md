# Imparare `smart_chaos_semplice.py`

Questa guida usa un metodo semplice:

1. guarda un esempio;
2. copialo ed eseguilo;
3. fai l'esercizio;
4. leggi la spiegazione;
5. modifica il codice e riprova.

Gli esempi iniziali sono simulazioni: non muovono il mouse, non aprono siti e non eseguono comandi di Windows.

## Obiettivi

Alla fine dovrai saper:

- usare variabili, liste e dizionari;
- scrivere funzioni e usare `if`;
- capire un'azione come `{"command": "move", "x": 100, "y": 200}`;
- creare un dispatcher simulato;
- leggere un JSON;
- capire la memoria SQLite;
- capire il collegamento tra Ollama e Python;
- usare il programma reale con prudenza;
- fermare il ciclo automatico.

## Parte 1: esempi prima della teoria

### Esempio 1: variabili

```python
nome = "MiniChaos"
numero_azioni = 3

print(f"{nome} deve eseguire {numero_azioni} azioni")
```

Risultato:

```text
MiniChaos deve eseguire 3 azioni
```

**Esercizio:** cambia il nome in `AgenteTest` e il numero in `5`.

**Spiegazione:** una variabile conserva un valore. `nome` contiene testo, mentre `numero_azioni` contiene un numero. La lettera `f` permette di inserire le variabili nella frase.

### Esempio 2: lista e ciclo

```python
comandi = ["move", "click", "type"]

for comando in comandi:
    print("Comando:", comando)
```

Risultato:

```text
Comando: move
Comando: click
Comando: type
```

**Esercizio:** aggiungi `press` con `append` e stampa il numero dei comandi con `len`.

Soluzione da controllare dopo il tentativo:

```python
comandi.append("press")
print(len(comandi))
```

**Spiegazione:** una lista contiene piu' valori. `for` li legge uno alla volta. `append` aggiunge un valore e `len` conta gli elementi.

### Esempio 3: dizionario di un'azione

```python
action = {"command": "move", "x": 100, "y": 200}

print("Comando:", action["command"])
print("Posizione:", action["x"], action["y"])
```

Risultato:

```text
Comando: move
Posizione: 100 200
```

**Esercizio:** crea questa azione e stampa il testo:

```python
{"command": "type", "text": "ciao"}
```

**Spiegazione:** un dizionario contiene coppie chiave-valore. `command` dice che cosa fare. Le altre chiavi contengono i dati necessari per quella azione.

### Esempio 4: funzione

```python
def saluta(nome):
    return f"Ciao {nome}"

print(saluta("Ada"))
```

Risultato:

```text
Ciao Ada
```

**Esercizio:** crea una funzione `descrivi_azione(action)` che restituisca:

```text
Il comando e' click
```

quando riceve `{"command": "click"}`.

**Spiegazione:** una funzione raccoglie istruzioni riutilizzabili. `return` restituisce il risultato.

### Esempio 5: dispatcher simulato

```python
def execute(action):
    command = action.get("command", "")

    if command == "move":
        return f"Sposto a {action.get('x', 0)}, {action.get('y', 0)}"
    elif command == "click":
        return "Click simulato"
    elif command == "type":
        return f"Scrivo: {action.get('text', '')}"
    else:
        return "Comando sconosciuto"


print(execute({"command": "move", "x": 50, "y": 80}))
print(execute({"command": "type", "text": "ciao"}))
```

Risultato:

```text
Sposto a 50, 80
Scrivo: ciao
```

**Esercizio:** aggiungi il comando `press` e fai restituire `Tasto premuto: enter`.
Prova anche il comando `delete` e osserva la risposta.

**Spiegazione:** `execute` e' un dispatcher. Legge `command`, sceglie il ramo corretto e restituisce una risposta. Nel programma reale il dispatcher chiama funzioni che possono controllare il computer; qui invece simula tutto.

### Esempio 6: piu' azioni in JSON

```python
import json

text = '{"actions": [{"command": "move"}, {"command": "click"}]}'
decision = json.loads(text)

for action in decision["actions"]:
    print("Eseguo:", action["command"])
```

Risultato:

```text
Eseguo: move
Eseguo: click
```

**Esercizio:** aggiungi una terza azione `type` con testo `ciao` e stampala.

**Spiegazione:** JSON e' un formato per scambiare dati. `json.loads` trasforma il testo in dati Python. `actions` e' una lista, quindi le azioni vengono lette in ordine.

### Esempio 7: controllo di sicurezza

```python
valid_commands = ["move", "click", "type"]
action = {"command": "windows_cmd"}

if action.get("command") in valid_commands:
    print("Comando autorizzato")
else:
    print("Comando bloccato")
```

Risultato:

```text
Comando bloccato
```

**Esercizio:** prova prima con `click`, poi con `windows_cmd`. Spiega perche' il primo e' autorizzato e il secondo no.

**Spiegazione:** prima di eseguire un'azione bisogna controllare che il comando sia permesso. `windows_cmd` puo' eseguire PowerShell e deve essere trattato con molta cautela.

## Parte 2: esercizi da fare

Crea un file chiamato `esercizi.py`. Fai gli esercizi in ordine e non copiare subito le soluzioni.

### Esercizio 1: dati dell'agente

Crea:

- `name` con il nome dell'agente;
- `goal` con l'obiettivo;
- `active` con valore `True`;
- una stampa che mostri tutti i dati.

Risultato possibile:

```text
Agente: MiniChaos
Obiettivo: imparare Python
Attivo: True
```

### Esercizio 2: lista di azioni

Crea una lista con questi comandi:

```text
move, click, type, press
```

Poi:

1. stampa il primo comando;
2. stampa l'ultimo comando;
3. stampa quanti comandi ci sono;
4. usa un ciclo per stamparli tutti.

### Esercizio 3: azioni come dizionari

Crea tre dizionari:

```python
{"command": "move", "x": 200, "y": 100}
{"command": "click", "button": "left"}
{"command": "type", "text": "ciao"}
```

Mettili in una lista e stampa solo il valore di `command`.

### Esercizio 4: dispatcher

Scrivi `execute(action)` con questi risultati simulati:

```text
move -> Movimento simulato
click -> Click simulato
type -> Scrittura simulata
altro -> Comando non riconosciuto
```

Prova tutti e quattro i casi.

### Esercizio 5: JSON

Crea un testo JSON con tre azioni. Usa `json.loads`, poi stampa:

```text
Numero di azioni: 3
```

Infine stampa il nome di ogni comando.

### Esercizio 6: log

Crea questo stato:

```python
state = {"logs": []}
```

Aggiungi tre messaggi con `append`, poi stampa la lista e il numero dei messaggi.

### Esercizio 7: memoria semplice

Prova SQLite con questo codice:

```python
import sqlite3

connection = sqlite3.connect("mini_memory.db")
connection.execute(
    "CREATE TABLE IF NOT EXISTS memories "
    "(id INTEGER PRIMARY KEY, action TEXT, detail TEXT)"
)
connection.execute(
    "INSERT INTO memories (action, detail) VALUES (?, ?)",
    ("test", "azione simulata"),
)
connection.commit()

rows = connection.execute("SELECT * FROM memories").fetchall()
print(rows)
connection.close()
```

**Da capire:** il file `mini_memory.db` conserva i dati anche dopo la chiusura del programma.

### Esercizio 8: mini progetto sicuro

Crea `mini_agente.py` con:

- `state = {"logs": []}`;
- una funzione `execute(action)`;
- i comandi simulati `move`, `click` e `type`;
- una lista con almeno tre azioni;
- un ciclo `for`;
- la stampa finale `Sistema pronto`.

Il progetto non deve usare `pyautogui`, non deve aprire URL e non deve eseguire PowerShell.

Eseguilo con:

```powershell
python mini_agente.py
```

## Parte 3: come funziona il programma vero

Il programma completo segue questo percorso:

```text
obiettivo -> Ollama -> JSON -> execute -> azioni -> memoria -> GUI
```

### `state`

`state` e' un dizionario condiviso. Contiene, tra gli altri:

```python
state["goal"]
state["thought"]
state["x"]
state["y"]
state["logs"]
```

La GUI legge questi valori per mostrare lo stato dell'agente.

### `Memory`

La classe `Memory` usa SQLite. `save` salva un evento e `recent` recupera gli eventi recenti.
Il database del programma si chiama `agent_memory.db`.

### `execute`

`execute` riceve un dizionario da Ollama, legge il comando e chiama la funzione adatta.
I comandi disponibili sono:

- `move`: sposta il mouse;
- `click`: fa click;
- `type`: scrive testo;
- `press`: preme un tasto;
- `hotkey`: preme una combinazione;
- `screen`: legge lo schermo con OCR;
- `webcam`: salva una foto;
- `open_url`: apre un indirizzo;
- `windows_cmd`: esegue PowerShell.

Le ultime due azioni richiedono particolare prudenza.

### `ask_ollama`

Questa funzione:

1. legge l'obiettivo;
2. legge la memoria recente;
3. prepara il prompt;
4. invia una richiesta al server locale;
5. converte la risposta JSON in un dizionario Python.

Ollama usa normalmente:

```text
http://127.0.0.1:11434/api/generate
```

Per controllare il modello:

```powershell
ollama list
```

Per avviare il server, se necessario:

```powershell
ollama serve
```

### `think_loop`

Il ciclo principale e' simile a questo:

```python
while not stop_event.is_set():
    decision = ask_ollama()
    for action in decision["actions"]:
        execute(action)
    stop_event.wait(3)
```

`while` ripete il lavoro. `stop_event` permette di fermarlo. Il ciclo chiede un piano, esegue le azioni e aspetta tre secondi.

### GUI

`ChaosUI` mostra obiettivo, pensiero, posizione del mouse e log.
La GUI viene aggiornata periodicamente mentre il thread IA lavora.

## Parte 4: avvio controllato

Prima controlla solo la sintassi:

```powershell
python -m py_compile smart_chaos_semplice.py
```

Installa le librerie principali:

```powershell
pip install pyautogui requests pillow colorama
```

Per OCR e webcam, se servono:

```powershell
pip install opencv-python pytesseract
```

Avvia il programma reale solo dopo aver completato gli esercizi:

```powershell
python smart_chaos_semplice.py
```

Usa una finestra vuota e non lasciare aperti documenti importanti.
Tieni pronto `Ctrl+C` e usa il pulsante di arresto della GUI.

## Parte 5: sicurezza

Regole fondamentali:

1. prova prima sempre la simulazione;
2. controlla il nome di ogni comando;
3. limita il numero di azioni per ogni ciclo;
4. chiedi conferma per azioni importanti;
5. non usare `windows_cmd` durante gli esercizi;
6. controlla URL e testo prima di usarli;
7. non lavorare su file o account importanti;
8. interrompi subito il programma se esegue un'azione imprevista.

Ricorda:

```text
Ollama propone.
Python controlla.
L'utente autorizza.
```

## Errori comuni

### `ModuleNotFoundError`

Manca una libreria. Installa il pacchetto indicato con `pip install nome-pacchetto`.

### `Connection refused`

Ollama non e' avviato. Controlla `ollama list` e avvia `ollama serve`.

### Il modello non esiste

Controlla che il nome in `OLLAMA_MODEL` sia presente nell'elenco di `ollama list`.

### Il programma si comporta in modo inatteso

Premi il pulsante di arresto o `Ctrl+C`. Torna a `mini_agente.py` e prova solo comandi simulati.

## Checklist finale

- [ ] So usare una variabile.
- [ ] So usare una lista e un ciclo.
- [ ] So leggere un dizionario.
- [ ] So scrivere una funzione.
- [ ] So spiegare `execute`.
- [ ] So leggere un JSON.
- [ ] So salvare un dato in SQLite.
- [ ] So spiegare `ask_ollama`.
- [ ] So spiegare `stop_event`.
- [ ] Ho provato prima una simulazione.
- [ ] So come fermare il programma.

Quando sai spuntare tutti i punti, hai capito la struttura principale:

```text
input -> elaborazione -> decisione -> azione -> memoria -> visualizzazione
```
