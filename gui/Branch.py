# Author: Dina Hassanein (22066792)
from tkinter import *
from CTkTable import *
import customtkinter as ctk
import pywinstyles

from api import API, URL, State


class BranchesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.tab_view = BranchView(master=self, command=self.on_tab_selected)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

    def on_tab_selected(self):
        selected_tab = self.tab_view.get()
        if selected_tab == "View Branches":
            self.tab_view.load_data()
        if selected_tab == "Create Branch":
            self.tab_view.create_msg.configure(text="")
            self.tab_view.create_dropdown()
        if selected_tab == "Update Branch":
            self.tab_view.update_msg.configure(text="")
            self.tab_view.create_update_dropdown()

class BranchView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create notebook tabs
        self.add("View Branches")
        self.add("Create Branch")
        self.add("Update Branch")

        self.font = ctk.CTkFont(family="Dosis Semibold", size=20)

        self.create_branch()
        self.view_branches()
        self.update_branch()

    def load_data(self):

        value = [["Branch Name", "Address", "City"]]

        for i in range(1, len(self.table.values)):
            if len(self.table.values) > 1:
                self.table.delete_row(index=i)

        all_branches_res = API.post(f"{URL}/branches")
        all_branches = all_branches_res.json()

        global branch_data
        branch_data = {}

        for branch in all_branches["data"]["branches"]:
            address = API.post(
                f"{URL}/branches/{branch["id"]}").json()["data"]["address"]
            value.append([branch["name"], address, branch["city"]["name"]])
            data = {branch["name"]: branch["id"]}
            branch_data.update(data)

        for i in range(0, len(value)):
            self.table.add_row(index=i, values=value[i])
        
        self.table.delete_row(index=-1)

    def on_press(self, data):
        if data["column"] != 0 or data["row"] == 0:
            self.update_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
        else:
            self.branch = data["value"]
            self.update_button.configure(state="normal")
            self.delete_button.configure(state="normal")

    def view_branches(self):
        self.tab("View Branches").columnconfigure((1, 2), minsize=1000)
        self.tab("View Branches").rowconfigure(2, minsize=245)

        self.label = ctk.CTkLabel(master=self.tab("View Branches"), text="View all Branches",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.tab("View Branches"),
                                                       width=720, height=350)
        self.scrollable_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.value = [["Branch Name", "Address", "City"]]
        self.table = CTkTable(master=self.scrollable_frame, column=3, 
                              row=1, hover=True, command=self.on_press,
                              values=self.value)

        self.table.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        self.load_data()

        self.view_frame = ctk.CTkFrame(master=self.tab("View Branches"),
                                       fg_color="#333333")
        self.view_frame.grid(row=2, column=0, sticky="sew", pady=(0,10), padx=10)

        self.update_button = ctk.CTkButton(master=self.view_frame,
                                      text='Update Branch', command= lambda:
                                      self.configure_update(self.branch))
        self.update_button.grid(row=0, column=0, padx=10)
        self.update_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete Branch', command= lambda:
                                      self.delete_record(self.branch))
        self.delete_button.grid(row=0, column=1, padx=10)
        self.delete_button.configure(state="disabled")

        self.delete_all_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete All Branches', command=
                                      self.delete_all_records)
        self.delete_all_button.grid(row=0, column=2, padx=10)

    def configure_update(self, branch):
        self.updated_branch = branch
        self.set("Update Branch")

        self.update_label.configure(text=f"Branch to be updated: {self.updated_branch}"
                                    " - only fill in values you'd like to update")
        self.branch_update_btn.configure(state="normal")
        self.new_name_entry.configure(state="normal")
        self.update_msg.configure(text="")
        self.new_address_entry.configure(state="normal")
        self.new_city_entry.configure(state="normal")
        self.update_error_msg.configure(text="")

    def delete_record(self, branch):
        branch_id = branch_data[branch]
        API.post(f"{URL}/branches/{branch_id}/delete", json=branch_id)
        
        self.load_data()

        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def delete_all_records(self):
        branch_ids = []
        for record in branch_data:
            branch_ids.append(branch_data[f"{record}"])
        for id in branch_ids:
            API.post(f"{URL}/branches/{id}/delete", json=id)

        State.branch_id = None
        
        self.load_data()
        
        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def create_branch(self):
        self.drop_font = ctk.CTkFont(family="Dosis Semibold", size=16)

        self.branch_name = ctk.StringVar()
        self.branch_address = ctk.StringVar()

        self.tab("Create Branch").columnconfigure((0, 1, 2), minsize=1000)
        self.tab("Create Branch").rowconfigure(5, minsize=400)

        self.label = ctk.CTkLabel(master=self.tab("Create Branch"), text="Create a branch",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.branch_label = ctk.CTkLabel(master=self.tab("Create Branch"), text='Branch Name')
        self.branch_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.branch_entry = ctk.CTkEntry(master=self.tab("Create Branch"), textvariable=
                                       self.branch_name, width=350)
        self.branch_entry.grid(row=1, column=0, padx=(150,0), pady=5, sticky="w")

        self.address_label = ctk.CTkLabel(master=self.tab("Create Branch"), text='Address')
        self.address_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.address_entry = ctk.CTkEntry(master=self.tab("Create Branch"), textvariable=
                                       self.branch_address, width=350)
        self.address_entry.grid(row=2, column=0, padx=(150,0), pady=5, sticky="w")

        self.address_msg = ctk.CTkLabel(master=self.tab("Create Branch"),
                                        text="Address must follow format: 000 Street, City POS TCODE"
                                        "\nExample: 12a Oxford Rd, Manchester M1 5QA")
        self.address_msg.grid(row=2, column=0, padx=(150,0), pady=(65,0), sticky="w")

        self.label = ctk.CTkLabel(master=self.tab("Create Branch"), text="Choose City")
        self.label.grid(row=3, column=0, padx=20, pady=(30,10), sticky="nw")

        self.error_msg = ctk.CTkLabel(master=self.tab("Create Branch"), text="")
        self.error_msg.grid(row=4, column=0, padx=(150,0), pady=(30,10), sticky="nw")

        self.dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            self.dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]

        self.city_id = None
        combobox_var = ctk.StringVar(value="Choose City")
        self.drop = ctk.CTkComboBox(master=self.tab("Create Branch"), values=self.dropdown,
                                    variable=combobox_var, command=self.combobox_callback,
                                    width=200, height=35, font=self.drop_font,
                                    fg_color="#f2f2f2", bg_color="#333333",
                                    text_color='black')
        self.drop.grid(row=3, column=0, padx=(150,0), pady=25, sticky="nw")

        self.create_msg = ctk.CTkLabel(master=self.tab("Create Branch"), text="")
        self.create_msg.grid(row=4, column=0, padx=(150,0), pady=10, sticky="nw")

        self.create_frame = ctk.CTkFrame(master=self.tab("Create Branch"), fg_color="#333333")
        self.create_frame.grid(row=5, column=0, sticky="sew", pady=(0,10), padx=10)

        self.create_button = ctk.CTkButton(master=self.create_frame,
                                text='Create Branch',
                                command=self.add_record)
        self.create_button.grid(padx=10, row=0, column=0)

        pywinstyles.set_opacity(self.drop, color="#333333")

        self.create_dropdown()

    def combobox_callback(self, choice):
        self.city = city_data[choice]
        self.city_id = self.city

    def add_record(self):
        branch = self.branch_name.get()
        address = self.branch_address.get()

        if branch != "" and address != "" and self.city_id is not None:
            branch_data = {"name": branch, "address": address, "city_id": self.city}
        else:
            self.create_msg.configure(text="Please fill in all fields to create a branch")
            return
        
        create = API.post(f"{URL}/branches/create", json=branch_data)
        match create.status_code:
            case 200:
                self.create_msg.configure(text="Branch created successfully")
                self.branch_name.set("")
            case 400 | 409:
                self.create_msg.configure(text=f"{create.json()["message"]}")
    
    def update_branch(self):
        self.new_name = ctk.StringVar()
        self.new_address = ctk.StringVar()
        self.new_city = ctk.StringVar()

        self.tab("Update Branch").columnconfigure((0, 1, 2), minsize=1000)
        self.tab("Update Branch").rowconfigure(6, minsize=480)

        self.label = ctk.CTkLabel(master=self.tab("Update Branch"), text="Update a branch",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.update_label = ctk.CTkLabel(master=self.tab("Update Branch"),
                                      text="Please select a branch first")
        self.update_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.label = ctk.CTkLabel(master=self.tab("Update Branch"), text="New Branch Name")
        self.label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.new_name_entry = ctk.CTkEntry(master=self.tab("Update Branch"), textvariable=
                                       self.new_name, width=350)
        self.new_name_entry.grid(row=2, column=0, padx=(160,0), pady=5, sticky="nw")

        self.label = ctk.CTkLabel(master=self.tab("Update Branch"), text="New Branch Address")
        self.label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")

        self.new_address_entry = ctk.CTkEntry(master=self.tab("Update Branch"), textvariable=
                                       self.new_address, width=350)
        self.new_address_entry.grid(row=3, column=0, padx=(160,0), pady=5, sticky="nw")

        self.label = ctk.CTkLabel(master=self.tab("Update Branch"), text="New Branch City")
        self.label.grid(row=4, column=0, padx=20, pady=5, sticky="nw")

        self.dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            self.dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]

        self.new_city_id = None
        combobox_var = ctk.StringVar(value="Choose City")
        self.new_city_entry = ctk.CTkComboBox(master=self.tab("Update Branch"), values=self.dropdown,
                                    variable=combobox_var, command=self.update_combobox_callback,
                                    width=200, height=35, font=self.drop_font,
                                    fg_color="#f2f2f2", bg_color="#333333",
                                    text_color='black')
        self.new_city_entry.grid(row=4, column=0, padx=(160,0), pady=5, sticky="nw")

        self.update_msg = ctk.CTkLabel(master=self.tab("Update Branch"), text="")
        self.update_msg.grid(row=5, column=0, padx=(160,0), pady=5, sticky="nw")

        self.update_frame = ctk.CTkFrame(master=self.tab("Update Branch"), fg_color="#333333")
        self.update_frame.grid(row=6, column=0, sticky="sew", pady=(0,10), padx=10)

        self.branch_update_btn = ctk.CTkButton(master=self.update_frame,
                                      text='Update Branch', command=lambda:
                                      self.update_record(self.updated_branch))
        self.branch_update_btn.grid(padx=10, row=0, column=0)
        
        self.branch_update_btn.configure(state="disabled")
        self.new_name_entry.configure(state="disabled")
        self.new_address_entry.configure(state="disabled")
        self.new_city_entry.configure(state="disabled")

        self.update_error_msg = ctk.CTkLabel(master=self.tab("Update Branch"), text="")
        self.update_error_msg.grid(row=5, column=0, padx=(160,0), pady=(30,10), sticky="nw")

        self.create_update_dropdown()

    def update_combobox_callback(self, choice):
        self.update_city = city_data[choice]
        self.new_city_id = self.update_city

    def update_record(self, to_update):
        branch_id = branch_data[to_update]
        name_data = self.new_name.get()
        address_data = self.new_address.get()

        if name_data != "":
            set_name = API.post(
                f"{URL}/branches/{branch_id}/set/name", json={"name": name_data})
        
            match set_name.status_code:
                case 200:
                    self.configure_update_widgets()
                case 400 | 409:
                    self.update_msg.configure(text=f"Invalid Branch Name: {set_name.json()["message"]}")

        if address_data != "":
            set_address = API.post(
                f"{URL}/branches/{branch_id}/set/address", json={"address": address_data})
        
            match set_address.status_code:
                case 200:
                    self.configure_update_widgets()
                case 400 | 409:
                    self.update_msg.configure(text=f"Invalid Address: {set_name.json()["message"]}")

        if self.new_city_id is not None:
            set_city = API.post(
                f"{URL}/branches/{branch_id}/set/city", json={"city_id": self.city_id})
        
            match set_city.status_code:
                case 200:
                    self.configure_update_widgets()
                case 400 | 409:
                    self.update_msg.configure(text=f"Invalid City: {set_name.json()["message"]}")

    def configure_update_widgets(self):
        self.new_name.set("")
        self.update_msg.configure(text="Branch updated successfully")
        self.update_label.configure(text="Please select a branch first")
        self.branch_update_btn.configure(state="disabled")
        self.new_name_entry.configure(state="disabled")
        self.new_address_entry.configure(state="disabled")
        self.new_city_entry.configure(state="disabled")
        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
    
    def create_dropdown(self):
        self.dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            self.dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]
            
        if len(self.dropdown) == 0:
            self.drop.configure(state="disabled")
            self.branch_entry.configure(state="disabled")
            self.address_entry.configure(state="disabled")
            self.create_button.configure(state="disabled")
            self.error_msg.configure(text="Please create a city first"
                                     " to create or update branches")

            return
        
        self.drop.configure(state="normal", values=self.dropdown)
        self.branch_entry.configure(state="normal")
        self.address_entry.configure(state="normal")
        self.create_button.configure(state="normal")
        self.error_msg.configure(text="")

    def create_update_dropdown(self):
        self.update_dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            self.update_dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]

        print(len(self.update_dropdown))
            
        if len(self.dropdown) == 0:
            self.branch_update_btn.configure(state="disabled")
            self.new_city_entry.configure(state="disabled")
            self.new_name_entry.configure(state="disabled")
            self.new_address_entry.configure(state="disabled")
            self.update_error_msg.configure(text="Please create a city first"
                                            " to create or update branches")

            return

        self.new_city_entry.configure(values=self.update_dropdown)
        self.update_error_msg.configure(text="")