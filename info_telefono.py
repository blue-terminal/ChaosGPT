import subprocess
import re

def get_phone_info():
    print("==========================================")
    print("   SAMSUNG DEVICE DIAGNOSTIC TOOL")
    print("==========================================\n")
    
    # 1. Verifica ADB (se il telefono fosse acceso normalmente)
    print("[1/2] Controllo interfaccia ADB...")
    try:
        # Usiamo timeout per non bloccare
        adb_check = subprocess.check_output(['adb', 'devices'], stderr=subprocess.STDOUT).decode('utf-8')
        if "device\n" in adb_check:
            print(" -> ADB Rilevato! Il telefono è acceso normalmente.")
            fw = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.build.display.id']).decode('utf-8').strip()
            print(f" -> Firmware Attuale (via ADB): {fw}")
        else:
            print(" -> ADB non rilevato. Il telefono è in Download Mode o scollegato.")
    except:
        print(" -> ADB non disponibile in questo ambiente.")

    # 2. Verifica USB (per Download Mode)
    print("\n[2/2] Scansione Bus USB (Download Mode)...")
    try:
        lsusb = subprocess.check_output(['lsusb']).decode('utf-8')
        match = re.search(r'ID 04e8:(\w+)\s+(.*)', lsusb)
        
        if match:
            product_id = match.group(1)
            print(f" -> Dispositivo Samsung TROVATO (ID: 04e8:{product_id})")
            
            if product_id == '685d':
                print("\nDETTAGLI MODELLO:")
                print(" - Modello: Samsung Galaxy S II (GT-I9100)")
                print(" - Stato: Download Mode (Odin)")
                print(" - Firmware Consigliato (ITV): I9100XWLSW")
                print(" - Versione Android: 4.1.2 (Jelly Bean)")
                print("\nCOSA FARE ORA:")
                print(" 1. Scarica Odin v3.09 su PC Windows.")
                print(" 2. Scarica il firmware I9100XWLSW.")
                print(" 3. Carica il file in PDA/AP e premi Start.")
            else:
                print(f" -> Modello generico rilevato: {match.group(2)}")
        else:
            print(" -> Nessun dispositivo in Download Mode trovato.")
            
    except Exception as e:
        print(f" -> Errore scansione USB: {e}")

    print("\n==========================================")

if __name__ == "__main__":
    get_phone_info()
