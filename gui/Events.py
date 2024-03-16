# Author: Dina Hassanein (22066792)
from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State
from datetime import datetime


class EventsPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = ViewEvents(notebook)
        self.frame2 = CreateEvent(notebook)
        # self.frame3 = UpdateEvent(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='View All Events')
        notebook.add(self.frame2, text='Create Event')
        # notebook.add(self.frame3, text='Update Event')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Events":
            self.frame1.load_records()
        if tab_text == "Create Event":
            self.frame2.fields['message']['text'] = ""
            self.frame1.load_records()
        if tab_text == "Update Event":
            self.frame1.load_records()
            self.frame2.fields['message']['text'] = ""


class ViewEvents(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('email', 'phone_number', 'start_time', 'end_time', 'type', 'address')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('email', text='Customer Email')
        self.tree.heading('phone_number', text='Phone Number')
        self.tree.heading('start_time', text='Start Time')
        self.tree.heading('end_time', text='End Time')
        self.tree.heading('type', text='Event Type')
        self.tree.heading('address', text='Address')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_events_res = API.post(
            f"{URL}/branches/{branch_id}/events")
        branch_events = branch_events_res.json()

        global event_data
        event_data = {}

        for event in branch_events["data"]["events"]:
            self.tree.insert('', 'end', values=(
                event["email"], event["phone_num"], event["start_time"],
                event["end_time"], event["type"], event["address"]))
            event_data[event["email"]] = event["id"]

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branch_id = State.branch_id
        for record in event_data:
            res = API.post(
                f"{URL}/branches/{branch_id}/events/{event_data[record]}/delete")
        self.load_records()


class CreateEvent(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.email = tk.StringVar()
        self.phone_number = tk.IntVar()
        self.start_time = tk.StringVar()
        self.end_time = tk.StringVar()
        self.type = tk.IntVar()
        self.address = tk.StringVar()

        self.fields = {}

        self.fields['email_label'] = ttk.Label(
            self, text='Customer Email:')
        self.fields['email'] = ttk.Entry(
            self, textvariable=self.email)
        self.fields['phone_number_label'] = ttk.Label(self, text='Phone Number:')
        self.fields['phone_number'] = ttk.Entry(self, textvariable=self.phone_number)
        self.fields['start_time_label'] = ttk.Label(self, text='Start Time:')
        self.fields['start_time'] = ttk.Entry(self, textvariable=self.start_time)
        self.fields['end_time_label'] = ttk.Label(self, text='End Time:')
        self.fields['end_time'] = ttk.Entry(self, textvariable=self.end_time)
        self.fields['type_label'] = ttk.Label(self, text='Type:')
        self.fields['type'] = ttk.Entry(self, textvariable=self.type)
        self.fields['address_label'] = ttk.Label(self, text='Event Address:')
        self.fields['address'] = ttk.Entry(self, textvariable=self.address)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Event', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        branch_id = State.branch_id

        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, \
            Choose a branch on login first to create branch items"
            return
        
        email = self.email.get()
        phone_number = self.phone_number.get()
        type = self.type.get()
        address = self.address.get()

        start_time = datetime.strptime(self.start_time.get(), '%d-%m-%Y %H:%M:%S')
        start_timestamp = start_time.timestamp()
        end_time = datetime.strptime(self.end_time.get(), '%d-%m-%Y %H:%M:%S')
        end_timestamp = end_time.timestamp()

        if email == "" or phone_number == "" or start_time is None or end_time is None or type == "" or address == "":
            self.fields['message']["text"] = "All fields must be filled."
            return
        else:
            event_info = {"email": email, "phone_number": phone_number, "start_timestamp": start_timestamp,
                          "end_timestamp": end_timestamp, "type": type, "address": address}
            create = API.post(
                f"{URL}/branches/{branch_id}/events/create", json=event_info)
            match create.status_code:
                case 200:
                    self.fields['message']["text"] = "Event Created Successfully"
                case 400 | 409 | 401:
                    self.fields['message']["text"] = create.json()[
                        "message"]