# Author: Dina Hassanein (22066792)

from api import URL, API, State

import tkinter as tk
import customtkinter as ctk
import ttkbootstrap as ttkb
import pywinstyles
from PIL import ImageTk


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.custom_font = ctk.CTkFont(family="Oswald", size=20)
        self.input_font = ctk.CTkFont(family="Dosis Semibold", size=16)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        login_frame = ttkb.Frame(self)
        login_frame.grid(row=0, column=0)

        top = ctk.CTkLabel(self, bg_color='#2b2b2b', height=100, text='')
        top.grid(row=0, column=0, sticky="ew")

        self.canvas = ttkb.Canvas(self, bg="black", width=700, height=700)
        self.canvas.grid(row=1, column=0)

        self.image = ImageTk.PhotoImage(file="gui/assets/background.jpg", size=(430, 400))
        self.title = ImageTk.PhotoImage(file="gui/assets/title.png")
        

        self.canvas.create_image(350, 350, image=self.image)

        user_text = self.canvas.create_text(120, 350, fill="white", text="Username")
        self.canvas.itemconfig(user_text, font=("Dosis Semibold", 23))
        
        pass_text = self.canvas.create_text(120, 430, fill="white", text="Password")
        self.canvas.itemconfig(pass_text, font=("Dosis Semibold", 23))
        
        self.canvas.create_image(350, 150, image=self.title)

        label = ctk.CTkLabel(self.canvas, text='', bg_color='#8b3bec', height=0)
        self.canvas.create_window(50, 50, anchor="center", window=label)

        username_entry = ctk.CTkEntry(master=self.canvas, textvariable=self.username,
                                      width=250, height=35, bg_color="#af2de7",
                                      font=self.input_font)
        username_entry.place(x=190, y=218)

        password_entry = ctk.CTkEntry(master=self.canvas, textvariable=self.password,
                                      width=250, height=35, show="•", bg_color="#af2de7",
                                      font=self.input_font)
        password_entry.place(x=190, y=275)

        login_btn = ctk.CTkButton(master=self.canvas, text="  LOGIN →", command=self.handle_input,
                                  font=self.custom_font, width=200, fg_color='#333333', bg_color=
                                  "#af2de7")
        login_btn.place(relx= 0.04, rely=0.8)

        back_btn = ctk.CTkButton(master=self.canvas, text="PREVIOUS PAGE",
            command=lambda: self.controller.goto("ChooseBranch"),
            font=self.custom_font, width=200, fg_color='#333333',
            bg_color="#af2de7")
        back_btn.place(relx= 0.55, rely=0.8)

        self.message = self.canvas.create_text(390, 510, fill="#330026", font="Dosis 20 bold",
                   text="")
        
        pywinstyles.set_opacity(username_entry, color="#af2de7")
        pywinstyles.set_opacity(password_entry, color="#af2de7")
        pywinstyles.set_opacity(login_btn, color="#af2de7")
        pywinstyles.set_opacity(back_btn, color="#af2de7")

    def goto(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        frame.tkraise()

    def handle_input(self):
        print("The branch id is", State.branch_id)
        if State.branch_id is not None:
            branch_id = State.branch_id

            branch_users_res = API.post(f"{URL}/branches/{branch_id}/users")
            branch_users = branch_users_res.json()

            if self.username.get() != "admin":
                for user in branch_users["data"]["users"]:
                    found = user["username"] == self.username.get()
                    print(found)

                    if found:
                        break

                if not found:
                    self.canvas.itemconfig(self.message, text="This user doesn't \
                                           work at this branch.")
                    return
                
        login_data = {"username": self.username.get(),
                      "password": self.password.get()}
        login = API.post(f"{URL}/login", json=login_data)

        State.is_ui_rendered = False

        match login.status_code:
            case 200:
                self.canvas.itemconfig(self.message, text="")

                username = login_data["username"]
                user_data_res = API.post(
                    f"{URL}/users/{username}", json=username)
                user_data = user_data_res.json()

                State.role_id = user_data["data"]["role"]["id"]
                State.username = username

                self.username.set("")
                self.password.set("")

                self.controller.goto("MainPage")

            case 401:
                self.canvas.itemconfig(self.message, text="Invalid Credentials")