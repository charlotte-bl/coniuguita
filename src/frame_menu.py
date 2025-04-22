import customtkinter as ctk

class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_title = ctk.CTkLabel(self, text="Coniuguita", font=("TkDefaultFont", 30))
        self.label_title.grid(row=1, column=0, sticky="nsew")

        self.label_mood = ctk.CTkLabel(self, text="Mood", font=("TkDefaultFont", 25))
        self.label_mood.grid(row=2, column=0, sticky="nsew")

        self.moods = {
            "Infinito": ["Presente", "Passato"],
            "Participio": ["Presente", "Passato"],
            "Gerundio": ["Presente", "Passato"],
            "Indicativo": ["Presente", "Imperfetto", "Passato remoto", "Futuro semplice",
                           "Passato prossimo", "Trapassato prossimo", "Trapassato remoto", "Futuro anteriore"],
            "Congiuntivo": ["Presente", "Imperfetto", "Passato", "Trapassato"],
            "Condizionale": ["Presente", "Passato"],
            "Imperativo": ["Presente"]
        }

        self.checkvars_mood = {}
        self.checkvars_tense = {}

        for i, mood in enumerate(self.moods.keys()):
            var = ctk.StringVar(value="on")
            self.checkvars_mood[mood] = var
            cb = ctk.CTkCheckBox(
                self, text=mood.capitalize(), variable=var, onvalue="on", offvalue="off",
                command=self.update_tense_visibility
            )
            row = 3 if i < 3 else 4
            col = i + 1 if i < 3 else i - 2
            cb.grid(row=row, column=col, sticky="nsew")

        self.label_tense = ctk.CTkLabel(self, text="Tense", font=("TkDefaultFont", 25))
        self.label_tense.grid(row=5, column=0, sticky="nsew")

        current_row = 6
        for mood, tenses in self.moods.items():
            label = ctk.CTkLabel(self, text=mood.capitalize(), font=("TkDefaultFont", 18))
            label.grid(row=current_row, column=1, sticky="nsew")

            self.checkvars_tense[mood] = {}

            for j, tense in enumerate(tenses):
                var = ctk.StringVar(value="on")
                self.checkvars_tense[mood][tense] = var
                cb = ctk.CTkCheckBox(
                    self, text=tense,
                    variable=var, onvalue="on", offvalue="off",
                    command=lambda m=mood: self.check_mood_state(m)
                )
                cb.grid(row=current_row, column=2 + j, sticky="nsew")

            current_row += 1

        self.button_validate = ctk.CTkButton(
            self,
            text="Start",
            command=self.validate 
        )
        self.button_validate.grid(row=20, column=0, padx=20, pady=10)

    def check_mood_state(self, mood):
        all_off = all(var.get() == "off" for var in self.checkvars_tense[mood].values())
        self.checkvars_mood[mood].set("off" if all_off else "on")

    def update_tense_visibility(self):
        for mood, tenses in self.checkvars_tense.items():
            mood_val = self.checkvars_mood[mood].get()
            for tense, var in tenses.items():
                if mood_val == "off":
                    var.set("off")
                elif mood_val == "on" and var.get() == "off":
                    var.set("on")

    def validate(self):
        selected_moods = []
        selected_tenses = {}

        for mood, mood_var in self.checkvars_mood.items():
            if mood_var.get() == "on":
                selected_moods.append(mood)
                selected_tenses[mood] = []
                for tense, tense_var in self.checkvars_tense[mood].items():
                    if tense_var.get() == "on":
                        selected_tenses[mood].append(tense)

        conjugation_frame = self.controller.frames["conjugation"]
        conjugation_frame.load_options(selected_moods, selected_tenses)

        self.controller.show_frame("conjugation")
