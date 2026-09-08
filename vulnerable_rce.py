import os

def execute_user_command():
    # VULNERABILITÀ RCE: l'input dell'utente viene passato direttamente alla shell
    comando = input("Inserisci un comando da eseguire: ")
    os.system(comando)

def evaluate_expression():
    # VULNERABILITÀ RCE: l'input viene valutato come codice Python
    espressione = input("Inserisci un'espressione matematica: ")
    print(f"Risultato: {eval(espressione)}")

if __name__ == "__main__":
    execute_user_command()
    evaluate_expression()
