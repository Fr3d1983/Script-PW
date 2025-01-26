import pandas as pd
import sqlite3
import logging
import datetime
import time

# Configurazione logging
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Log principale (dettagliato)
log_filename = f"log_importazione_utenti_{timestamp}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log di audit (conciso)
audit_log_filename = f"audit_importazione_utenti_{timestamp}.log"
audit_logger = logging.getLogger("AuditLogger")
audit_logger.setLevel(logging.INFO)
audit_handler = logging.FileHandler(audit_log_filename)
audit_handler.setFormatter(logging.Formatter("%(asctime)s - AUDIT - %(message)s"))
audit_logger.addHandler(audit_handler)
# Disattiva la propagazione di messaggi verso il logger principale per evitarne la ripetizione
audit_logger.propagate = False

# Funzione principale
def importa_utenti(excel_file: str, db_file: str) -> bool:
    """
    Importa dati utenti da file Excel a database SQLite.
    Ritorna True se l'operazione va a buon fine, False in caso di errore.
    """
    try:
        df = pd.read_excel(excel_file)
        logging.info("File Excel letto correttamente.")
        audit_logger.info("Inizio importazione utenti.")

        start_time = time.time()
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utenti (
                    Nome TEXT NOT NULL,
                    Cognome TEXT NOT NULL,
                    Email TEXT NOT NULL UNIQUE,
                    Telefono TEXT NOT NULL UNIQUE
                )
            """)
            conn.commit()
            logging.info("Tabella utenti creata o già esistente.")

            righe_inserite = 0
            righe_saltate = 0

            for index, row in df.iterrows():
                try:
                    cursor.execute(
                        "INSERT INTO utenti (Nome, Cognome, Email, Telefono) VALUES (?, ?, ?, ?)",
                        (row['Nome'], row['Cognome'], row['Email'], row['Telefono'])
                    )
                    conn.commit()
                    righe_inserite += 1
                    logging.debug(
                        f"Riga {index + 1} inserita: "
                        f"{row['Nome']}, {row['Cognome']}, {row['Email']}, {row['Telefono']}"
                    )
                except sqlite3.IntegrityError:
                    righe_saltate += 1
                    logging.warning(
                        f"Duplicato rilevato alla riga {index + 1}: "
                        f"{row['Nome']}, {row['Cognome']}, {row['Email']}, {row['Telefono']}"
                    )
                    print(f"Duplicato per Utente {index + 1} (riga saltata).")
                    audit_logger.warning(f"Duplicato in riga {index + 1}.")
                except Exception as e:
                    conn.rollback()
                    logging.exception(f"Errore in riga {index + 1}: {e}")
                    print(f"Errore inserimento Utente {index + 1}: {e}")
                    audit_logger.error(f"Errore in riga {index + 1}: {e}")
                   
            elapsed_time = time.time() - start_time

        logging.info(
            f"Importazione completata in {elapsed_time:.2f} s. "
            f"Inserite {righe_inserite}, saltate {righe_saltate}."
        )
        print(
            f"Importazione completata in {elapsed_time:.2f} s. "
            f"Inserite {righe_inserite}, saltate {righe_saltate}."
        )
        audit_logger.info(
            f"Importazione terminata: {righe_inserite} inserite, "
            f"{righe_saltate} duplicati. Tempo: {elapsed_time:.2f}s."
        )

    except FileNotFoundError as e:
        logging.error(f"Errore file non trovato: {e}")
        print(f"Errore file non trovato: {e}")
        audit_logger.error("Errore apertura file Excel.")
        return False
    except sqlite3.OperationalError as e:
        logging.error(f"Errore database: {e}")
        print(f"Errore database: {e}")
        audit_logger.error("Errore database.")
        return False
    except Exception as e:
        logging.exception(f"Errore principale: {e}")
        print(f"Errore principale: {e}")
        audit_logger.error("Errore durante l'operazione.")
        return False

    return True

# Main
if __name__ == "__main__":
    if importa_utenti("utenti.xlsx", "utenti.db"):
        logging.info("Operazione completata con successo.")
        print("Operazione completata con successo.")
        audit_logger.info("Operazione completata con successo.")
    else:
        logging.error("Operazione fallita.")
        print("Operazione fallita.")
        audit_logger.error("Operazione fallita.")
