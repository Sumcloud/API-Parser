import csv
import os
import configparser
from Logger import Logger

class Configuration:

    def __init__(self, Logger: Logger) -> None:
        self.URL :str = ""
        self.Username :str = ""
        self.Password :str = ""
        self.Endpoints :list[str] = []
        self.Filters :dict[str, dict[str,str,bool]] = {}
        self.Path :str = ""
        self.Logger = Logger
        self.Deleted :str = ""
        self.SQLITE : bool = False
        self.POSTGRES : bool = False
        self.load_settings()
        self.load_filters()
    
    def load_settings(self) -> None:
        config = configparser.ConfigParser()

        if not os.path.exists('Config.ini'):
            message = f"ConfigurationLoader: {'Config.ini'} does not exist!"
            Logger.log_error(message)
            raise FileNotFoundError(message)
        
        else: 
            config.read('Config.ini')

            self.URL = config["API_INFO"]["URL"]
            self.Username = config["API_INFO"]["Username"]
            self.Password = config["API_INFO"]["Password"]
            self.Path = config["Storage"]["Path"]
            self.Deleted = config["Storage"]["Deleted"]
            self.SQLITE = config["Creat_Test_DB"]["SQLITE"] == "True" or config["Creat_Test_DB"]["SQLITE"] == "true"
            self.SQLITE = config["Creat_Test_DB"]["POSTGRES"] == "True" or config["Creat_Test_DB"]["POSTGRES"] == "true"

    def load_filters(self) -> None:
        if not os.path.exists('Endpoints.csv'):
            message = f"ConfigurationLoader: {'Endpoints.csv'} does not exist!"
            Logger.log_error(message)
            raise FileNotFoundError(message)
        
        with open('Endpoints.csv', mode='r') as csvfile:
            csv_reader = csv.reader(csvfile,delimiter=',')
            csv_reader.__next__()
            for row in csv_reader:
                self.Endpoints.append(row[0])
                self.Filters[row[0]] = {"pk_1" : row[1], "pk_2" : row[2], "has_version" : bool(int(row[3]))}

    def print_config(self) -> None:
        print(f'API Info:\n\tUsername: {self.Username}\n\tPassword: {self.Password}\n\tURL: {self.URL}')

        print(f'\nEndpoints:')
        for endpoint in self.Endpoints:
            print(endpoint)

        for endpoint in self.Filters.keys():
            print(endpoint)
            for filter in self.Filters[endpoint]:
                print(f'\t{filter} : {self.Filters[endpoint][filter]}')

