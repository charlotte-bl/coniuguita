import customtkinter as ctk
from frame_conjugation import ConjugationFrame
from frame_menu import MenuFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Coniuguita")

        self.geometry("1500x500")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("../ressources/cherry.json")

        self.bind("<Escape>", self.exit)

        # Adding pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.current_frame = None

        self.frames["menu"] = MenuFrame(self.container, self)
        self.frames["conjugation"] = ConjugationFrame(self.container, self)

        self.show_frame("menu")

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame = self.frames[frame_name]
        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame

    def exit(self, event=None):
        self.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()
