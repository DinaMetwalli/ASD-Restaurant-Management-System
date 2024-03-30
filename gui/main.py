# Author: Dina Hassanein (22066792)
"""Entry point for GUI application"""

import customtkinter as ctk
from customtkinter import CTk

from Login import LoginPage
from ChooseBranch import ChooseBranch
from MainPage import MainPage


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1050x680+0+0")
        self.title('Horizon Restaurants')
        self.resizable(1, 1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frame = None

        self.frames = {}
        for F in (LoginPage, ChooseBranch, MainPage):
            page_name = F.__name__
            self.frame = F(container, self)
            self.frames[page_name] = self.frame

        self.goto("ChooseBranch")

    def goto(self, page_name):
        """Display given page and hide current page"""
        if self.frame is not None:
            self.frame.pack_forget()
        self.frame = self.frames[page_name]
        self.frame.pack(fill="both", expand=False)
        self.frame.tkraise()
        self.on_show()

    def on_show(self):
        """Refresh page widgets when moving to a different page"""
        try:
            self.frame.on_show()
        except Exception:
            pass

if __name__ == "__main__":
    root = App()
    root.mainloop()
