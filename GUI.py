from tkinter import *
from tkinter import ttk
import csv

class GUI:

    def __init__(self, configuration, logger, fetcher, parser, writer) -> None:
        self.logger = logger
        self.fetcher = fetcher
        self.parser = parser
        self.writer = writer
        self.configuration = configuration
        self.versions_screen : list[tuple] = []

        self.root = Tk()
        
        # Define frames
        self.credential_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.endpoint_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.versions_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.database_export = Frame(self.root, highlightbackground="black", highlightthickness=1)
        self.run_frame = Frame(self.root, highlightbackground="black", highlightthickness=1)

        # Define input fields (credentials, endpoints, checkbox)

        # TODO !
        self.username_entry : Entry
        self.password_entry : Entry
        self.URL_entry : Entry
        self.endpoint_selection : Listbox
        self.SQLite_option : Checkbutton
        self.POSTGRES_option: Checkbutton

        self.initialize_frame()
        self.root.resizable(False, False)
        self.root.iconbitmap("Config/Static/app.ico")
        self.root.mainloop()

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
        endpoints = self.get_endpoints()

        # Dictionary to store version entries
        version_entries = {}

        # Label and Entry for each endpoint and version
        for i, endpoint in enumerate(endpoints):
            endpoint_label = Label(inner_frame, text=endpoint)
            endpoint_label.pack(anchor='w', padx=10, pady=5)

            # Create an entry box for each version, with default value 0
            version_entry = Entry(inner_frame, width=10)
            version_entry.insert(0, "0")  # Default version number is 0
            version_entry.pack(anchor='w', padx=10, pady=5)
            
            # Store the entry widget in a dictionary with the endpoint as the key
            version_entries[endpoint] = version_entry

        # Update the scroll region to accommodate all widgets
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Button to confirm changes and return the values
        def save_versions():
            # Extract the version numbers from the entries
            self.versions_screen = [(endpoint, version_entry.get()) for endpoint, version_entry in version_entries.items()]
            version_window.destroy()

        # Save button
        save_button = Button(version_window, text="Save Versions", command=save_versions)
        save_button.pack(pady=10)

        version_window.mainloop()

    def fetch_data(self):
        username : str = self.username_entry.get()
        password : str = self.password_entry.get()
        URL : str = self.URL_entry.get()

        selected_endpoints = [self.endpoint_selection.get(i) for i in self.endpoint_selection.curselection()]
        sqlite_export = self.SQLite_option.get() == 1
        postgres_export = self.POSTGRES_option.cget() == 1

        print(selected_endpoints)


        # TODO make the entry fields object based , actual data getting needs to be refactored from headless function

    def get_endpoints(self) -> list[str]:
        endpoints = []
        with open('Config/Static/all_endpoints.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # Skip header
            for row in csv_reader:
                endpoints.append(row[0])
            # Set Versions
            for endpoint in endpoints:
                self.versions_screen.append((endpoint, 0))
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
        self.username_entry = Entry(self.credential_frame, width=40)  # Wider Entry
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label = Label(self.credential_frame, text="Password:")
        password_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = Entry(self.credential_frame, width=40, show="*")  # Wider Entry
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        URL_label = Label(self.credential_frame, text="URL:")
        URL_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.URL_entry = Entry(self.credential_frame, width=40)  # Wider Entry
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

        # Version entry button (wider)
        version_entry_button = Button(self.versions_frame, text="SET VERSIONS", width=40, command=self.set_versions_screen)
        version_entry_button.grid(row=1, column=0, pady=5, padx=135)

        # Database Export options
        export_label = Label(self.database_export, text="Database Export Options:", font=("Helvetica", 16))
        export_label.grid(row=0, column=0, sticky='w', pady=5)

        self.SQLite_option = Checkbutton(self.database_export, text="SQLite database output")
        self.SQLite_option.grid(row=1, column=0, sticky='w', pady=5)

        self.POSTGRES_option = Checkbutton(self.database_export, text="Postgres database creation")
        self.POSTGRES_option.grid(row=2, column=0, sticky='w', pady=5)

        # Run button (wider)
        run_button = Button(self.run_frame, text="Fetch Data", width=40, command=self.fetch_data())
        run_button.grid(row=0, column=0, pady=10, padx=135)
