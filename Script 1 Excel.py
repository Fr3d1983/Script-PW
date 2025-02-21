# IMPORTA IL FILE DI CONFIGURAZIONE E LE LIBRERIE.
import logging # Libreria per il logging.
import faker # Libreria per la generazione di dati realistici.
import random # Libreria per la generazione di numeri casuali.
import pandas as pd # Libreria per la manipolazione dei dati.
import config # File di configurazione.

# CONFIGURA IL LOGGING.
logging.basicConfig(
    filename=config.LOGGING_CONFIG['log_excel_filename'], # Log in un file di testo.
    level=config.LOGGING_CONFIG['log_level'], # Livello di logging.
    format=config.LOGGING_CONFIG['log_format'] # Formato del log.
)

# CONFIGURA IL LOGGER PER L'AUDIT.
audit_logger = logging.getLogger("AuditLogger") # Crea un logger per l'audit.
audit_handler = logging.FileHandler(config.LOGGING_CONFIG['audit_excel_filename']) # Log in un file di testo per l'audit.
audit_handler.setFormatter(logging.Formatter(config.LOGGING_CONFIG['audit_log_format'])) # Formato del log di audit.
audit_logger.addHandler(audit_handler) # Aggiunge il gestore 'hanndler' al logger per la registrazione degli eventi.
audit_logger.setLevel(config.LOGGING_CONFIG['log_level']) # Livello di logging per l'audit.

# UTILIZZA FAKER CON IL PARAMETRO DI LOCALIZZAZIONE OTTENUTO DAL FILE DI CONFIGURAZIONE.
fake = faker.Faker(config.FAKER_LOCALE)

# ELENCO DEI PROVIDER EMAIL OTTENUTO DAL FILE DI CONFIGURAZIONE.
EMAIL_PROVIDERS = config.EMAIL_PROVIDERS

def genera_email_unica(nome, cognome, providers, email_esistenti):
    # GENERA UN'EMAIL UNIVOCA (COMBINANDO NOME, COGNOME E UN PROVIDER CASUALE) E VERIFICA SE L'EMAIL NON SIA GIÀ STATA USATA.
    while True:
        email = f"{nome.lower()}.{cognome.lower()}@{random.choice(providers)}" # Genera l'email con un provider casuale.
        if email not in email_esistenti: # Verifica se l'email è già stata usata.
            email_esistenti.add(email) # Aggiunge l'email all'insieme degli email esistenti.
            return email # Restituisce l'email generata.
        else:
            logging.warning(f"Collisione trovata per l'email: {email}. Rigenero...") # Log di warning in caso di collisione.

def genera_telefono_unico(telefoni_esistenti):
    # GENERA UN NUMERO DI TELEFONO MOBILE ITALIANO UNIVOCO E VERIFICA SE IL NUMERO NON SIA GIÀ STATO USATO.
    while True:
        telefono = f"+39 3{random.randint(200000000, 999999999)}" # Genera un numero di telefono.
        if telefono not in telefoni_esistenti: # Verifica se il numero di telefono è già stato usato.
            telefoni_esistenti.add(telefono) # Aggiunge il numero di telefono all'insieme dei numeri esistenti.
            return telefono # Restituisce il numero di telefono generato.
        else:
            logging.warning(f"Collisione trovata per il telefono: {telefono}. Rigenero...") # Log di warning in caso di collisione.

def genera_dati(num_utenti):
    # GENERA UN NUMERO SPECIFICATO DI UTENTI CON NOME, COGNOME, EMAIL E TELEFONO, GARANTENDO L'UNICITÀ DI EMAIL E NUMERI DI TELEFONO.
    # RESTITUISCE UN DATAFRAME PANDAS CON I RISULTATI, REGISTRANDO I MESSAGGI DI LOG INFORMATIVO E AUDIT.
    logging.info(f"Inizio generazione di {num_utenti} utenti.")
    audit_logger.info(f"Generazione iniziata.")

    # INSIEMI PER TENERE TRACCIA DELLE EMAIL E NUMERI DI TELEFONO GENERATI PRECEDENTEMENTE.
    email_esistenti = set() # Insieme per le email.
    telefoni_esistenti = set() # Insieme per i numeri di telefono.
    utenti = [] # Lista per i dati degli utenti.

    # CICLO PER LA GENERAZIONE DEI DATI DEGLI UTENTI.
    for i in range(num_utenti): 
        nome = fake.first_name()  # Genera un nome casuale.
        cognome = fake.last_name()  # Genera un cognome casuale.
        email = genera_email_unica(nome, cognome, EMAIL_PROVIDERS, email_esistenti)  # Genera un'email univoca.
        telefono = genera_telefono_unico(telefoni_esistenti)  # Genera un numero di telefono univoco.

        # AGGIUNGE I DATI GENERATI ALLA LISTA DEGLI UTENTI.
        utenti.append({
            "Nome": nome,
            "Cognome": cognome,
            "Email": email,
            "Telefono": telefono
        })

        logging.info(f"Utente {i+1}: {nome} {cognome}, {email}, {telefono}") # Log informativo per ogni utente generato.

    audit_logger.info(f"Generazione di {len(utenti)} utenti unici completata.") # Log di audit per la generazione completata.
    return pd.DataFrame(utenti) # Restituisce i dati degli utenti come DataFrame Pandas.

# MAIN
if __name__ == "__main__":
    n_utenti = config.NUM_UTENTI  # Numero di utenti da generare ottenuto dal file di configurazione.
    dati_utenti = genera_dati(n_utenti) # Genera i dati degli utenti.
    
    # SALVATAGGIO IN EXCEL
    nome_file_excel = config.EXCEL_FILENAME  # Nome del file Excel ottenuto dal file di configurazione.
    dati_utenti.to_excel(nome_file_excel, index=False) # Salva i dati nel file Excel.

    # LOG FINALE E STAMPA A SCHERMO DEL NUMERO DI DATI DI UTENTI SALVATI.
    audit_logger.info(f"Dati salvati in {nome_file_excel}")
    print(f"Dati di {len(dati_utenti)} utenti salvati nel file Excel: {nome_file_excel}")