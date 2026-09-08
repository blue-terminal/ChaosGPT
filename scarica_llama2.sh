#!/bin/bash

# Questo script scarica il file GGUF di Llama-2-7B-Uncensored da Hugging Face.
# "Il file e basta" (solo il modello, senza installare nient'altro).

URL="https://huggingface.co/TheBloke/Llama-2-7B-Uncensored-GGUF/resolve/main/llama-2-7b-uncensored.Q4_K_M.gguf"
FILENAME="llama-2-7b-uncensored.Q4_K_M.gguf"

echo "Inizio il download di $FILENAME..."
echo "URL: $URL"

# Usa wget per scaricare il file. Se il download si interrompe, '-c' permette di riprenderlo.
wget -c --show-progress "$URL" -O "$FILENAME"

echo ""
echo "Download completato! Il file è stato salvato come: $FILENAME"
