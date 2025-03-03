# Generazione di dati utente fittizi e trasferimento su database SQLite

## Introduzione 

I due script Python principali del progetto generano dati fittizi di utenti e impiegano le librerie "**faker**" (*per generare dati realistici*) e "**pandas**" (*per la manipolazione e l'organizzazione dei dati in DataFrame*). 

* Il primo script crea un foglio di lavoro Excel con i dati (*nome, cognome, email e numero di telefono*) di 10 utenti.  

* Il secondo script acquisisce i dati del file Excel e popola un database SQLite replicandone esattamente la struttura e i dati.

* Il terzo script è un file di configurazione con dei parametri (*numero degli utenti, lista dei provider email, localizzazione di Faker, nomi dei file da generare e impostazioni di logging e audit*) utilizzati dagli altri due script.
    
## Prerequisiti 

Per la corretta esecuzione degli script, è necessario installare le suddette librerie, se non già presenti nel sistema. L'installazione può essere effettuata tramite "**pip**", il gestore di pacchetti di Python, eseguendo i seguenti comandi nel prompt dei comandi (CMD) o terminale:

***`pip install pandas`***

***`pip install faker`***  

oppure con un unico comando:

***`pip install pandas faker`***  

___
Le altre librerie/moduli impiegate ("***logging***", "***sqlite3***", "***random***", "***datetime***") sono incluse nella libreria standard di Python e non richiedono alcuna installazione.

## Funzionalità extra implementate

### Logging e Audit

Oltre ai file utenti.xlsx e utenti.db, il sistema crea per entrambi gli script un file di log principale e uno di audit.

>[!NOTE]
>
>Il modulo "**logging**" gestisce la registrazione degli eventi, generando due file di log distinti: uno per le informazioni operative (*log*) e uno per le attività di audit (*audit*), utili per tracciare l'esecuzione del codice, monitorare il flusso del programma ed esaminare eventuali errori o anomalie (*troubleshooting*).

### Gestione Big data

In scenari di generazione di dati su larga scala, con un numero di utenti dell'ordine delle centinaia di migliaia o superiore, la probabilità di collisioni (*ovvero la generazione di email e numeri di telefono duplicati*) aumenta significativamente. Il sistema gestisce questa eventualità attraverso un meccanismo di 
controllo che, come documentato nei log operativi e di audit, verifica l'univocità di ogni combinazione e scarta quelle duplicate, rigenerandole fino a trovarne una univoca.

Questa gestione garantisce l'integrità dei dati e di conseguenza comporta un aumento dei tempi di elaborazione, specialmente all'aumentare del numero di utenti generati.  

### Esempio pratico con grandi volumi di dati

Come dimostrato negli screenshot appena sotto, il sistema ha gestito con successo la generazione di 100.000 utenti, risolvendo automaticamente le collisioni tramite rigenerazione delle email per garantirne l’univocità.
I file di log documentano l’intero processo, evidenziando sia le collisioni rilevate che le correzioni applicate.

![image](https://github.com/Fr3d1983/Script-PW/blob/main/Images/log%20%26%20audit%20100000%20utenti.png)

Nonostante l’elevato volume di dati, il file Excel e il database SQLite mantengono una corrispondenza perfetta, confermando l’affidabilità del sistema.

![image](https://github.com/Fr3d1983/Script-PW/blob/main/Images/Excel%20%26%20dbSQL%20100000%20utenti.png)


