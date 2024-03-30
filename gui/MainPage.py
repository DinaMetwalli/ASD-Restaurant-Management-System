# Author: Dina Hassanein (22066792)
from gui_lib import Page
import tkinter as tk
import customtkinter as ctk
from tkinter import *
from tkinter import ttk


class MainTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        label = ctk.CTkLabel(self, text="Main Page")
        label.pack(padx=20, pady=20)

    def load_records(self):
        pass
