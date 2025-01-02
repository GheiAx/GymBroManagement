import json


class BookingManager:
    def __init__(self):
        self.attrezzi = self.load_attrezzi()
        self.prenotazioni = []

    def load_attrezzi(self):
        try:
            with open("machines.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Errore: Il file 'machines.json' non è stato trovato.")
            return {}
        except json.JSONDecodeError:
            print("Errore: Il file 'machines.json' non è valido.")
            return {}

    def get_attrezzi(self):
        return list(self.attrezzi.keys())

    def prenota_attrezzo(self, attrezzo, durata):
        self.prenotazioni.append((attrezzo, durata))

    def has_prenotazioni(self):
        return len(self.prenotazioni) > 0

    def get_prossima_prenotazione(self):
        return self.prenotazioni.pop(0)

    def salva_tempo(self, attrezzo, durata_rimanente):
        self.prenotazioni.insert(0, (attrezzo, durata_rimanente))
