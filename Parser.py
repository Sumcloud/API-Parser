from Logger import Logger
from Configuration import Configuration
from VersionManagement import VersionManagement as vm
import pandas as pd
import sys

class Parser:
    
    def __init__(self, logger: Logger, config: Configuration) -> None:
        self.logger = logger
        self.config = config

    def add_versioning(self, data: pd.DataFrame, endpoint: str, deleted: bool) -> pd.DataFrame:
        highest_version = vm.get_version(endpoint, deleted)
        data["version"] = range(highest_version+1, highest_version + len(data)+1, 1)
        vm.update_version(endpoint, int(data['version'].max()), deleted)
        return data
    
    def remove_duplicates(self, data: pd.DataFrame, endpoint: str) -> pd.DataFrame:
        """ 
            Function flow:
                1. Loads data and filters based on the filters on the configured filter
                2. Returns filtered values

                Also, if no PK is configured there is no filtering required!
        """
        if self.config.Filters[endpoint]['pk_1'] == '':
            return data # if no work remove the func call
        elif self.config.Filters[endpoint]['pk_2'] != '':
            data = data.sort_values(by=[self.config.Filters[endpoint]['pk_1'],self.config.Filters[endpoint]['pk_2'],'version'],ascending=[False,False,True])
            data = data.drop_duplicates(keep='last', subset=[self.config.Filters[endpoint]['pk_1'],self.config.Filters[endpoint]['pk_2']])
        else:
            data = data.sort_values(by=[self.config.Filters[endpoint]['pk_1'],'version'],ascending=[False,True])
            data = data.drop_duplicates(keep='last', subset=[self.config.Filters[endpoint]['pk_1']])
        return self.remove_delimter_plain_text(data)
    
    def remove_delimter_plain_text(self, data: pd.DataFrame) -> pd.DataFrame:
        for column in data:
            if data[column].dtype == 'object':  
                data[column] = data[column].astype(str)  
                data[column] = data[column].str.replace('|', '',regex=False)
        return data
