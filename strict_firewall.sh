#!/bin/bash
# ==============================================================================
# SCRIPT: IL MURA DELLA PRIGIONE (STRICT FIREWALL)
# Questo script trasforma il tuo computer in un bunker. Tutto il mondo internet
# viene staccato dalla presa, tranne i pochissimi siti che autorizziamo qui.
# ==============================================================================

echo "[*] FASE 1: AZZERARE TUTTO..."
# Spazza via tutte le vecchie regole del firewall, pulendo il cervello di UFW
sudo ufw --force reset

# DICE A LINUX: "Da questo momento in poi, chiunque cercherà di far Uscire (outgoing)
# o Entrare (incoming) anche un singolo MegaByte di dati verso Internet, verrà distrutto!"
sudo ufw default deny outgoing
sudo ufw default deny incoming

echo "[*] FASE 2: RIACCENDERE IL CERVELLO DI BASE (Loopback e DNS)..."
# Abilita IL LOOPBACK LOCALE (lo). Il PC parla con se stesso.
# SE NON METTI QUESTO, il computer fa crash e si blocca l'intero sistema operativo!
sudo ufw allow in on lo
sudo ufw allow out on lo

# Abilita le porte 53. La porta 53 è il "DNS". Il DNS è l'elenco telefonico di internet.
# Se non apri la porta 53, il computer non sa che google.com corrisponde a dei numeri IP!
sudo ufw allow out 53/udp
sudo ufw allow out 53/tcp

echo "[*] FASE 3: LISTA DEI "VIP" (Solo chi è qui dentro può passare)..."
# Questo è un grande secchio (array) che contiene tutti i nomi dei siti web autorizzati
DOMAINS=(
    "google.com"
    "www.google.com"
    "google.it"
    "canva.com"
    "www.canva.com"
    "thepythoncode.com"
    "mspace.it"
    "instagram.com"
    "www.instagram.com"
    "gemini.google.com"
    "github.com"
    "api.github.com"
    "githubassets.com" # Contiene le immagini vere di Github
    "avatars.githubusercontent.com"
    "camo.githubusercontent.com"
    "protonvpn.com" # Il sito per chi usa Proton
    "api.protonvpn.ch"
    "account.proton.me"
    "api.protonmail.ch"
    "api.protonmail.com"
    "pass.proton.me"
    "youtube.com"
    "www.youtube.com"
    "googlevideo.com" # Il dominio segreto da cui YT pompa davvero i video
    "ytimg.com"
    "i.ytimg.com"
    "ggpht.com" # Le copertine dei canali youtube
    "raw.githubusercontent.com"
    "generativelanguage.googleapis.com" # Il serve segreto di GEMINI/Antigravity
    "googleapis.com"
    "www.googleapis.com"
    "oauth2.googleapis.com" # Server per fare Login con account Google
    "gstatic.com"
    "fonts.gstatic.com"
    "fonts.googleapis.com"
    "googleusercontent.com"
    "translate.google.com" # OBBLIGATORIO PER FAR FUNZIONARE LA VOCE DI CHAOS GPT!
    "translate.googleapis.com"
    "twitch.tv"
    "ttvnw.net" # Pezzi di live di Twitch
    "jtvnw.net"
)

# Qui parte un ciclo. Python si chiamerà "for". In Bash è "for DOMAIN in..."
# Traduzione: "Per ogni nome di sito (DOMAIN) contenuto nel secchio DOMAINS, fai questo:"
for DOMAIN in "${DOMAINS[@]}"; do
    # Digità di nascosto "dig +short ilmiosito.com".
    # Il comando DIG va a chiedere a internet qual è il N° IP segreto del sito.
    # Poi grep controlla che sia davvero un numero IP pulito per essere sicuri.
    IPS=$(dig +short "$DOMAIN" | grep -E '^[0-9.]+$')
    
    # Per ciascun IP trovato per un sito...
    for IP in $IPS; do
        # Crea la regola fissa! Manda al muro (UFW) l'ordine: "Fagli scaricare e navigare (port 80 e 443 TCP)!"
        sudo ufw allow out to "$IP" port 80,443 proto tcp comment "Allow $DOMAIN"
    done
done

echo "[*] FASE 4: ECCEZIONI SPECIALI FATTE A MANO..."

echo "[*] Aggiunta IP diretti per mspace/cPanel..."
# Questo è il server del tuo CPanel con le porte strane (2083) per non bloccarti il sito!
sudo ufw allow out to 86.107.36.49 port 80,443,2083 proto tcp comment "Allow mspace.it cpanel server"

echo "[*] Aggiunta Subnet globali di GitHub (per aggirare i blocchi dei CDN)..."
# I siti giganti come GitHub hanno milioni di IP. DIG falliva nel prenderli tutti.
# Quindi qui gli abbiamo sbattuto direttamente i "Recinti" (Subnets intere /20 e /22) 
# dicendogli "Falli passare in blocco, sono tutti buoni!"
sudo ufw allow out to 140.82.112.0/20 port 80,443 proto tcp comment "GitHub Core"
sudo ufw allow out to 192.30.252.0/22 port 80,443 proto tcp comment "GitHub Core 2"
sudo ufw allow out to 185.199.108.0/22 port 80,443 proto tcp comment "GitHub Assets/Pages"

echo "[*] Abilitazione porte VPN (ProtonVPN / OpenVPN / WireGuard / IPSec)..."
# Un muro deve avere i buchi per far passare i tubi sicuri.
# Queste sono le porte UDP/TCP famose in tutto il mondo che le VPN usano per nascondere il tuo traffico.
sudo ufw allow out 1194/udp
sudo ufw allow out 1194/tcp
sudo ufw allow out 51820/udp
sudo ufw allow out 500/udp
sudo ufw allow out 4500/udp

echo "[*] FASE FINALE E ATTIVAZIONE..."
# Prende tutte le regole accumulate qui sopra e ALZA lo scudo bloccandolo (-force per non fargli chiedere sicurezze).
sudo ufw --force enable

echo "[OK] Il bunker è pronto. Il Firewall UFW è vivo e vegeto."
