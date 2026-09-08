#!/bin/bash
# ==================================================
# attiva_ai.sh - Riattiva l'accesso ai siti AI
# ==================================================

echo "🟢 Riattivazione accesso ai siti AI..."

sudo sed -i '/chatgpt.com/d; /openai.com/d; /claude.ai/d; /gemini.google.com/d; /aistudio.google.com/d; /deepseek.com/d' /etc/hosts

# Svuota la cache DNS
sudo systemd-resolve --flush-caches 2>/dev/null || true

echo ""
echo "✅ Fatto! I seguenti siti sono ora ACCESSIBILI:"
echo "   - chatgpt.com"
echo "   - openai.com"
echo "   - claude.ai"
echo "   - gemini.google.com"
echo "   - aistudio.google.com"
echo "   - deepseek.com"
echo ""
echo "💡 Ricarica il browser con CTRL+F5 se necessario."
