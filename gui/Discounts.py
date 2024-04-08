# Author: Dina Hassanein (22066792)
from tkinter import *
from CTkTable import *
import customtkinter as ctk

from api import API, URL, State


class DiscountsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.tab_view = DiscountView(master=self, command=self.on_tab_selected)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

    def on_tab_selected(self):
        selected_tab = self.tab_view.get()
        
        if selected_tab == "View Discounts":
            self.tab_view.load_data()
        if selected_tab == "Create Discount":
            self.tab_view.create_msg.configure(text="")

class DiscountView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("View Discounts")
        self.add("Create Discount")

        self.font = ctk.CTkFont(family="Dosis Semibold", size=20)

        self.view_discounts()
        self.create_discount()

    def load_data(self):
        if State.branch_id is None:
            return
        
        value = [["Discount Name", "Percentage", "Description"]]

        for i in range(1, len(self.table.values)):
            if len(self.table.values) > 1:
                self.table.delete_row(index=i)

        branch_id = State.branch_id
        all_discounts_res = API.post(
            f"{URL}/branches/{branch_id}/discounts")
        all_discounts = all_discounts_res.json()
        
        global discount_data
        discount_data = {}

        for discount in all_discounts["data"]["discounts"]:
            value.append([discount["name"], discount["multiplier"],
                          discount["description"]])
            data = {discount["name"]: discount["id"]}
            discount_data.update(data)

        print(value)
        for i in range(0, len(value)):
            self.table.add_row(index=i, values=value[i])
        
        self.table.delete_row(index=-1)

    def on_press(self, data):
        self.discount = data["value"]
        if self.discount != "Discount Name":
            self.delete_button.configure(state="normal")
        else:
            self.delete_button.configure(state="disabled")

    def view_discounts(self):

        self.tab("View Discounts").columnconfigure((1, 2), minsize=1000)
        self.tab("View Discounts").rowconfigure(2, minsize=245)

        self.label = ctk.CTkLabel(master=self.tab("View Discounts"), text="View all discounts",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.tab("View Discounts"),
                                                       width=720, height=350)
        self.scrollable_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.value = [["Discount Name", "Percentage", "Description"]]
        self.table = CTkTable(master=self.scrollable_frame, column=3,
                              row=1, hover=True, command=self.on_press,
                              values=self.value)
        self.table.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        self.load_data()

        self.view_frame = ctk.CTkFrame(master=self.tab("View Discounts"),
                                       fg_color="#333333")
        self.view_frame.grid(row=2, column=0, sticky="sew", pady=(0,10), padx=10)

        self.delete_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete Discount', command= lambda:
                                      self.delete_record(self.discount))
        self.delete_button.grid(row=0, column=0, padx=10)
        self.delete_button.configure(state="disabled")

        self.delete_all_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete All Records', command=
                                      self.delete_all_records)
        self.delete_all_button.grid(row=0, column=1, padx=10)

    def delete_record(self, discount):
        discount_id = discount_data[discount]
        branch_id = State.branch_id
        
        API.post(f"{URL}/branches/{branch_id}/discounts/{discount_id}/delete")
        
        self.load_data()

        self.delete_button.configure(state="disabled")

    def delete_all_records(self):
        discounts_ids = []
        branch_id = State.branch_id
        
        if branch_id is None:
            return
        
        for record in discount_data:
            discounts_ids.append(discount_data[record])
        for id in discounts_ids:
            API.post(f"{URL}/branches/{branch_id}/discounts/{id}/delete")
        
        self.load_data()
        
        self.delete_button.configure(state="disabled")

    def create_discount(self):
        self.discount_name = ctk.StringVar()
        self.multiplier = ctk.DoubleVar()
        self.description = ctk.StringVar()

        self.tab("Create Discount").columnconfigure((0, 1, 2), minsize=1000)
        self.tab("Create Discount").rowconfigure(5, minsize=585)

        self.label = ctk.CTkLabel(master=self.tab("Create Discount"), text="Create a discount",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.discount_label = ctk.CTkLabel(master=self.tab("Create Discount"), text='Discount Name')
        self.discount_label.grid(row=1, column=0, padx=20, pady=5, sticky="nw")

        self.discount_entry = ctk.CTkEntry(master=self.tab("Create Discount"), textvariable=
                                       self.discount_name, width=350)
        self.discount_entry.grid(row=1, column=0, padx=(150,0), pady=5, sticky="nw")

        self.multiplier_label = ctk.CTkLabel(master=self.tab("Create Discount"), text='Multiplier')
        self.multiplier_label.grid(row=2, column=0, padx=20, pady=5, sticky="nw")

        self.multiplier_entry = ctk.CTkEntry(master=self.tab("Create Discount"), textvariable=
                                       self.multiplier, width=350)
        self.multiplier_entry.grid(row=2, column=0, padx=(150,0), pady=5, sticky="nw")

        self.desc_label = ctk.CTkLabel(master=self.tab("Create Discount"), text='Description')
        self.desc_label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")

        self.desc_entry = ctk.CTkEntry(master=self.tab("Create Discount"), textvariable=
                                       self.description, width=350)
        self.desc_entry.grid(row=3, column=0, padx=(150,0), pady=5, sticky="nw")

        self.create_msg = ctk.CTkLabel(master=self.tab("Create Discount"), text="")
        self.create_msg.grid(row=4, column=0, padx=(150,0), pady=5, sticky="nw")

        self.create_frame = ctk.CTkFrame(master=self.tab("Create Discount"), fg_color="#333333")
        self.create_frame.grid(row=5, column=0, sticky="sew", pady=(0,10), padx=10)

        create_button = ctk.CTkButton(master=self.create_frame,
                                      text='Create Discount',
                                      command=self.add_record)
        create_button.grid(padx=10, row=0, column=0)

    def add_record(self):
        branch_id = State.branch_id
        name = self.discount_name.get()
        multiplier = self.multiplier.get()
        desc = self.description.get()

        discount_data = {"name": name, "multiplier": multiplier, "description": desc}
        print(discount_data)
        create = API.post(f"{URL}/branches/{branch_id}/discounts/create", json=discount_data)
        match create.status_code:
            case 200:
                self.create_msg.configure(text="Discount Created Successfully")
                self.discount_name.set("")
            case 400 | 409:
                self.create_msg.configure(text=f"Invalid Input: {create.json()["message"]}")