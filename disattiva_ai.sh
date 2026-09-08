#!/bin/bash
# ==================================================
# disattiva_ai.sh - Blocca l'accesso ai siti AI
# ==================================================

echo "🔴 Disattivazione accesso ai siti AI..."

# Prima rimuove eventuali vecchie voci duplicate
sudo sed -i '/chatgpt.com/d; /openai.com/d; /claude.ai/d; /gemini.google.com/d; /aistudio.google.com/d; /deepseek.com/d' /etc/hosts

# Aggiunge le nuove voci di blocco
echo "" | sudo tee -a /etc/hosts > /dev/null
echo "# --- BLOCCO SITI AI ---" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 chatgpt.com" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 openai.com" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 claude.ai" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 gemini.google.com" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 aistudio.google.com" | sudo tee -a /etc/hosts > /dev/null
echo "127.0.0.1 deepseek.com" | sudo tee -a /etc/hosts > /dev/null

# Svuota la cache DNS
sudo systemd-resolve --flush-caches 2>/dev/null || true

echo ""
echo "🚫 Fatto! I seguenti siti sono ora BLOCCATI:"
echo "   - chatgpt.com"
echo "   - openai.com"
echo "   - claude.ai"
echo "   - gemini.google.com"
echo "   - aistudio.google.com"
echo "   - deepseek.com"
echo ""
echo "💡 Ricarica il browser con CTRL+F5 se necessario."
