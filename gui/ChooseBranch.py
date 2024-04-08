from api import URL, API, State

import customtkinter as ctk
import tkinter as tk
from tkinter import *
import ttkbootstrap as ttkb
from PIL import Image, ImageTk
import pywinstyles

branch_data = None

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

        text = self.canvas.create_text(180, 426, fill="white",
                   text="Please choose a branch")
        self.canvas.itemconfig(text, font=("Dosis Semibold", 23))
        
        self.canvas.create_image(350, 150, image=self.title)

        label = ctk.CTkLabel(self.canvas, text='', bg_color='#8b3bec', height=0)
        self.canvas.create_window(50, 50, anchor="center", window=label)

        self.all_branches_res = API.post(f"{URL}/branches")
        self.all_branches = self.all_branches_res.json()

        self.on_show()

    def on_show(self):
        """Go to login page if no branches exist"""
        if len(self.all_branches["data"]["branches"]) == 0:
            self.controller.goto("LoginPage")
            return

        State.is_ui_rendered = False

        if self.drop is None:
            self.dropdown = []

            global branch_data
            branch_data = {}
            for branch in self.all_branches["data"]["branches"]:
                self.dropdown.append(branch["name"])
                branch_data[branch["name"]] = branch["id"]

            def combobox_callback(choice):
                State.branch_id = branch_data[choice]
            
            combobox_var = ctk.StringVar(value="Choose a Branch")

            self.drop = ctk.CTkComboBox(master=self.canvas, values=self.dropdown,
                                        variable=combobox_var, command=combobox_callback,
                                        width=200, height=35, font=self.drop_font,
                                        fg_color="#f2f2f2", bg_color="#af2de7",
                                        text_color='black')
            self.drop.place(relx = 0.51, rely=0.575)

            branch_btn = ctk.CTkButton(master=self.canvas, text="  CHOOSE BRANCH →",
            command=lambda: self.controller.goto("LoginPage"),
            font=self.custom_font, width=410,
            height=45, fg_color='#333333', bg_color="#af2de7")

            branch_btn.place(relx = 0.06, rely=0.8)

            pywinstyles.set_opacity(branch_btn, color="#af2de7")
            pywinstyles.set_opacity(self.drop, color="#af2de7")
