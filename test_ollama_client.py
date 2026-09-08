"""
test_ollama_client.py
---------------------
Client essenziale (usando urllib nativo di Python) per testare l'inferenza locale
del modello leggero Qwen2.5:0.5b su Ollama.
"""

import urllib.request
import json
import time

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_API_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=60) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            elapsed = round(time.time() - start_time, 2)
            reply = res_json.get("response", "").strip()
            print(f"[OLLAMA - {MODEL_NAME}] Risposta generata in {elapsed}s:")
            print("-" * 50)
            print(reply)
            print("-" * 50)
            return reply
    except Exception as e:
        print(f"[!] Errore durante la richiesta a Ollama: {e}")
        return ""


if __name__ == "__main__":
    test_prompt = "Spiega in una frase cosa fa un programma per computer."
    print(f"[*] Invio prompt a Ollama locale ({MODEL_NAME})...")
    query_ollama(test_prompt)
