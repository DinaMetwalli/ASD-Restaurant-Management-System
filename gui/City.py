# Author: Dina Hassanein (22066792)
from tkinter import *
from CTkTable import *
import customtkinter as ctk

from api import API, URL

class CitiesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.tab_view = CityView(master=self, command=self.on_tab_selected)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

    def on_tab_selected(self):
        selected_tab = self.tab_view.get()
        if selected_tab == "View Cities":
            self.tab_view.load_data()
        if selected_tab == "Create City":
            self.tab_view.create_msg.configure(text="")
        if selected_tab == "Update City":
            self.tab_view.update_msg.configure(text="")

class CityView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create notebook tabs
        self.add("View Cities")
        self.add("Create City")
        self.add("Update City")

        self.font = ctk.CTkFont(family="Dosis Semibold", size=20)

        self.create_city()
        self.view_cities()
        self.update_city()

    def load_data(self):
        value = [["City Name"]]

        for i in range(1, len(self.table.values)):
            if len(self.table.values) > 1:
                self.table.delete_row(index=i)

        all_cities_res = API.post(f"{URL}/cities")
        all_cities = all_cities_res.json()
        
        global city_data
        city_data = {}

        for city in all_cities["data"]["cities"]:
            value.append([city["name"]])
            data = {city["name"]: city["id"]}
            city_data.update(data)

        for i in range(0, len(value)):
            self.table.add_row(index=i, values=value[i])
        
        self.table.delete_row(index=-1)

    def on_press(self, data):
        self.city = data["value"]
        if self.city != "City Name":
            self.update_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            self.update_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def view_cities(self):

        self.tab("View Cities").columnconfigure((1, 2), minsize=1000)
        self.tab("View Cities").rowconfigure(2, minsize=245)

        self.label = ctk.CTkLabel(master=self.tab("View Cities"), text="View all cities",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.tab("View Cities"),
                                                       width=720, height=350)
        self.scrollable_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.value = [["City Name"]]
        self.table = CTkTable(master=self.scrollable_frame, column=1,
                              row=1, hover=True, command=self.on_press,
                              values=self.value)
        self.table.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        self.load_data()

        self.view_frame = ctk.CTkFrame(master=self.tab("View Cities"),
                                       fg_color="#333333")
        self.view_frame.grid(row=2, column=0, sticky="sew", pady=(0,10), padx=10)

        self.update_button = ctk.CTkButton(master=self.view_frame,
                                      text='Update City', command= lambda:
                                      self.configure_update(self.city))
        self.update_button.grid(row=0, column=0, padx=10)
        self.update_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete City', command= lambda:
                                      self.delete_record(self.city))
        self.delete_button.grid(row=0, column=1, padx=10)
        self.delete_button.configure(state="disabled")

        self.delete_all_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete All Records', command=
                                      self.delete_all_records)
        self.delete_all_button.grid(row=0, column=2, padx=10)

    def configure_update(self, city):
        self.updated_city = city
        self.set("Update City")

        self.update_label.configure(text=f"City to be updated: {self.updated_city}")
        self.city_update_btn.configure(state="normal")
        self.name_entry.configure(state="normal")
        self.update_msg.configure(text="")

    def delete_record(self, city):
        city_id = city_data[city]
        API.post(f"{URL}/cities/{city_id}/delete", json=city_id)
        
        self.load_data()

        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def delete_all_records(self):
        cities_ids = []
        for record in city_data:
            cities_ids.append(city_data[f"{record}"])
        for id in cities_ids:
            API.post(f"{URL}/cities/{id}/delete", json=id)
        
        self.load_data()
        
        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def create_city(self):
        self.city_name = ctk.StringVar()

        self.tab("Create City").columnconfigure((0, 1, 2), minsize=1000)
        self.tab("Create City").rowconfigure(3, minsize=700)

        self.label = ctk.CTkLabel(master=self.tab("Create City"), text="Create a city",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.city_label = ctk.CTkLabel(master=self.tab("Create City"), text='City Name')
        self.city_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.city_entry = ctk.CTkEntry(master=self.tab("Create City"), textvariable=
                                       self.city_name, width=350)
        self.city_entry.grid(row=1, column=0, padx=(100,0), pady=5, sticky="w")

        self.create_msg = ctk.CTkLabel(master=self.tab("Create City"), text="")
        self.create_msg.grid(row=2, column=0, padx=(100,0), pady=5, sticky="w")

        self.create_frame = ctk.CTkFrame(master=self.tab("Create City"), fg_color="#333333")
        self.create_frame.grid(row=3, column=0, sticky="sew", pady=(0,10), padx=10)

        create_button = ctk.CTkButton(master=self.create_frame,
                                      text='Create City',
                                      command=self.add_record)
        create_button.grid(padx=10, row=0, column=0)

    def add_record(self):
        city = (self.city_name.get())
        city_data = {"name": city}
        create = API.post(f"{URL}/cities/create", json=city_data)
        match create.status_code:
            case 200:
                self.create_msg.configure(text="City Created Successfully")
                self.city_name.set("")
            case 400 | 409:
                self.create_msg.configure(text=f"Invalid City Name: {create.json()["message"]}")

    def update_city(self):
        self.new_name = ctk.StringVar()

        self.tab("Update City").columnconfigure((0, 1, 2), minsize=1000)
        self.tab("Update City").rowconfigure(4, minsize=630)

        self.label = ctk.CTkLabel(master=self.tab("Update City"), text="Update a city",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.update_label = ctk.CTkLabel(master=self.tab("Update City"),
                                      text="Please select a city first")
        self.update_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.label = ctk.CTkLabel(master=self.tab("Update City"), text="New City Name")
        self.label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.name_entry = ctk.CTkEntry(master=self.tab("Update City"), textvariable=
                                       self.new_name, width=350)
        self.name_entry.grid(row=2, column=0, padx=(160,0), pady=5, sticky="w")
        
        self.update_msg = ctk.CTkLabel(master=self.tab("Update City"), text="")
        self.update_msg.grid(row=3, column=0, padx=(160,0), pady=5, sticky="w")

        self.update_frame = ctk.CTkFrame(master=self.tab("Update City"), fg_color="#333333")
        self.update_frame.grid(row=4, column=0, sticky="sew", pady=(0,10), padx=10)

        self.city_update_btn = ctk.CTkButton(master=self.update_frame,
                                      text='Update City', command=lambda:
                                      self.update_record(self.updated_city))
        self.city_update_btn.grid(padx=10, row=0, column=0)
        
        self.city_update_btn.configure(state="disabled")    
        self.name_entry.configure(state="disabled")

    def update_record(self, to_update):
        city_id = city_data[to_update]
        name_data = self.new_name.get()

        set_name = API.post(
            f"{URL}/cities/{city_id}/set/name", json={"name": name_data})
        
        match set_name.status_code:
            case 200:
                self.new_name.set("")
                self.update_msg.configure(text="City Name Set Successfully")
                self.update_label.configure(text="Please select a city first")
                self.city_update_btn.configure(state="disabled")
                self.name_entry.configure(state="disabled")
                self.update_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")
            case 400 | 409:
                self.update_msg.configure(text=f"Invalid Entry: {set_name.json()["message"]}")
