# ChaosGPT 2.0: implementazione di agenti di intelligenza artificiale autonoma

![Licenza: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Modello: Lama-3.2-1b](https://huggingface.co/ChaosGPT007/ChaosGPT)
![Motore: Ollama](https://img.shields.io/badge/Engine-Ollama-orange)
![Visione: supportata](https://img.shields.io/badge/Vision-Enabled-green)

## 🤖 Panoramica del progetto
Questo repository presenta un'implementazione autonoma di **ChaosGPT 2.0**, ottimizzato per l'esecuzione locale utilizzando il **Lama 3.2:1b** modello tramite **Ollama**. Una differenza delle interfacce di chat standard, ChaosGPT 2.0 opera all'interno di un ciclo continuo di "Pensiero-Azione-Osservazione", che gli consensi di ragiungere obiettivi complessi senza ricerca un costante intervento umano.

Ora aggiornato con **Capacità di visione artificiale**, l'agente può percepire il suo ambiente e interagire direttamente con l'interfaccia desktop.

> [!IMPORTANTE]
> **Disclaimer:** Questo progetto è destinato in modo esclusivo a scopi educativi e di ricerca rigorosa l'autonomia dell'intelligenza artificiale. Utilizzare la responsabilità.

---

## 🚀 Caratteristiche principali della versione 2.0

### 👁️ Visione e controllo desktop
ChaosGPT 2.0 ora è presente **Messa a terra visiva**. L'agente può:
* **Schermi di Analisi gli:** "Visualizza" lo stato attuale del tuo desktop o di applicazioni specifiche.
* **Controllo del mouse:** Identifica gli elementi dell'interfaccia utente (pulsanti, icone, campi di testo) e calcola le coordinate per eseguire clic, trasformazioni e movimenti.
* **Feedback in tempo reale:** Utilizza la conferma visiva per verificare se un'azione (come fare clic su un pulsante "Invia") ha avuto successo.

### 🧠 Ragimento anticipato (Albero dei pensieri)
ChaosGPT 2.0 va oltre la semplice previsione delle parole: esplorazione molto multipla percorsi di formazione, valutando la probabilità di successo di ogni passaggio prima dell'esecuzione.

### 💾 Memoria a lungo termine (integrazione RAG)
Integrato con un **Banca dati veterinari**, l'agente può:
* Memorizza e indica le informazioni fornite dalle ricerche sul web.
* Ricorda gli errori precedenti per evitare ripetizioni.
* Mantenere il concorso nelle sessioni che durano più giorni.

### 🛠️ Accesso agli strumenti nativi
L'agente è stato di una suite di strumenti locali:
* **Browser Web:** Per la cotta di informazioni in tempo reale.
* **Terminale/Shell:** Per eseguire script Python in un ambiente sicuro e sandbox.
* **File Gestore:** Per leggi e scrivere documentazione e registri locali.

---

## 🛠️ Tecnico dello stack
* **LLM:** Meta Lama 3.2 (1 miliardo di parametri) — *Veloce, leggi e locale.*
* **Motore di visione:** Modulo integrato di analisi degli screenshot.
* **Tempo di esecuzione:** [Ollama](https://ollama.ai/)
* **Architettura:** Flusso di lavoro agente (autocorrezione e liberazione)
* **Memoria:** Incorporazioni vettoriali per l'architettura persistente.

---

## 📋 Vieni divertente locale

1. **Installa Ollama:**
   Scarica e installa da [ollama.com](https://ollama.com).

2. **Tira il modello:**
   ```bash
   ollama run lama3.2:1b
