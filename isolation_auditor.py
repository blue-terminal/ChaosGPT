import socket
import time
from colorama import init, Fore, Style

init(autoreset=True)

def test_lateral_movement(target_ips, ports):
    """
    Testa la capacità di muoversi lateralmente verso altri IP sulle porte specificate.
    Se la connessione ha successo, la rete NON è isolata correttamente.
    """
    print(Fore.CYAN + "=== AVVIO AUDIT DI ISOLAMENTO RETE (LATERAL MOVEMENT TEST) ===")
    print(Fore.YELLOW + "Verifica se questo host può raggiungere servizi critici su altri server...\n")

    vulnerabilities_found = 0

    for ip in target_ips:
        print(Fore.WHITE + f"[*] Scansione verso il target interno: {ip}")
        for port in ports:
            try:
                # Creiamo un socket TCP per tentare la connessione
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0) # Timeout breve, se è bloccato andrà in timeout subito
                
                result = s.connect_ex((ip, port))
                
                if result == 0:
                    print(Fore.RED + f"    [!] VULNERABILITÀ ISOLAMENTO: La porta {port} su {ip} è raggiungibile!")
                    print(Fore.RED + f"        -> Un malware su questa macchina potrebbe attaccare {ip}:{port}")
                    vulnerabilities_found += 1
                else:
                    # Connessione rifiutata o in timeout, significa che il firewall sta lavorando bene
                    print(Fore.GREEN + f"    [OK] Accesso bloccato verso {ip}:{port} (Isolamento funzionante)")
                
                s.close()
            except Exception as e:
                print(Fore.YELLOW + f"    [?] Errore durante il test di {ip}:{port} ({e})")
        print("-" * 50)
        time.sleep(0.5)

    print(Fore.CYAN + "\n=== RISULTATI AUDIT ===")
    if vulnerabilities_found > 0:
        print(Fore.RED + f"FALLITO: Sono state trovate {vulnerabilities_found} vie di movimento laterale aperte.")
        print("Azione richiesta: Configurare il firewall per bloccare il traffico in uscita (egress) non necessario verso queste porte.")
    else:
        print(Fore.GREEN + "SUCCESSO: Nessuna via di movimento laterale rilevata sulle porte testate. Isolamento forte.")

if __name__ == "__main__":
    # ESEMPIO: Inserisci qui gli IP degli altri server nella tua rete (es. Database, Server Backup)
    # 127.0.0.1 simula la macchina stessa, in un test reale metteresti IP come 192.168.1.50
    target_servers = ["127.0.0.1", "192.168.1.100", "10.0.0.5"]
    
    # Porte critiche usate dai worm per muoversi (SSH, SMB, RDP, Database)
    critical_ports = [22, 139, 445, 3389, 3306]

    test_lateral_movement(target_servers, critical_ports)
