# Gym Bro Management System

----------------------------------------------------------------------------------------------------------------------------------------

## **Descrizione**

Il **Gym Bro  Management System** è un'applicazione Python progettata per la gestione delle prenotazioni degli attrezzi in una palestra. L'applicazione consente agli utenti di:

- Prenotare un attrezzo scegliendo una durata specifica.
- Avviare un timer per monitorare il tempo di utilizzo.
- Gestire automaticamente le prenotazioni in sequenza.

L'app utilizza **Tkinter** per l'interfaccia utente e un sistema di threading per gestire i timer in background, garantendo un'esperienza utente fluida.
È stata anche creata una presentazione PowerPoint breve che presenta le descrizioni dei file in inglese:https://docs.google.com/presentation/d/1UNfHYQee1NXiB33iJJ788ewbUbYJ69mq/edit#slide=id.p1

----------------------------------------------------------------------------------------------------------------------------------------

## **Struttura del progetto**

La struttura del progetto è stata divisa in moduli per migliorare la manutenibilità e la leggibilità del codice:

----------------------------------------------------------------------------------------------------------------------------------------

## **File Descrizione**

### **1. `UI.py`**
- Contiene la classe `GymBookingUI`, che gestisce l'interfaccia utente utilizzando il framework **Tkinter**.
- Permette agli utenti di:
  - Selezionare un attrezzo dal menu a discesa.
  - Specificare la durata dell'uso in secondi.
  - Prenotare un attrezzo con opzioni aggiuntive (es. selezione peso per i manubri).
  - Avviare un timer per monitorare le prenotazioni in sequenza.

#### Componenti principali:
- **Form di prenotazione:** 
  - Menù a discesa per selezionare l'attrezzo.
  - Campo di input per la durata.
  - Campo di input o menu per il peso, se necessario.
- **Lista prenotazioni:** Mostra tutte le prenotazioni effettuate.
- **Gestione timer:** Interfaccia per avviare, mettere in pausa e completare gli esercizi.

### **2. `machines_management.py`**
- Contiene la classe `BookingManager`, che gestisce la logica di prenotazione e le operazioni legate agli attrezzi.

#### Funzionalità principali:
- **Caricamento attrezzi:** Legge i dettagli degli attrezzi dal file JSON (`machines.json`).
- **Prenotazioni:** Permette di aggiungere, rimuovere e modificare le prenotazioni.
- **Salvataggio:** Gestisce la modifica del tempo residuo di un attrezzo.

### **3. `machines.json`**
- File JSON che memorizza i dettagli degli attrezzi disponibili in palestra.
- Ogni attrezzo ha una durata predefinita per l'utilizzo:
  ```json
  {
      "Manubri": {"durata": 10},
      "Cyclette": {"durata": 30},
      ...
  }

----------------------------------------------------------------------------------------------------------------------------------------

## Requisiti

### Prerequisiti

1. **Python 3.9 o successivo**
   - Assicurati di avere Python installato. Puoi scaricarlo da [python.org](https://www.python.org/).
2. **Tkinter**
   - Incluso nella maggior parte delle distribuzioni Python. Per installarlo su Linux:
     ```bash
     sudo apt-get install python3-tk
     ```

### Librerie Python

Le librerie richieste sono incluse nel core di Python e non necessitano di installazioni aggiuntive:
- `tkinter`
- `threading`
- `time`
- `json`

