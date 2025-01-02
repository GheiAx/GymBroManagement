import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from machines_management import BookingManager


class GymBookingUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prenotazione Attrezzi Palestra")
        self.root.geometry("440x380")
        self.root.resizable(False, False)

        self.manager = BookingManager()
        self.attrezzo_var = tk.StringVar(self.root)
        self.durata_var = tk.IntVar(self.root)
        self.peso_var = tk.IntVar(self.root)

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.create_widgets()

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        ttk.Label(header_frame, text="Prenotazione Attrezzi", font=("Helvetica", 16, "bold")).pack()

        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # Scelta attrezzo
        ttk.Label(form_frame, text="Attrezzo:").grid(row=0, column=0, sticky="w")
        self.attrezzo_var.set(self.manager.get_attrezzi()[0])
        self.attrezzo_menu = ttk.OptionMenu(
            form_frame, self.attrezzo_var, *self.manager.get_attrezzi(), command=self.update_peso_visibility
        )
        self.attrezzo_menu.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Durata
        ttk.Label(form_frame, text="Durata (secondi):").grid(row=0, column=2, sticky="w")
        ttk.Entry(form_frame, textvariable=self.durata_var, width=10).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        # Peso
        self.peso_label = ttk.Label(form_frame, text="Peso (kg):")
        self.peso_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.peso_entry = ttk.Entry(form_frame, textvariable=self.peso_var, width=10)
        self.peso_entry.grid(row=1, column=1, sticky="ew", pady=(5, 0))

        self.peso_menu = ttk.OptionMenu(
            form_frame, self.peso_var, None  # Placeholder; valori verranno aggiornati dinamicamente
        )
        self.peso_menu.grid(row=1, column=1, sticky="ew", pady=(5, 0))
        self.peso_menu.grid_remove()

        # Bottoni
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=2, column=0, columnspan=4, sticky="ew")
        ttk.Button(button_frame, text="Prenota", command=self.prenota_attrezzo).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Avvia Timer", command=self.avvia_timer).grid(row=0, column=1, padx=10)

        # Lista prenotazioni
        self.lista_prenotazioni = tk.Listbox(self.root, width=70, height=10)
        self.lista_prenotazioni.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def update_peso_visibility(self, selected_attrezzo):
        if selected_attrezzo in ["Cyclette", "Tapis roulant"]:
            self.peso_label.grid_remove()
            self.peso_entry.grid_remove()
            self.peso_menu.grid_remove()
        elif selected_attrezzo == "Manubri":
            self.peso_label.grid()
            self.peso_entry.grid()
            self.peso_menu.grid_remove()
        else:
            self.peso_label.grid()
            self.peso_entry.grid_remove()
            self.peso_menu.grid()

            weights = list(range(5, 105, 5))
            self.peso_var.set(weights[0])
            menu = self.peso_menu["menu"]
            menu.delete(0, "end")
            for weight in weights:
                menu.add_command(label=weight, command=lambda w=weight: self.peso_var.set(w))

    def prenota_attrezzo(self):
        attrezzo = self.attrezzo_var.get()
        durata = self.durata_var.get()

        if attrezzo == "Manubri":
            peso = self.peso_var.get()
            if peso <= 0:
                messagebox.showerror("Errore", "Inserisci un peso valido per i manubri.")
                return
            attrezzo = f"Manubri {peso}kg"
        elif attrezzo in ["Cyclette", "Tapis roulant"]:
            peso = None
        else:
            peso = self.peso_var.get()
            attrezzo = f"{attrezzo} {peso}kg"

        self.manager.prenota_attrezzo(attrezzo, durata)
        self.lista_prenotazioni.insert(tk.END, f"{attrezzo} - {durata} secondi")

    def avvia_timer(self):
        if not self.manager.has_prenotazioni():
            messagebox.showinfo("Info", "Nessuna prenotazione disponibile.")
            return

        self.avvia_esercizio()

    def avvia_esercizio(self):
        if not self.manager.has_prenotazioni():
            messagebox.showinfo("Info", "Tutte le prenotazioni sono state completate.")
            return

        attrezzo, durata = self.manager.get_prossima_prenotazione()
        CountdownWindow(self.root, attrezzo, durata, self.prossimo_esercizio, self.salva_tempo)

    def prossimo_esercizio(self):
        self.lista_prenotazioni.delete(0)
        self.avvia_esercizio()

    def salva_tempo(self, attrezzo, durata_rimanente):
        self.manager.salva_tempo(attrezzo, durata_rimanente)
        self.lista_prenotazioni.insert(0, f"{attrezzo} - {durata_rimanente} secondi")

    def run(self):
        self.root.mainloop()


class CountdownWindow:
    def __init__(self, parent, attrezzo, durata, completato_callback, pausa_callback):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Esercizio: {attrezzo}")
        self.completato_callback = completato_callback
        self.pausa_callback = pausa_callback
        self.attrezzo = attrezzo
        self.durata = durata

        ttk.Label(self.top, text=f"Attrezzo: {attrezzo}", font=("Helvetica", 14)).pack(pady=10)
        self.timer_var = tk.StringVar(value=f"Tempo rimanente: {durata} secondi")
        self.timer_label = ttk.Label(self.top, textvariable=self.timer_var, font=("Helvetica", 16, "bold"))
        self.timer_label.pack(pady=10)

        button_frame = ttk.Frame(self.top, padding="10")
        button_frame.pack()

        ttk.Button(button_frame, text="Metti in pausa", command=self.mettere_in_pausa).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Chiudi", command=self.annulla).pack(side="right", padx=5)

        self.in_esecuzione = True
        self.thread = threading.Thread(target=self.start_countdown)
        self.thread.start()

    def start_countdown(self):
        while self.durata > 0 and self.in_esecuzione:
            time.sleep(1)
            self.durata -= 1
            self.timer_var.set(f"Tempo rimanente: {self.durata} secondi")

        if self.durata == 0:
            self.termina()

    def termina(self):
        self.timer_var.set("Esercizio completato!")
        ttk.Button(self.top, text="Avvia prossimo esercizio", command=self.prossimo).pack(pady=10)

    def prossimo(self):
        self.top.destroy()
        self.completato_callback()

    def mettere_in_pausa(self):
        self.in_esecuzione = False
        self.pausa_callback(self.attrezzo, self.durata)
        self.top.destroy()

    def annulla(self):
        self.in_esecuzione = False
        self.top.destroy()
