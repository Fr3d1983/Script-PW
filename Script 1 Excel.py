import logging
import faker
import random
import pandas as pd
import datetime

# Configurazione logging
log_filename = f"generazione_utenti_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Logger per l'audit
audit_logger = logging.getLogger("AuditLogger")
audit_handler = logging.FileHandler("audit.log")
audit_handler.setFormatter(logging.Formatter("%(asctime)s - AUDIT - %(message)s"))
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

# Localizzazione di Faker in italiano
fake = faker.Faker('it_IT')

# Provider email italiani più comuni
EMAIL_PROVIDERS = [
    "alice.it", "aruba.it", "fastweb.it", "gmail.com", 
    "hotmail.it", "kataweb.it", "libero.it", "live.it", 
    "outlook.it", "tiscali.it", "virgilio.it", "yahoo.it"
]

# Funzioni di supporto
def genera_email_unica(nome, cognome, providers, email_esistenti):
    """
    Genera un'email univoca combinando nome, cognome e un provider casuale.
    Verifica che l'email non sia già stata usata.
    """
    while True:
        email = f"{nome.lower()}.{cognome.lower()}@{random.choice(providers)}"
        if email not in email_esistenti:
            email_esistenti.add(email)
            return email

def genera_telefono_unico(telefoni_esistenti):
    """
    Genera un numero di telefono italiano fittizio univoco.
    Verifica che il numero non sia già stato usato.
    """
    while True:
        telefono = f"+39 3{random.randint(200000000, 999999999)}"
        if telefono not in telefoni_esistenti:
            telefoni_esistenti.add(telefono)
            return telefono

def genera_dati(num_utenti=10):
    """
    Genera un numero specificato di utenti con nome, cognome, email e telefono,
    evitando duplicati per email e numero di telefono.
    Restituisce un DataFrame Pandas con i risultati.
    """
    logging.info(f"Inizio generazione di {num_utenti} utenti.")
    audit_logger.info(f"Generazione avviata per {num_utenti} utenti.")

    # Insiemi per tenere traccia delle email e numeri di telefono già generati
    email_esistenti = set()
    telefoni_esistenti = set()
    utenti = []

    for i in range(num_utenti):
        nome = fake.first_name() 
        cognome = fake.last_name() 
        email = genera_email_unica(nome, cognome, EMAIL_PROVIDERS, email_esistenti) 
        telefono = genera_telefono_unico(telefoni_esistenti) 

        utenti.append({
            "Nome": nome,
            "Cognome": cognome,
            "Email": email,
            "Telefono": telefono
        })

        logging.info(f"Utente {i+1}: {nome} {cognome}, {email}, {telefono}")

    audit_logger.info(f"Generati {len(utenti)} utenti unici.")
    return pd.DataFrame(utenti)

# Main
if __name__ == "__main__":
    n_utenti = 10
    dati_utenti = genera_dati(n_utenti)
    
    # Salvataggio in Excel
    nome_file_excel = "utenti.xlsx"
    dati_utenti.to_excel(nome_file_excel, index=False)

    # Log finale e stampa a schermo
    logging.info(f"Dati di {len(dati_utenti)} utenti salvati in {nome_file_excel}")
    audit_logger.info(f"Esportazione completata: {len(dati_utenti)} utenti salvati in {nome_file_excel}")
    print(f"Dati di {len(dati_utenti)} utenti salvati nel file Excel: {nome_file_excel}")
