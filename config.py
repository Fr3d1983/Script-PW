# LIBRERIA PER GENERARE I TIMESTAMP PER I NOMI DEI FILE DI LOG E AUDIT.
import datetime

# LOCALIZZAZIONE DI FAKER IN ITALIANO.
FAKER_LOCALE = 'it_IT'

# PROVIDER EMAIL ITALIANI PIÙ COMUNI.
EMAIL_PROVIDERS = [
    'alice.it', 'aruba.it', 'fastwebnet.it', 'gmail.com',
    'hotmail.it', 'kataweb.it', 'libero.it', 'live.it',
    'outlook.it', 'tiscali.it', 'virgilio.it', 'yahoo.it'
]

# NUMERO DI UTENTI DA GENERARE.
NUM_UTENTI = 10

# NOME DEL FILE EXCEL IN CUI SALVARE I DATI GENERATI.
EXCEL_FILENAME = "utenti.xlsx"

# NOME DEL DATABASE SQLITE IN CUI SALVARE I DATI IMPORTATI.
DATABASE_FILENAME = "utenti.db"

# CONFIGURAZIONE LOGGING E AUDIT.
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') # Genera un timestamp per i nomi dei file di log e audit.
LOGGING_CONFIG = {
    'log_excel_filename': f"log_excel_{timestamp}.log", # Nome del file di log per la generazione di dati in Excel.
    'log_db_filename': f"log_db_{timestamp}.log", # Nome del file di log per l'importazione nel database.
    'audit_excel_filename': f"audit_excel_{timestamp}.log", # Nome del file di audit per la generazione di dati in Excel.
    'audit_db_filename': f"audit_db_{timestamp}.log", # Nome del file di audit per l'importazione nel database.
    'log_level': 'INFO', # Livello di logging.
    'log_format': '%(asctime)s - %(levelname)s - %(message)s', # Formato del log.
    'audit_log_format': '%(asctime)s - AUDIT - %(message)s' # Formato del log di audit.
}