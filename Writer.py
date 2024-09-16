from Configuration import Configuration
from Logger import Logger
import os
import pandas as pd

class Writer:

    def __init__(self, logger: Logger, config: Configuration) -> None:
        self.config: Configuration = config
        self.logger: Logger = logger

    def storage_file_exists(self, endpoint: str) -> bool:
        return os.path.exists(self.config.Path + endpoint.replace('constants/', ''))
    
    def write_data(self, data: pd.DataFrame, endpoint: str, deleted: bool) -> None:

        if deleted == False:
            file_path = self.config.Path + endpoint.replace('constants/', '') + '.csv'
        else:
            file_path = self.config.Deleted + endpoint.replace('constants/', '') + '.csv'
        print(file_path)
        with open(file_path, 'w', newline='', encoding='utf-8', errors='replace') as file:
            result = data.to_csv(sep='|',index=False, lineterminator='')
            file.write(result)

    def create_empty_file(self, endpoint: str, deleted: bool) -> None:
        if deleted == False:
            file_path = self.config.Path + endpoint.replace('constants/', '') + '.csv'
        else:
            file_path = self.config.Deleted + endpoint.replace('constants/', '') + '.csv'
        
        with open(file_path, 'w', newline='', encoding='utf-8', errors='replace') as file:
                pass
