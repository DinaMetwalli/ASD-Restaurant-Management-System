from api import URL, API, State

import customtkinter as ctk
import tkinter as tk
from tkinter import *
import ttkbootstrap as ttkb
from PIL import Image, ImageTk
import pywinstyles

class ChooseBranch(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.drop = None

        self.custom_font = ctk.CTkFont(family="Oswald", size=20)
        self.drop_font = ctk.CTkFont(family="Dosis Semibold", size=16)

        main_frame = ttkb.Frame(self)
        main_frame.grid(row=0, column=0)

        top = ctk.CTkLabel(self, bg_color='#2b2b2b', height=100, text='')
        top.grid(row=0, column=0, sticky="ew")

        self.canvas = ttkb.Canvas(self, bg="black", width=700, height=700)
        self.canvas.grid(row=1, column=0)

        self.image = ImageTk.PhotoImage(file="gui/assets/background.jpg", size=(430, 400))
        self.title = ImageTk.PhotoImage(file="gui/assets/title.png")

        self.canvas.create_image(350, 350, image=self.image)

        text = self.canvas.create_text(150, 426, fill="white",
                   text="Choose A Branch")
        self.canvas.itemconfig(text, font=("Dosis Semibold", 23))
        
        self.canvas.create_image(350, 150, image=self.title)

        self.label = ctk.CTkLabel(self.canvas, text='', bg_color='#8b3bec', height=0)
        self.canvas.create_window(50, 50, anchor="center", window=self.label)

        self.dropdown = []

        self.branch_data = {}

        self.all_branches_res = API.post(f"{URL}/branches")
        self.all_branches = self.all_branches_res.json()

        for branch in self.all_branches["data"]["branches"]:
            self.dropdown.append(branch["name"])
            self.branch_data[branch["name"]] = branch["id"]
            
        self.combobox_var = ctk.StringVar(value="Choose a Branch")
        self.drop = ctk.CTkComboBox(master=self.canvas, values=self.dropdown,
                                    variable=self.combobox_var, command=self.combobox_callback,
                                    width=200, height=35, font=self.drop_font,
                                    fg_color="#f2f2f2", bg_color="#af2de7",
                                    text_color='black')
        self.drop.place(relx = 0.51, rely=0.575)

        self.message = ctk.CTkLabel(master=self.canvas, text="", font=self.drop_font,
                                    bg_color="black")
        self.message.place(relx = 0.51, rely = 0.67)

        branch_btn = ctk.CTkButton(master=self.canvas, text="  CHOOSE BRANCH →",
                                   command = self.handle_choice, font=self.custom_font, width=410,
                                   height=45, fg_color='#333333', bg_color="#af2de7")

        branch_btn.place(relx = 0.06, rely=0.8)

        pywinstyles.set_opacity(branch_btn, color="#af2de7")
        pywinstyles.set_opacity(self.drop, color="#af2de7")
        pywinstyles.set_opacity(self.message, color="black")
        pywinstyles.set_opacity(self.label, color="#8b3bec")

        self.on_show()

    def handle_choice(self):
        if State.branch_id is not None:
            self.message.configure(text="")
            self.controller.goto("LoginPage")
        else:
            self.message.configure(text="Please choose a branch first")

    def on_show(self):
        all_branches = API.post(f"{URL}/branches").json()
        if len(all_branches["data"]["branches"]) == 0:
            # Go to login page if no branches exist
            self.controller.goto("LoginPage")
            return

        State.is_ui_rendered = False

        self.dropdown = []
        self.branch_data = {}

        self.all_branches_res = API.post(f"{URL}/branches")
        self.all_branches = self.all_branches_res.json()

        for branch in self.all_branches["data"]["branches"]:
            self.dropdown.append(branch["name"])
            self.branch_data[branch["name"]] = branch["id"]

        self.drop.configure(values=self.dropdown)

    def combobox_callback(self, choice):
        State.branch_id = self.branch_data[choice]
