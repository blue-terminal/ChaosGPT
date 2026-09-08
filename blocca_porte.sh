#!/bin/bash
# ==================================================
# blocca_porte.sh - Configura firewall e chiude porte inutili
# ==================================================

echo "🔥 Configurazione Firewall in corso..."

# --- REGOLE BASE ---
sudo ufw default deny incoming       # Blocca TUTTO il traffico in entrata
sudo ufw default allow outgoing      # Permetti tutto il traffico in uscita

# --- PORTE DA TENERE APERTE (necessarie) ---
sudo ufw allow 80/tcp                # HTTP (navigazione web)
sudo ufw allow 443/tcp               # HTTPS (navigazione sicura)
sudo ufw allow 53/udp                # DNS (risoluzione nomi)

# --- BLOCCA PORTE INUTILI/PERICOLOSE ---
sudo ufw deny 21/tcp                 # FTP
sudo ufw deny 22/tcp                 # SSH (se non usi accesso remoto)
sudo ufw deny 23/tcp                 # Telnet
sudo ufw deny 3306/tcp               # MySQL
sudo ufw deny 5432/tcp               # PostgreSQL
sudo ufw deny 6379/tcp               # Redis
sudo ufw deny 8080/tcp               # HTTP alternativo
sudo ufw deny 8888/tcp               # Jupyter Notebook
sudo ufw deny 11434/tcp              # Ollama AI (non accessibile dalla rete)
sudo ufw deny 3000/tcp               # Node.js dev server
sudo ufw deny 5000/tcp               # Flask dev server
sudo ufw deny 9090/tcp               # Prometheus

# --- BLOCCA IP SPECIFICO (router Pi-hole precedente) ---
sudo ufw deny from 192.168.1.53

# --- ATTIVA IL FIREWALL ---
sudo ufw --force enable

echo ""
echo "✅ Firewall attivo! Riepilogo regole:"
sudo ufw status verbose
echo ""
echo "🛡️ Porte bloccate: 21, 22, 23, 3306, 5432, 6379, 8080, 8888, 11434"
echo "✅ Porte aperte: 80 (HTTP), 443 (HTTPS), 53 (DNS)"
