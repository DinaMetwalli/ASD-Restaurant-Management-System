# Author: Dina Hassanein (22066792)
from tkinter import *
from CTkTable import *
import customtkinter as ctk
import pywinstyles

from api import API, URL, State


class StaffPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tab_view = StaffView(master=self, command=self.on_tab_selected)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

    def on_tab_selected(self):
        selected_tab = self.tab_view.get()
        if selected_tab == "View Staff":
            self.tab_view.load_data()
        if selected_tab == "Create Staff":
            self.tab_view.create_msg.configure(text="")
        if selected_tab == "Update Staff":
            self.tab_view.update_msg.configure(text="")


class StaffView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create notebook tabs
        self.add("View Staff")
        self.add("Create Staff")
        self.add("Update Staff")

        self.font = ctk.CTkFont(family="Dosis Semibold", size=20)

        self.view_staff()
        self.create_staff()
        self.update_staff()

    def load_data(self):
        if State.branch_id is None:
            return
        
        value = [["Username", "Full Name", "Role", "Branch"]]

        for i in range(1, len(self.table.values)):
            if len(self.table.values) > 1:
                self.table.delete_row(index=i)

        branch_id = State.branch_id
        branch_users_res = API.post(f"{URL}/branches/{branch_id}/users")
        branch_users = branch_users_res.json()
        
        global staff_data
        staff_data = []

        for staff in branch_users["data"]["users"]:
            value.append([staff["username"], staff["full_name"],
                          staff["role"]["name"], staff["branch"]["name"]])
            staff_data.append(staff["username"])

        for i in range(0, len(value)):
            self.table.add_row(index=i, values=value[i])
        
        self.table.delete_row(index=-1)

    def on_press(self, data):
        if data["column"] != 0 or data["row"] == 0:
            self.update_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
        else:
            self.update_button.configure(state="normal")
            self.delete_button.configure(state="normal")
            self.user = data["value"]
            
        self.updated_staff = self.table.get(data["row"], 0)
            
    def view_staff(self):
        self.tab("View Staff").grid_rowconfigure(0, minsize=700)

        window = ctk.CTkFrame(master=self.tab("View Staff"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="View all Branch Staff",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=window,
                                                       width=720, height=350)
        self.scrollable_frame.grid(row=1, column=0, padx=(45, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.value = [["Username", "Full Name", "Role", "Branch"]]
        self.table = CTkTable(master=self.scrollable_frame, column=4, 
                              row=1, hover=True, command=self.on_press,
                              values=self.value)

        self.table.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        self.load_data()

        self.view_frame = ctk.CTkFrame(master=self.tab("View Staff"),
                                       fg_color="#333333")
        self.view_frame.grid(row=2, column=0, sticky="sew")

        self.update_button = ctk.CTkButton(master=self.view_frame,
                                      text='Update Staff', command= lambda:
                                      self.configure_update(self.updated_staff))
        self.update_button.grid(row=0, column=0, pady=(0,10), padx=10)
        self.update_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete Staff', command= lambda:
                                      self.delete_record(self.user))
        self.delete_button.grid(row=0, column=1, pady=(0,10), padx=10)
        self.delete_button.configure(state="disabled")

        self.delete_all_button = ctk.CTkButton(master=self.view_frame,
                                      text='Delete All Records', command=
                                      self.delete_all_records)
        self.delete_all_button.grid(row=0, column=2, pady=(0,10), padx=10)

    def configure_update(self, to_update):
        self.set("Update Staff")

        self.update_label.configure(text=f"Staff member to be updated: {to_update}"
                                    " - only fill in values you'd like to update")
        self.staff_update_btn.configure(state="normal")
        self.new_fullname_entry.configure(state="normal")
        self.update_drop.configure(state="normal")
        self.update_msg.configure(text="")

    def delete_record(self, username):
        for name in staff_data:
            if username == name:
                API.post(f"{URL}/users/{username}/delete", json=username)
        
        self.load_data()

        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def delete_all_records(self):
        for username in staff_data:
            API.post(f"{URL}/users/{username}/delete", json=username)
        
        self.load_data()
        
        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def create_staff(self):
        self.drop_font = ctk.CTkFont(family="Dosis Semibold", size=16)

        self.full_name = ctk.StringVar()
        self.username = ctk.StringVar()
        self.dropdown = ["Staff", "Frontend Staff", "Kitchen Staff",
                         "Chef", "Manager", "Admin"]
        self.password = ctk.StringVar()

        self.tab("Create Staff").grid_rowconfigure(0, minsize=700)

        window = ctk.CTkFrame(master=self.tab("Create Staff"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="Create a staff member",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.full_name_label = ctk.CTkLabel(master=window, text='Full Name')
        self.full_name_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.full_name_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.full_name, width=350)
        self.full_name_entry.grid(row=1, column=0, padx=(150,0), pady=5, sticky="w")

        self.username_label = ctk.CTkLabel(master=window, text='Username')
        self.username_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.username_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.username, width=350)
        self.username_entry.grid(row=2, column=0, padx=(150,0), pady=5, sticky="w")

        self.password_label = ctk.CTkLabel(master=window, text='Password')
        self.password_label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")

        self.password_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.password, width=350)
        self.password_entry.grid(row=3, column=0, padx=(150,0), pady=5, sticky="w")

        self.role_label = ctk.CTkLabel(master=window, text='Role')
        self.role_label.grid(row=4, column=0, padx=20, pady=10, sticky="nw")

        combobox_var = ctk.StringVar(value="Select Role")
        self.drop = ctk.CTkComboBox(master=window, values=self.dropdown,
                                    variable=combobox_var, command=self.combobox_callback,
                                    width=200, height=35, font=self.drop_font,
                                    fg_color="#f2f2f2", bg_color="#333333",
                                    text_color='black')
        self.drop.grid(row=4, column=0, padx=(150,0), pady=10, sticky="nw")

        self.error_msg = ctk.CTkLabel(master=window, text="")
        self.error_msg.grid(row=5, column=0, padx=(150,0), pady=(30,10), sticky="nw")

        self.create_msg = ctk.CTkLabel(master=window, text="")
        self.create_msg.grid(row=5, column=0, padx=(150,0), pady=10, sticky="nw")

        self.create_frame = ctk.CTkFrame(master=self.tab("Create Staff"), fg_color="#333333")
        self.create_frame.grid(row=6, column=0, sticky="sew")

        self.create_button = ctk.CTkButton(master=self.create_frame,
                                text='Create Staff',
                                command=self.add_record)
        self.create_button.grid(pady=(0,10), padx=10, row=0, column=0)

        pywinstyles.set_opacity(self.drop, color="#333333")

    def combobox_callback(self, choice):
        self.role_id = self.configure_role_type(choice)

    def add_record(self):
        full_name = self.full_name.get()
        username = self.username.get()
        password = self.password.get()

        if full_name != "" and username != "" and password != "" and self.role_id is not None:
            user_data = {"full_name": full_name, "username": username,
                         "password": password, "role_id": self.role_id}
        else:
            self.create_msg.configure(text="Please fill in all fields to create a staff member")
            return
        
        branch_id = State.branch_id
        create = API.post(f"{URL}/branches/{branch_id}/users/add", json=user_data)
        match create.status_code:
            case 200:
                self.create_msg.configure(text="Staff member created successfully")
                self.full_name.set("")
                self.username.set("")
                self.password.set("")
            case 400 | 409:
                self.create_msg.configure(text=f"{create.json()["message"]}")

    def update_staff(self):
        self.new_full_name = ctk.StringVar()
        self.dropdown = ["Staff", "Frontend Staff", "Kitchen Staff",
                         "Chef", "Manager", "Admin"]

        self.tab("Update Staff").grid_rowconfigure(0, minsize=700)

        window = ctk.CTkFrame(master=self.tab("Update Staff"),
                              fg_color="#333333", height=600)
        window.grid(row=0, column=0, sticky="n")
        window.columnconfigure((0, 1, 2), minsize=1000)

        self.label = ctk.CTkLabel(master=window, text="Update Staff Member",
                                  font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.update_label = ctk.CTkLabel(master=window,
                                      text="Please select a staff member first")
        self.update_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.new_fullname_label = ctk.CTkLabel(master=window, text="New Full Name")
        self.new_fullname_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.new_fullname_entry = ctk.CTkEntry(master=window, textvariable=
                                       self.new_full_name, width=350)
        self.new_fullname_entry.grid(row=2, column=0, padx=(150,0), pady=5, sticky="nw")

        self.new_role_label = ctk.CTkLabel(master=window, text="New Role")
        self.new_role_label.grid(row=3, column=0, padx=20, pady=10, sticky="nw")

        self.new_role = None
        combobox_var = ctk.StringVar(value="Select Role")
        self.update_drop = ctk.CTkComboBox(master=window, values=self.dropdown,
                                    variable=combobox_var, command=self.update_combobox_callback,
                                    width=200, height=35, font=self.drop_font,
                                    fg_color="#f2f2f2", bg_color="#333333",
                                    text_color='black')
        self.update_drop.grid(row=3, column=0, padx=(150,0), pady=10, sticky="nw")

        self.update_msg = ctk.CTkLabel(master=window, text="")
        self.update_msg.grid(row=4, column=0, padx=(150,0), pady=5, sticky="nw")

        self.update_error_msg = ctk.CTkLabel(master=window, text="")
        self.update_error_msg.grid(row=4, column=0, padx=(150,0), pady=(30,10), sticky="nw")

        self.update_frame = ctk.CTkFrame(master=self.tab("Update Staff"), fg_color="#333333")
        self.update_frame.grid(row=5, column=0, sticky="sew")

        self.staff_update_btn = ctk.CTkButton(master=self.update_frame,
                                      text='Update Staff', command=lambda:
                                      self.update_record(self.updated_staff))
        self.staff_update_btn.grid(pady=(0,10), padx=10, row=0, column=0)
        
        self.staff_update_btn.configure(state="disabled")
        self.new_fullname_entry.configure(state="disabled")
        self.update_drop.configure(state="disabled")

    def update_combobox_callback(self, choice):
        self.new_role = self.configure_role_type(choice)

    def update_record(self, to_update):
        full_name_data = self.new_full_name.get()
        role_id_data = self.new_role

        if full_name_data != "":
            set_full_name = API.post(
                f"{URL}/users/{to_update}/set/fullname",
                json={"full_name": full_name_data})
        
            match set_full_name.status_code:
                case 200:
                    self.configure_update_widgets()
                case 400 | 409:
                    self.update_msg.configure(text=f"Invalid Full Name: {set_full_name.json()["message"]}")

        if role_id_data is not None:
            set_role = API.post(
                f"{URL}/users/{to_update}/set/role",
                json={"role_id": role_id_data})
        
            match set_role.status_code:
                case 200:
                    self.configure_update_widgets()
                case 400 | 409:
                    self.update_msg.configure(text=f"Invalid Role Type: {set_role.json()["message"]}")

    def configure_update_widgets(self):
        self.new_full_name.set("")
        self.update_msg.configure(text="Staff member updated successfully")
        self.update_label.configure(text="Please select a staff member first")
        self.staff_update_btn.configure(state="disabled")
        self.new_fullname_entry.configure(state="disabled")
        self.update_drop.configure(state="disabled")
        self.update_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

    def configure_role_type(self, choice):
        self.role_id = None
        match choice:
            case "Admin":
                self.role_id = 99
            case "Manager":
                self.role_id = 4
            case "Chef":
                self.role_id = 3
            case "Kitchen Staff":
                self.role_id = 2
            case "Frontend Staff":
                self.role_id = 1
            case "Staff":
                self.role_id = 0
        return self.role_id