# IMPORTA IL FILE DI CONFIGURAZIONE E LE LIBRERIE.
import pandas as pd # Libreria per la manipolazione dei dati.
import sqlite3 # Libreria per la connessione al database SQLite.
import logging # Libreria per il logging.
import config # File di configurazione.

# CONFIGURA IL LOGGING.
logging.basicConfig(
    filename=config.LOGGING_CONFIG['log_db_filename'], # Log in un file di testo.
    level=config.LOGGING_CONFIG['log_level'], # Livello di logging.
    format=config.LOGGING_CONFIG['log_format'] # Formato del log.
)

# CONFIGURA IL LOGGER PER L'AUDIT.
audit_logger = logging.getLogger("AuditLogger") # Crea un logger per l'audit.
audit_handler = logging.FileHandler(config.LOGGING_CONFIG['audit_db_filename']) # Log in un file di testo per l'audit.
audit_handler.setFormatter(logging.Formatter(config.LOGGING_CONFIG['audit_log_format'])) # Formato del log di audit.
audit_logger.addHandler(audit_handler) # Aggiunge il gestore 'hanndler' al logger per la registrazione degli eventi.
audit_logger.setLevel(config.LOGGING_CONFIG['log_level']) # Livello di logging per l'audit.

def create_table(conn):
    # DEFINISCE LA STRUTTURA DELLA TABELLA 'UTENTI' NEL DATABASE SQLITE.
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS utenti (
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL UNIQUE
    );
    """
    conn.execute(create_table_sql) # Esegue la query per creare la tabella.
    audit_logger.info("Tabella 'utenti' creata, (se non esisteva già).") # Log di audit.

def insert_data(conn, data):
    # INSERISCE I DATI NELLA TABELLA 'UTENTI'.
    insert_sql = """
    INSERT INTO utenti (nome, cognome, email, telefono)
    VALUES (?, ?, ?, ?)
    """
    try:
        for i, d in enumerate(data, start=1): # Itera sui record e li inserisce nella tabella.
            conn.execute(insert_sql, d) # Esegue la query di inserimento.
            logging.info(f"Inserito utente {i}: {d[0]} {d[1]}, {d[2]}, {d[3]}") # Log informativo per ogni record inserito.
        logging.info(f"{len(data)} record inseriti nella tabella 'utenti'.") # Log informativo sul totale dei record inseriti.
    except sqlite3.IntegrityError as e: # Gestisce gli errori di integrità.
        audit_logger.error(f"Errore di integrità durante l'inserimento dei dati: {e}") # Log di audit per gli errori di integrità.

def main():
    # LEGGE I DATI DAL FILE EXCEL SPECIFICATO NEL FILE DI CONFIGURAZIONE.
    try:
        df = pd.read_excel(config.EXCEL_FILENAME) # Legge il file Excel.
        audit_logger.info(f"Dati letti dal file Excel '{config.EXCEL_FILENAME}'.") # Log di audit.
    except Exception as e: # Gestisce gli errori durante la lettura del file Excel.
        audit_logger.error(f"Errore durante la lettura del file Excel: {e}") # Log di audit per gli errori.
        return

    # CONNESSIONE AL DATABASE SQLITE E CREAZIONE DEL DATABASE SE NON PRESENTE.
    try:
        conn = sqlite3.connect(config.DATABASE_FILENAME) # Connessione al database SQLite.
        audit_logger.info(f"Connesso al database SQLite '{config.DATABASE_FILENAME}'.") # Log di audit.
    except Exception as e: # Gestisce gli errori durante la connessione al database.
        audit_logger.error(f"Errore durante la connessione al database SQLite: {e}") # Log di audit per gli errori.
        return

    # CREA LA TABELLA.
    create_table(conn)

    # CONVERTE IL DATAFRAME IN UNA LISTA DI RECORD.
    data = df.values.tolist()

    # INSERISCE I RECORD NEL DATABASE E AGGIORNA IL LOG DI AUDIT.
    audit_logger.info("Inserimento dei dati iniziato.")
    insert_data(conn, data)
    audit_logger.info("Inserimento dei dati completato.")

    # SALVA LE MODIFICHE E CHIUDE LA CONNESSIONE.
    conn.commit()
    conn.close()
    audit_logger.info("Connessione al database chiusa.") # Log di audit.
    print(f"Dati inseriti nel database '{config.DATABASE_FILENAME}' con successo.") # Stampa a schermo dei dati inseriti.

# MAIN
if __name__ == "__main__":
    main()