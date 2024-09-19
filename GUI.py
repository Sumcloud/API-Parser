from Logger  import Logger
from Configuration import Configuration
from Fetch import Fetch
from Parser import Parser
from Writer import Writer
from DatabaseCreator.SQLITE_Creator import CSVtoSQLite
from DatabaseCreator.POSTGRES_Creator import CSVtoSQL
from tkinter import *
from tkinter import ttk
import csv

class GUI:

    def __init__(self, configuration, logger, fetcher, parser, writer) -> None:
        self.logger : Logger = logger
        self.fetcher : Fetch = fetcher
        self.parser : Parser = parser
        self.writer : Writer = writer
        self.configuration : Configuration = configuration
        self.versions_screen : dict[str,int] = {}

        self.root = Tk()
        
        # Define frames
        self.credential_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.endpoint_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.versions_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.database_export = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.run_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)

        # Define input fields (credentials, endpoints, checkbox)

        self.username_entry : Entry
        self.password_entry : Entry
        self.URL_entry : Entry
        self.endpoint_selection : Listbox
        self.SQLite_option : Checkbutton
        self.POSTGRES_option: Checkbutton

        self.SQLite_Option_BOOL = BooleanVar()
        self.POSTGRES_option_BOOL = BooleanVar()


        self.initialize_frame()
        self.root.resizable(False, False)
        self.root.iconbitmap("Config/Static/app.ico")
        self.root.mainloop()

    def get_selected_endpoints(self) -> list[str]:
        selection = [str(self.endpoint_selection.get(i)).strip() for i in self.endpoint_selection.curselection()]

        if len(selection) != 0:
            return selection
        else:
            return self.get_endpoints()

    def set_versions_screen(self) -> list[tuple]:
        # Create the pop-out window
        version_window = Toplevel(self.root)
        version_window.title("Set Versions")
        version_window.geometry("400x800")

        # Create a frame to hold the endpoint list and version entries
        version_frame = Frame(version_window)
        version_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for the version window
        scrollbar = Scrollbar(version_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Canvas to hold the endpoint list and version entries for scrolling
        canvas = Canvas(version_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        # Create a frame inside the canvas to hold the actual widgets
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # List of endpoints
        endpoints = self.get_selected_endpoints()

        # Dictionary to store version entries
        version_entries = {}

        # Label and Entry for each endpoint and version
        for i, endpoint in enumerate(endpoints):
            endpoint_label = Label(inner_frame, text=endpoint)
            endpoint_label.pack(anchor='w', padx=10, pady=5)

            version_entry = Entry(inner_frame, width=10)
            version_entry.insert(0, self.versions_screen[endpoint])  # Default version number is 0
            version_entry.pack(anchor='w', padx=10, pady=5)
            
            # Store the entry widget in a dictionary with the endpoint as the key
            version_entries[endpoint] = version_entry

        # Update the scroll region to accommodate all widgets
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Button to confirm changes and return the values
        def save_versions():

            for endpoint, entry_widget in version_entries.items():
                version = int(entry_widget.get())
                self.versions_screen[endpoint] = version

            version_window.destroy()

        # Save button
        save_button = Button(version_window, text="Save Versions", command=save_versions)
        save_button.pack(pady=10)

        version_window.mainloop()

    def fetch_data(self):
        username : str = self.username_entry.get()
        password : str = self.password_entry.get()
        URL : str = self.URL_entry.get()

        selected_endpoints = self.get_selected_endpoints()
        sqlite_export = self.SQLite_Option_BOOL.get()
        postgres_export = self.POSTGRES_option_BOOL.get()

        print(username)
        print(password)
        print(URL)


        print(selected_endpoints)
        print(self.versions_screen)

        print(sqlite_export)
        print(postgres_export)

        # Get the version number

        length : int = len(selected_endpoints)

        for i in range(length) :
            data = self.fetcher.fetch(selected_endpoints[i], "false", username= username, password= password, url= URL, initial_version = self.versions_screen[selected_endpoints[i]] )

            if data.empty == True:
                self.writer.create_empty_file(data,selected_endpoints[i], False)
                continue

            if self.configuration.Filters[self.configuration.Endpoints[i]]['has_version'] == 0 or data['version'].max() == 0:
                data = self.parser.add_versioning(data, endpoint=selected_endpoints[i], deleted = False)

            data = self.parser.remove_duplicates(data,self.configuration.Endpoints[i])
            self.writer.write_data(data=data, endpoint=self.configuration.Endpoints[i], deleted=False)

        for i in range(length) :
            data = self.fetcher.fetch(selected_endpoints[i], "true", username= username, password= password, url= URL, initial_version = self.versions_screen[selected_endpoints[i]])

            if data.empty == True:
                self.writer.create_empty_file(data, self.configuration.Endpoints[i], True)
                continue

            if self.configuration.Filters[self.configuration.Endpoints[i]]['has_version'] == 0 or data['version'].max() == 0:
                data = self.parser.add_versioning(data, self.configuration.Endpoints[i], True)

            data = self.parser.remove_duplicates(data,self.configuration.Endpoints[i])
            self.writer.write_data(data=data, endpoint=self.configuration.Endpoints[i], deleted=True)

        if sqlite_export == True:
            CSVtoSQLite()
        
        if postgres_export == True:
            CSVtoSQL()
            

    def get_endpoints(self) -> list[str]:
        endpoints = []
        with open('Config/Static/all_endpoints.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                endpoints.append(row[0])
            # Set Versions
            for endpoint in endpoints:
                self.versions_screen[endpoint] = 0
        return endpoints

    def initialize_frame(self) -> None:
        self.root.title("API-Parser")
        self.root.geometry('600x725')

        self.credential_frame.pack(fill="x", pady=(10, 0), padx=10)
        self.endpoint_frame.pack(fill="x", pady=(20, 0), padx=10)
        self.versions_frame.pack(fill="x", pady=(20, 0), padx=10)
        self.database_export.pack(fill="x", pady=(20, 0), padx=10)
        self.run_frame.pack(fill="x", pady=(20, 0), padx=10)

        input_section_label = Label(self.credential_frame, text="API-Credentials:", font=("Helvetica", 16))
        input_section_label.grid(row=0, column=0, pady=5)

        # API Credential input:
        username_label = Label(self.credential_frame, text="Username:")
        username_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.username_entry = Entry(self.credential_frame, width=40)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label = Label(self.credential_frame, text="Password:")
        password_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = Entry(self.credential_frame, width=40)  
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        URL_label = Label(self.credential_frame, text="URL:")
        URL_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.URL_entry = Entry(self.credential_frame, width=40)
        self.URL_entry.grid(row=3, column=1, padx=5, pady=5)

        # Endpoint selection
        endpoint_label = Label(self.endpoint_frame, text="Endpoints:", font=("Helvetica", 16))
        endpoint_label.grid(row=0, column=0, sticky='w', pady=5)

        endpoint_selection_frame = Frame(self.endpoint_frame)
        endpoint_selection_frame.grid(row=1, column=0, sticky='w')

        self.endpoint_selection = Listbox(endpoint_selection_frame, selectmode=MULTIPLE, height=15, width=92)  
        self.endpoint_selection.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(endpoint_selection_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.endpoint_selection.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.endpoint_selection.yview)

        for item in self.get_endpoints():
            self.endpoint_selection.insert(END, f"{item:^40}")

        version_entry_button = Button(self.versions_frame, text="SET VERSIONS", width=40, command=self.set_versions_screen)
        version_entry_button.grid(row=1, column=0, pady=5, padx=135)

        # Database Export options
        export_label = Label(self.database_export, text="Database Export Options:", font=("Helvetica", 16))
        export_label.grid(row=0, column=0, sticky='w', pady=5)

        self.SQLite_option = Checkbutton(self.database_export, text="SQLite database output", variable=self.SQLite_Option_BOOL)
        self.SQLite_option.grid(row=1, column=0, sticky='w', pady=5)

        self.POSTGRES_option = Checkbutton(self.database_export, text="Postgres database creation", variable=self.POSTGRES_option_BOOL)
        self.POSTGRES_option.grid(row=2, column=0, sticky='w', pady=5)

        # Run button
        run_button = Button(self.run_frame, text="Fetch Data", width=40, command=self.fetch_data)
        run_button.grid(row=0, column=0, pady=10, padx=135)