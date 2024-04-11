# Author: Dina Hassanein (22066792)

import customtkinter as ctk
from PIL import Image, ImageTk

from Home import HomePage
from Staff import StaffPage
from City import CitiesPage
from Branch import BranchesPage
from Inventory import InventoryPage
from Table import TablesPage
from Menu import MenuPage
from Discounts import DiscountsPage
from Reservations import ReservationsPage

from api import API, URL, State

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_rowconfigure(0, weight=0, minsize=850)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)

        self.create_notebook_widget()

    def on_show(self):
        self.user_view()

    def user_view(self):
        user = State.username
        if user is not None:
            global user_data
            user_data_res = API.post(f"{URL}/users/{user}", json=user)
            user_data = user_data_res.json()
            if user_data["success"]:
                try:
                    for button in self.buttons:
                        button.grid_forget()
                except Exception:
                    pass

                match State.role_id:
                    case 0:
                        self.button1.grid(row=1, column=0, padx=20, pady=5, sticky="n")
                        # self.button7.grid(row=2, column=0, padx=20, pady=5, sticky="n")
                        self.button8.grid(row=3, column=0, padx=20, pady=5, sticky="n")
                    case 1:
                        self.button1.grid(row=1, column=0, padx=20, pady=5, sticky="n")
                        # self.button7.grid(row=2, column=0, padx=20, pady=5, sticky="n")
                        self.button8.grid(row=3, column=0, padx=20, pady=5, sticky="n")
                        # self.button9.grid(row=4, column=0, padx=20, pady=5, sticky="n")
                    case 2 | 3:
                        self.button1.grid(row=1, column=0, padx=20, pady=5, sticky="n")
                        # self.button7.grid(row=2, column=0, padx=20, pady=5, sticky="n")
                        # self.button5.grid(row=3, column=0, padx=20, pady=5, sticky="n")
                        self.button8.grid(row=4, column=0, padx=20, pady=5, sticky="n")
                    case 4:
                        self.button1.grid(row=1, column=0, padx=20, pady=5, sticky="n")
                        self.button3.grid(row=2, column=0, padx=20, pady=5, sticky="n")
                        self.button4.grid(row=3, column=0, padx=20, pady=5, sticky="n")
                        # self.button5.grid(row=4, column=0, padx=20, pady=5, sticky="n")
                        self.button6.grid(row=5, column=0, padx=20, pady=5, sticky="n")
                        # self.button7.grid(row=6, column=0, padx=20, pady=5, sticky="n")
                        self.button8.grid(row=7, column=0, padx=20, pady=5, sticky="n")
                        # self.button9.grid(row=8, column=0, padx=20, pady=5, sticky="n")
                    case 99:
                        self.button1.grid(row=1, column=0, padx=20, pady=5, sticky="n")
                        self.button2.grid(row=2, column=0, padx=20, pady=5, sticky="n")
                        self.button3.grid(row=3, column=0, padx=20, pady=5, sticky="n")
                        self.button4.grid(row=4, column=0, padx=20, pady=5, sticky="n")
                        # self.button5.grid(row=5, column=0, padx=20, pady=5, sticky="n")
                        self.button6.grid(row=6, column=0, padx=20, pady=5, sticky="n")
                        # self.button7.grid(row=7, column=0, padx=20, pady=5, sticky="n")
                        self.button8.grid(row=8, column=0, padx=20, pady=5, sticky="n")
                        # self.button9.grid(row=9, column=0, padx=20, pady=5, sticky="n")
            State.is_ui_rendered = True

    def logout(self):
        State.role_id = None
        State.username = None
        self.controller.goto("ChooseBranch")
        self.user_view()

    def create_notebook_widget(self):
        
        side_bar = ctk.CTkFrame(self, width=100)
        side_bar.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=0)
        side_bar.grid_rowconfigure(10, weight=1)
        
        self.frame1 = HomePage(self)
        self.frame2 = StaffPage(self)
        self.frame3 = CitiesPage(self)
        self.frame4 = BranchesPage(self)
        self.frame5 = InventoryPage(self)
        self.frame6 = TablesPage(self)
        self.frame7 = MenuPage(self)
        self.frame8 = DiscountsPage(self)
        self.frame9 = ReservationsPage(self)

        self.all_pages = [self.frame1, self.frame2, self.frame3, self.frame4,
                          self.frame5, self.frame6, self.frame7, self.frame8,
                          self.frame9]

        self.logo = ctk.CTkImage(Image.open("gui/assets/logo.png"), size=(170,25))
        self.logo_label = ctk.CTkLabel(side_bar, image=self.logo, text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        btn_w = 180
        btn_h = 30

        self.button1 = ctk.CTkButton(master=side_bar, text="Home", command=lambda:
                                    self.select_page(self.frame1), width=btn_w, height=btn_h)
        
        self.button2 = ctk.CTkButton(master=side_bar, text="Staff", command=lambda:
                                    self.select_page(self.frame2), width=btn_w, height=btn_h)
        
        self.button3 = ctk.CTkButton(master=side_bar, text="Cities", command=lambda:
                                    self.select_page(self.frame3), width=btn_w, height=btn_h)
        
        self.button4 = ctk.CTkButton(master=side_bar, text="Branch", command=lambda:
                                    self.select_page(self.frame4), width=btn_w, height=btn_h)
        
        self.button5 = ctk.CTkButton(master=side_bar, text="Inventory", command=lambda:
                                    self.select_page(self.frame5), width=btn_w, height=btn_h)
        
        self.button6 = ctk.CTkButton(master=side_bar, text="Tables", command=lambda:
                                    self.select_page(self.frame6), width=btn_w, height=btn_h)
        
        self.button7 = ctk.CTkButton(master=side_bar, text="Menu", command=lambda:
                                    self.select_page(self.frame7), width=btn_w, height=btn_h)
        
        self.button8 = ctk.CTkButton(master=side_bar, text="Discounts", command=lambda:
                                    self.select_page(self.frame8), width=btn_w, height=btn_h)
        
        self.button9 = ctk.CTkButton(master=side_bar, text="Reservations", command=lambda:
                                    self.select_page(self.frame9), width=btn_w, height=btn_h)
        
        

        self.buttons = [self.button1, self.button2, self.button3, self.button4,
                        self.button5, self.button6, self.button7, self.button8,
                        self.button9]

        for page in self.all_pages:
            page.grid(row=0, column=1, sticky="nsew")
        
        self.select_page(self.frame1)

        btn = ctk.CTkButton(master=side_bar, text="Logout", command=self.logout,
                            width=btn_w, height=btn_h)
        btn.grid(row=10, column=0, pady=(45,0))

        self.footer = ctk.CTkImage(Image.open("gui/assets/footer.jpg"), size=(1100,150))
        self.footer_label = ctk.CTkLabel(self, image=self.footer, text="")
        self.footer_label.grid(row=1, column=0, sticky="sew", columnspan=4, padx=7, pady=(0,7))
    
    def select_page(self, selected_page: ctk.CTkFrame):
        try:
            selected_page.load_records()
        except Exception:
            pass
        selected_page.grid(row=0, column=1,sticky="nsew")

        for page in self.all_pages:
            if page is not selected_page:
                page.grid_forget()