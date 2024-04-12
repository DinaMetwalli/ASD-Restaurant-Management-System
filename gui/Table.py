# Author: Dina Hassanein (22066792)
from tkinter import *
from CTkTable import *
import customtkinter as ctk

from api import API, URL, State


class TablesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tab_view = TableView(master=self, command=self.on_tab_selected)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

    def on_tab_selected(self):
        selected_tab = self.tab_view.get()
        
        if selected_tab == "View Tables":
            self.tab_view.load_data()
        if selected_tab == "Create Table":
            self.tab_view.create_msg.configure(text="")

class TableView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("View Tables")
        self.add("Create Table")
        self.add("Update Table")

        self.font = ctk.CTkFont(family="Dosis Semibold", size=20)

        self.view_tables()
        self.create_table()
        self.update_table()

    def load_data(self):
        if State.branch_id is None:
            return
        
        value = [["Number", "Capacity"]]

        for i in range(1, len(self.table_list.values)):
            if len(self.table_list.values) > 1:
                self.table_list.delete_row(index=i)

        branch_id = State.branch_id
        all_tables_res = API.post(
            f"{URL}/branches/{branch_id}/tables")
        all_tables = all_tables_res.json()
        
        global table_data
        table_data = []

        for table in all_tables["data"]["tables"]:
            value.append([table["number"], table["capacity"]])
            table_data.append(table["number"])

        for i in range(0, len(value)):
            self.table_list.add_row(index=i, values=value[i])
        
        self.table_list.delete_row(index=-1)

    def on_press(self, data):
        self.table = data["value"]
        if data["column"] != 0 or data["row"] == 0:
            self.delete_button.configure(state="disabled")
            self.update_button.configure(state="disabled")
        else:
            self.delete_button.configure(state="normal")
            self.update_button.configure(state="normal")

    def view_tables(self):
        self.tab("View Tables").grid_rowconfigure(0, minsize=700)

        window = ctk.CTkFrame(master=self.tab("View Tables"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="View All Tables",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=window,
                                                       width=720, height=350)
        self.scrollable_frame.grid(row=1, column=0, padx=(45, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.value = [["Number", "Capacity"]]
        self.table_list = CTkTable(master=self.scrollable_frame, column=2,
                              row=1, hover=True, command=self.on_press,
                              values=self.value)
        self.table_list.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        self.load_data()

        self.view_frame = ctk.CTkFrame(master=self.tab("View Tables"),
                                       fg_color="#333333")
        self.view_frame.grid(row=2, column=0, sticky="sew")

        self.update_button = ctk.CTkButton(master=self.view_frame,
                                      text='Update Table', command= lambda:
                                      self.configure_update(self.table))
        self.update_button.grid(row=0, column=0, pady=(0,10), padx=10)
        self.update_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete Table', command= lambda:
                                      self.delete_record(self.table))
        self.delete_button.grid(row=0, column=1, padx=10, pady=(0,10))
        self.delete_button.configure(state="disabled")

        self.delete_all_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete All Records', command=
                                      self.delete_all_records)
        self.delete_all_button.grid(row=0, column=2, padx=10, pady=(0,10))

    def configure_update(self, table):
        self.updated_table = table
        self.set("Update Table")

        self.update_label.configure(text=f"Table to be updated: Table No. {self.updated_table}")
        self.table_update_btn.configure(state="normal")
        self.new_capacity_entry.configure(state="normal")
        self.update_msg.configure(text="")

    def delete_record(self, number):
        branch_id = State.branch_id
        
        API.post(f"{URL}/branches/{branch_id}/tables/{number}/delete")
        
        self.load_data()

        self.delete_button.configure(state="disabled")

    def delete_all_records(self):
        branch_id = State.branch_id
        
        if branch_id is None:
            return
        
        for number in table_data:
            API.post(f"{URL}/branches/{branch_id}/tables/{number}/delete")
        
        self.load_data()
        self.delete_button.configure(state="disabled")

    def create_table(self):
        self.table_number = ctk.IntVar()
        self.table_capacity = ctk.IntVar()

        self.tab("Create Table").grid_rowconfigure(0, minsize=700)
        
        window = ctk.CTkFrame(master=self.tab("Create Table"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="Create a table",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.table_label = ctk.CTkLabel(master=window, text='Table Number')
        self.table_label.grid(row=1, column=0, padx=20, pady=5, sticky="nw")

        self.table_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.table_number, width=350)
        self.table_entry.grid(row=1, column=0, padx=(150,0), pady=5, sticky="nw")

        self.capacity_label = ctk.CTkLabel(master=window, text='Table Capacity')
        self.capacity_label.grid(row=2, column=0, padx=20, pady=5, sticky="nw")

        self.capacity_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.table_capacity, width=350)
        self.capacity_entry.grid(row=2, column=0, padx=(150,0), pady=5, sticky="nw")

        self.create_msg = ctk.CTkLabel(master=window, text="")
        self.create_msg.grid(row=3, column=0, padx=(150,0), pady=5, sticky="nw")

        self.create_frame = ctk.CTkFrame(master=self.tab("Create Table"),
                                         fg_color="#333333")
        self.create_frame.grid(row=1, column=0, sticky="sew")

        create_button = ctk.CTkButton(master=self.create_frame,
                                      text='Create Table',
                                      command=self.add_record)
        create_button.grid(padx=10, pady=(0,10), row=0, column=0)

    def add_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.create_msg.configure(text="User must be logged into a branch"
                                      " first before editing branch data.")
        
        number = self.table_number.get()
        capacity = self.table_capacity.get()

        table_info = {"table_number": number, "capacity": capacity}
        
        create = API.post(f"{URL}/branches/{branch_id}/tables/create", json=table_info)
        match create.status_code:
            case 200:
                self.create_msg.configure(text="Table Created Successfully")
                self.table_number.set("")
                self.table_capacity.set("")
            case 400 | 409:
                self.create_msg.configure(text=f"Error: {create.json()["message"]}")

    def update_table(self):
        self.new_capacity = ctk.IntVar()

        self.tab("Update Table").grid_rowconfigure(0, minsize=700)

        window = ctk.CTkFrame(master=self.tab("Update Table"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="Update A Table",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.update_label = ctk.CTkLabel(master=window,
                                      text="Please select a table first")
        self.update_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.new_capacity_label = ctk.CTkLabel(master=window, text="New Table Capacity")
        self.new_capacity_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.new_capacity_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.new_capacity, width=350)
        self.new_capacity_entry.grid(row=2, column=0, padx=(160,0), pady=5, sticky="w")
        
        self.update_msg = ctk.CTkLabel(master=window, text="")
        self.update_msg.grid(row=3, column=0, padx=(160,0), pady=5, sticky="w")

        self.update_frame = ctk.CTkFrame(master=self.tab("Update Table"), fg_color="#333333")
        self.update_frame.grid(row=4, column=0, sticky="sew")

        self.table_update_btn = ctk.CTkButton(master=self.update_frame,
                                      text='Update Table', command=lambda:
                                      self.update_record(self.updated_table))
        self.table_update_btn.grid(pady=(0,10), padx=10, row=0, column=0)
        
        self.table_update_btn.configure(state="disabled")    
        self.new_capacity_entry.configure(state="disabled")

    def update_record(self, table_num):
        branch_id = State.branch_id
        capacity_data = self.new_capacity_entry.get()

        set_capacity = API.post(
            f"{URL}/branches/{branch_id}/tables/{table_num}/set/capacity", json={"capacity": capacity_data})
        
        match set_capacity.status_code:
            case 200:
                self.new_capacity.set("")
                self.update_msg.configure(text="Table Capacity Set Successfully")
                self.update_label.configure(text="Please select a table first")
                self.table_update_btn.configure(state="disabled")
                self.new_capacity_entry.configure(state="disabled")
                self.update_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")
            case 400 | 409:
                self.update_msg.configure(text=f"Error: {set_capacity.json()["message"]}")