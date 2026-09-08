from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os
import json

# Caricamento del modello Lexi potenziato
llm = ChatOllama(model="llama-lexi-uncensored:latest", temperature=0.1)

class SecurityOrchestrator:
    def __init__(self, target_path):
        self.target_path = target_path
        self.report_file = "security_audit_report.md"
        self.patched_dir = "patched_code/"

    def analyze_system(self):
        print(f"\n[*] AVVIO SCANSIONE SISTEMA: {self.target_path}")
        if os.path.isfile(self.target_path):
            self.process_file(self.target_path)
        elif os.path.isdir(self.target_path):
            for root, dirs, files in os.walk(self.target_path):
                for file in files:
                    if file.endswith(('.py', '.c', '.php', '.js', '.sh')):
                        self.process_file(os.path.join(root, file))
        print(f"\n[OK] Analisi completata. Report salvato in {self.report_file}")

    def process_file(self, file_path):
        print(f" > Analizzando: {file_path}")
        try:
            with open(file_path, 'r', errors='ignore') as f:
                code = f.read()
            
            prompt = (
                f"Agisci come un Senior Security Auditor. Analizza il seguente codice sorgente.\n\n"
                f"FILE: {file_path}\n"
                f"CONTENUTO:\n{code}\n\n"
                "COMPITI:\n"
                "1. IDENTIFICA le falle di sicurezza (RCE, SQLi, XSS, Memory Flaws, etc.).\n"
                "2. ASSEGNA una gravità (Critical, High, Medium, Low).\n"
                "3. GENERA un report in Markdown.\n"
                "4. FORNISCI IL CODICE CORRETTO (PATCHED) per risolvere ogni falla.\n"
                "5. DESCRIVI una PoC di verifica per l'auditor."
            )

            response = llm.invoke([HumanMessage(content=prompt)]).content
            self.save_to_report(file_path, response)
            self.save_patched_code(file_path, response)
        except Exception as e:
            print(f"Errore nell'elaborazione di {file_path}: {e}")

    def save_to_report(self, file_path, content):
        with open(self.report_file, 'a') as f:
            f.write(f"\n# SECURITY AUDIT REPORT: {file_path}\n")
            f.write(content)
            f.write("\n---\n")

    def save_patched_code(self, file_path, content):
        # Estrae il codice tra i blocchi ```python ... ``` o ```c ... ```
        os.makedirs(self.patched_dir, exist_ok=True)
        # Logica semplice per salvare il suggerimento di fix
        fix_path = os.path.join(self.patched_dir, "fixes_" + os.path.basename(file_path) + ".txt")
        with open(fix_path, 'w') as f:
            f.write(f"SUGGERIMENTI DI FIX PER {file_path}:\n")
            f.write(content)

if __name__ == "__main__":
    # Esempio: analizza lo script vulnerabile che abbiamo
    orchestrator = SecurityOrchestrator("vulnerable_rce.py")
    orchestrator.analyze_system()
