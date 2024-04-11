# Author: Dina Hassanein (22066792)
import customtkinter as ctk
from tkinter import *

from PIL import Image


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1, minsize=900)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        
    def create_widgets(self):
        self.frame = ctk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky="nsew",
                        rowspan=4, columnspan=4)
        
        self.frame.grid_columnconfigure(0, weight=1)

        self.inner_frame = ctk.CTkFrame(master=self.frame)
        self.inner_frame.grid(row=0, column=0, sticky="nsew",
                              rowspan=4, columnspan=4, padx=10, pady=10)

        image = ctk.CTkImage(Image.open("gui/assets/title_bg.jpg"), size=(530,350))
        self.image_label = ctk.CTkLabel(self.frame, image=image, text="")
        self.image_label.grid(row=0, column=0, sticky="n", columnspan=4, pady=12)