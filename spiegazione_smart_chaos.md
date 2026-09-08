# 🧠 Manuale Dettagliato e Semplificato: SMART CHAOS GPT

Questo documento spiega in modo semplice e dettagliato come funziona il cervello e il corpo del tuo programma `smart_chaos.py`, mantenendo la logica originaria ma rendendola comprensibile anche a chi non ha scritto il codice.

L'intero programma è strutturato come un **Agente Intelligente (Agent AI)**. Immaginalo come un robot virtuale diviso in "organi".

---

## 🏗️ 1. Le Fondamenta e gli Strumenti (Fase 1 e 2)

All'inizio del file, il programma carica tutti gli strumenti di cui ha bisogno per interagire col mondo.
*   **Librerie:** Importa librerie per vedere (OpenCV), controllare mouse/tastiera (PyAutoGUI, xdotool), parlare (gTTS) e pensare (Requests per comunicare con Ollama).
*   **La Memoria (AgentMemory):** Il bot non è uno smemorato. Usa un database interno (`sqlite3`) per ricordarsi cosa ha fatto. Se un'azione fallisce, se lo segna ("Azione fallita"). Se funziona, se lo ricorda come un successo. Questo si chiama *RAG (Retrieval-Augmented Generation)*.
*   **I Poteri (ToolRegistry):** Qui c'è la *Whitelist* (lista bianca). È un sistema di sicurezza per evitare che l'intelligenza artificiale faccia cose a caso. Il bot può usare SOLO i poteri registrati qui dentro (es. `move`, `click`, `hacker_attack`, `network_defense`). Se l'IA si inventa un comando che non esiste in questa lista, il sistema la blocca.

---

## 🌡️ 2. I Sensi e la Diagnostica (Fase 3)

Il robot deve percepire l'ambiente e il proprio corpo (il tuo computer).
*   **Sensore CPU (`wait_for_cpu`):** Controlla quanto sta lavorando il processore. Se il PC sta per esplodere di fatica (sopra l'85% di utilizzo), il bot si mette in pausa per farlo "respirare" e non farti crashare il computer.
*   **Sensore Visivo (`webcam_vision_learn` & `capture_screen`):** Può usare la tua webcam per guardare fuori, oppure "fotografare" il tuo schermo per capire quali finestre hai aperto.

---

## 🦾 3. Il Corpo e le Azioni (Fase 4)

Questa è la parte "muscolare". Contiene le funzioni fisiche:
*   **Mouse e Tastiera:** Le funzioni `move_mouse`, `click_mouse` e `type_text` prendono fisicamente il controllo del tuo PC. *Trucco speciale:* quando il bot clicca, memorizza dove avevi tu il mouse, fa il suo clic a velocità della luce, e ti rimette il mouse dove lo avevi lasciato. Così non ti accorgi di nulla.
*   **La Voce (`speak`):** Crea un file audio MP3 con la voce di Google e lo riproduce in "sottofondo" (Thread), così il bot può continuare a lavorare mentre parla.

---

## 🧠 4. Il Cervello: La Logica IA (Fase 5)

Questa è la magia. Come fa il bot a decidere cosa fare?
1.  **L'Orchestratore (`ai_decision`):** Questa funzione raccoglie tutto il contesto: l'ora, le finestre aperte (tramite foto dello schermo), e cosa gli hai chiesto tu. 
2.  **La Telefonata a Ollama:** Prende tutti questi dati e li spedisce al tuo cervello locale (Ollama/Llama3).
3.  **Il Pensiero Strutturato (JSON):** L'IA non risponde con testo libero, ma è costretta a rispondere in un formato macchina preciso (JSON) dove dice:
    *   Cosa sta pensando ("Vedo il terminale aperto...")
    *   Cosa vuole dire a voce ("Sto per attaccare.")
    *   **Quali azioni (Tools) vuole eseguire dalla sua lista dei poteri.**

### 🗡️ I Moduli Offensivi e Difensivi
All'interno del codice sono stati inseriti i "Tool" che l'IA può richiamare:
*   `hacker_attack`: Apre tutti i software hacker presenti nella tua cartella (nmap, wireshark, sqlmap, ecc.) in terminali separati.
*   `auto_exploit`: Interroga il database offline (ExploitDB) per trovare vulnerabilità senza dover andare su internet.
*   `generate_payload`: Chiede all'IA di inventarsi da zero un codice Python malevolo e salvarlo in un file.
*   `network_defense`: Il contrario dell'attacco. Usa il firewall del tuo Linux (UFW) per chiudere il sistema come una cassaforte e controlla se ci sono intrusi.

---

## 🖥️ 5. La Faccia: L'Interfaccia Grafica (Fase 6)

La classe `ChaosUI` costruisce la finestra nera e verde (stile Matrix) che vedi sul monitor.
*   **La Bolla:** La piccola finestrella galleggiante che segue il mouse è indipendente e ti fa leggere i "pensieri" in tempo reale dell'IA.
*   **Casella di Input:** Ti permette di scrivere ordini manualmente (es. scrivere "tutto" o "difendi").

---

## ⚙️ 6. Il Motore (Fase 7 - Il Loop Principale)

La funzione `run_smart_chaos()` è il battito cardiaco del bot. È un ciclo infinito (`while True`) che fa questo, secondo dopo secondo:
1.  Si accerta che non stai fondendo la CPU.
2.  Scatta una foto allo schermo.
3.  Prende i tuoi comandi vocali o scritti.
4.  **Intercetta le parole chiave assolute:** Se scrivi *"hacker"*, salta il pensiero dell'IA e attiva subito i tool offensivi. Se scrivi *"difendi"*, alza i firewall. Se scrivi *"tutto"*, lancia sia l'attacco che la difesa.
5.  Se non ci sono ordini assoluti, lascia decidere all'IA.
6.  **L'Operaio (`singolo_operaio`):** Prende le decisioni del cervello (es. "clicca qui") e le fa eseguire al corpo fisico, una per volta per non creare confusione nel sistema operativo.
7.  Passa l'esito dell'azione alla Memoria (se ha funzionato o se ha dato errore) e ricomincia il ciclo.
