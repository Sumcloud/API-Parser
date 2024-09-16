from Logger  import Logger
from Configuration import Configuration
from Fetch import Fetch
from Parser import Parser
from Writer import Writer
from tkinter import *
from tkinter import ttk

class GUI: 

    def __init__(self, logger: Logger, fetcher: Fetch, parser: Parser, writer:Writer) -> None:
        self.logger: Logger = logger
        self.fetcher: Fetch = fetcher
        self.parser: Parser = parser
        self.writer: Writer = writer

        self.root: Tk = Tk()
        self.credential_frame = ttk.Frame(self.root, padding=10)
        self.endpoint_frame = ttk.Frame(self.root, padding= 10)
        self.versions_frame = ttk.Frame(self.root, padding=10)
        self.database_export = ttk.Frame(self.root, padding=10)
        self.run_frame = ttk.Frame(self.root, padding=10)
    
        self.initialize_frame()
        self.root.resizable(False, False)
        self.root.iconbitmap("Config/Static/app.ico")
        self.root.mainloop()


    def initialize_frame(self) -> None:
        self.root.title("API-Parser")
        self.root.geometry('450x1000')

        self.credential_frame.pack(fill="x",pady=10)
        self.endpoint_frame.pack(fill="x",pady=10)
        self.versions_frame.pack(fill="x",pady=10)
        self.database_export.pack(fill="x",pady=10)
        self.run_frame.pack(fill="x",pady=10)


        input_section_label : Label = Label(self.credential_frame, text="API-Credentials")
        input_section_label.pack(pady=5)

        # API Credential input :
        username_label : Label = Label(self.credential_frame, text= "Username")
        username_label.pack(pady=5)

        username_entry : Entry = Entry(self.credential_frame)
        username_entry.pack(pady=5)

        password_label : Label = Label(self.credential_frame, text= "Password")
        password_label.pack(pady=5)

        password_entry : Entry = Entry(self.credential_frame)
        password_entry.pack(pady=5)


        URL_label : Label = Label(self.credential_frame, text= "URL")
        URL_label.pack(pady=5)
        
        URL_entry : Entry = Entry(self.credential_frame)
        URL_entry.pack(pady=5)

        # Endpoint selection
        endpoint_label : Label = Label(self.endpoint_frame, text= "Endpoints")
        endpoint_label.pack(pady=5)

        # Select endpoints (using a listbox) I am not sure yet?
        endpoint_selection :Listbox = Listbox(self.endpoint_frame)
        endpoint_selection.pack(pady=5)

        # Version defaulting
        version_default_checkbox :Checkbutton = Checkbutton(self.versions_frame, text="Default version at 0")
        version_default_checkbox.pack(pady=5)

        # Version_entry
        version_entry :Button = Button(self.versions_frame, command=self.set_versions_screen, text="SET VERSIONS")
        version_entry.pack(pady=5)


        # Database Export 
        SQLite_option :Checkbutton = Checkbutton( self.database_export, text= "SQLite database output")
        SQLite_option.pack(pady=5)

        POSTGRES_option :Checkbutton = Checkbutton( self.database_export, text= "Postgres database creation")
        POSTGRES_option.pack(pady=5)

        run_button :Button = Button( self.run_frame, text="Fetch Data")
        run_button.pack(pady=5)

    def load_endpoints(self) -> list[str]:
        pass

    def set_versions_screen(self) -> list[tuple]:
        pass

    def fetch_data():
        # Refactor the Headless run option so that it simply starts a function with the headless parameters, 
        # saves amount of code
        pass
