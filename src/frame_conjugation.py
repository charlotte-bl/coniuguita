import customtkinter as ctk
from conjugator import create_verb

class ConjugationFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.corrected = False
        self.current_verb = None
        self.moods = ["Indicativo", "Condizionale", "Congiuntivo", "Imperativo", "Participio", "Gerundio"]
        self.tenses_per_mood = {
                    "Infinito": ["Presente", "Passato"],
                    "Participio": ["Presente", "Passato"],
                    "Gerundio": ["Presente", "Passato"],
                    "Indicativo": ["Presente", "Imperfetto", "Passato remoto", "Futuro semplice", 
                                   "Passato prossimo", "Trapassato prossimo", "Trapassato remoto", "Futuro anteriore"],
                    "Congiuntivo": ["Presente", "Imperfetto", "Passato", "Trapassato"],
                    "Condizionale": ["Presente", "Passato"],
                    "Imperativo": ["Presente"]
                }

        self.label_title = ctk.CTkLabel(self, text="Coniuguita", font=("TkDefaultFont", 30))
        self.label_title.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="nsew")

        self.label_verb = ctk.CTkLabel(self, text="", width=400,font=("TkDefaultFont", 18))
        self.label_verb.grid(row=1, column=0, padx=15, pady=10, sticky="e")

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Type your answer here",width=500)
        self.entry_user.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.entry_user.bind("<Return>", self.handle_enter_key)

        self.label_correction = ctk.CTkLabel(self, text="", font=("TkDefaultFont", 14))
        self.label_correction.grid(row=2, column=0, columnspan=3, pady=(5, 15), sticky="nsew")

        self.button_submit = ctk.CTkButton(self, text="Submit", command=self.check_answer)
        self.button_submit.grid(row=1, column=2, padx=10, pady=10)

        self.button_menu = ctk.CTkButton(
            self,
            text="Back to menu",
            command=lambda: self.controller.show_frame("menu")
        )
        self.button_menu.grid(row=3, column=1, padx=10, pady=10)

        self.button_next = ctk.CTkButton(self, text="Skip", command=self.load_new_verb)
        self.button_next.grid(row=1, column=3, padx=10, pady=10)

        self.load_new_verb()

    def handle_enter_key(self, event=None):
        if not self.corrected:
            self.check_answer()
        else:
            self.load_new_verb()

    def check_answer(self):
        user_input = self.entry_user.get().strip().lower()
        correct = self.current_verb.correct_form.strip().lower()

        if user_input == correct:
            self.label_correction.configure(text="✅ Correct", text_color="green")
        else:
            self.label_correction.configure(
                text=f"❌ Answer: {self.current_verb.correct_form}",
                text_color="red"
            )

        self.corrected = True

    def load_new_verb(self):
        self.current_verb = create_verb(moods=self.moods, tenses_per_mood=self.tenses_per_mood)
        verb_display = f"{self.current_verb.infinitive_translation} — {self.current_verb.mood} {self.current_verb.tense}"
        if self.current_verb.person:
            verb_display += f", {self.current_verb.person}"
        self.label_verb.configure(text=verb_display)
        self.label_correction.configure(text="")
        self.entry_user.delete(0, "end")
        self.entry_user.focus_set()
        self.corrected = False

    def load_options(self, moods, tenses_per_mood):
        self.moods = moods
        self.tenses_per_mood = tenses_per_mood
        self.load_new_verb()
