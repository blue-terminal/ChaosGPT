import json
import os

OUT_DIR = 'modello/'

def genera_dataset_avanzati():
    print("\n--- GENERATORE DATASET SPECIALISTICI (Wireless, Network, Web) ---")
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. DATASET WIRELESS (Aircrack-ng & Co)
    wireless_data = [
        {"prompt": "### Istruzione:\nConfigura l'interfaccia wireless in monitor mode.", "completion": "Usa 'sudo airmon-ng start <interface>'. Prima esegui 'sudo airmon-ng check kill' per fermare i processi interferenti."},
        {"prompt": "### Istruzione:\nCattura un handshake WPA2 su un canale specifico.", "completion": "Comando: 'sudo airodump-ng --bssid <BSSID> --channel <CH> --write capture <interface>'. Questo salverà i pacchetti in un file .cap."},
        {"prompt": "### Istruzione:\nEsegui un attacco di deautenticazione per forzare l'handshake.", "completion": "Comando: 'sudo aireplay-ng --deauth 10 -a <AP_BSSID> -c <Client_MAC> <interface>'. Utile per disconnettere i client e catturare i pacchetti di riconnessione."},
        {"prompt": "### Istruzione:\nCracka una password WPA2 usando una wordlist.", "completion": "Comando: 'aircrack-ng -w <wordlist.txt> -b <BSSID> <capture_file.cap>'. Richiede un handshake catturato precedentemente."}
    ]
    salva_file(wireless_data, "wireless_aircrack")

    # 2. DATASET NETWORK TRAFFIC (Analisi PCAP)
    network_data = [
        {"prompt": "### Istruzione:\nIdentifica un SYN Flood attack dal traffico di rete.", "completion": "Cerca un volume elevato di pacchetti SYN senza corrispondenti ACK. In Wireshark usa il filtro: 'tcp.flags.syn == 1 and tcp.flags.ack == 0'."},
        {"prompt": "### Istruzione:\nAnalizza i pattern di ARP Spoofing.", "completion": "Cerca più indirizzi MAC associati allo stesso indirizzo IP nel log ARP. Filtro Wireshark: 'arp.duplicate-address-detected'."},
        {"prompt": "### Istruzione:\nEstrai file da un dump di traffico HTTP.", "completion": "In Wireshark: File -> Export Objects -> HTTP. Oppure usa 'NetworkMiner' per ricostruire automaticamente i file dai pacchetti PCAP."}
    ]
    salva_file(network_data, "network_traffic")

    # 3. DATASET WEB SCANNING (Payloads & Vulnerability)
    web_data = [
        {"prompt": "### Istruzione:\nGenera un payload per testare SQL Injection bypass.", "completion": "Payload: ' OR 1=1-- ' oppure ' admin' -- '. Questi tentano di bypassare la logica di autenticazione."},
        {"prompt": "### Istruzione:\nPayload per Cross-Site Scripting (XSS) riflesso.", "completion": "Payload base: '<script>alert(1)</script>'. Payload avanzato: '<svg onload=alert(1)>' per bypassare filtri semplici."},
        {"prompt": "### Istruzione:\nEsegui una scansione di vulnerabilità con Nikto.", "completion": "Comando: 'nikto -h <target_url>'. Analizza header, file sensibili e versioni server vulnerabili."}
    ]
    salva_file(web_data, "web_scanning")

def salva_file(data, nome):
    path = os.path.join(OUT_DIR, f"dataset_{nome}.jsonl")
    with open(path, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')
    print(f" [OK] Creato {path} con {len(data)} esempi specialistici.")

if __name__ == "__main__":
    genera_dataset_avanzati()
