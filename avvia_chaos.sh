#!/bin/bash
cd /home/blue-terminal/Desktop/ChaosGPT
# Verifica se Ollama è attivo, altrimenti lo avvia
if ! curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "Avvio di Ollama..."
    ollama serve > ollama.log 2>&1 &
    sleep 5
fi
./venv/bin/python3 smart_chaos.py
