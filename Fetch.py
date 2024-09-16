from Logger import Logger
from Configuration import Configuration
from VersionManagement import VersionManagement
import requests
import pandas as pd

class Fetch:

    def __init__(self, logger: Logger, config: Configuration ) -> None:
        self.logger = logger
        self.config = config

    def fetch(self, endpoint: str, deleted: str) -> pd.DataFrame:
        """
            Sends requests to the API recursively until the version number pool is exhausted. 
                Scenario's:
                * If the API request presents no new data the Dataframe will be left empty.
                * If there is no version number present in the API endpoint, only one requests will be sent as there is no way to get a higher version.
                * If there are new versions, the API will be called recursively until the version number pool is exhausted, the data obtained from various calls will be returned in a 
                  combined dataframe.

            This works with both getting the intial data and regular operations where we only want to get the new data.
        """
        data: pd.DataFrame = pd.DataFrame()
        previous_version : int = 999999999999999


        def send_request(endpoint: str, version: int) -> None:
            nonlocal previous_version
            nonlocal data
            nonlocal  deleted

            response = requests.post(
                url = self.config.URL + endpoint,
                auth = (self.config.Username, self.config.Password),
                json = {"Version" : version, "Deleted" : deleted},
                headers = {'Content-Type' : 'application/json'}
            )


            if response.status_code != 200:
                return
            
            self.logger.log_request(response.status_code, endpoint  = endpoint, versionnumber = version, deleted = deleted)

            response_data = response.json()
            json_list_name = next(iter(response_data))

            # If there is no new data based on the version number obtained previously
            if len(response_data[json_list_name]) == 0:
                return
            elif api_filter['has_version'] == 0:
                data = pd.DataFrame(response_data[json_list_name])
                return
            else:
                temp_data: pd.DataFrame = pd.DataFrame(response_data[json_list_name])
                version: int = int(temp_data['version'].max())

                # Some API endpoints have faulty versions, this was a fix returns the API response data
                if version == 0 or previous_version_number == version:
                    data = pd.concat([data,temp_data])
                    return
                else:
                    previous_version_number = version
                    data = pd.concat([data, temp_data])
                    send_request(endpoint, version)

        try:
            api_filter = self.config.Filters[endpoint]
        except KeyError:
            Logger.log_error(f'Parser: endpoint - {endpoint} not in filter file (Endpoints.csv), please configure a filter for: {endpoint}')

        is_deleted: bool = False

        if deleted == 'true':
            is_deleted = True

        send_request(endpoint,VersionManagement.get_version(endpoint=endpoint, deleted=is_deleted))

        if data.empty == False and api_filter['has_version'] == 1:
            VersionManagement.update_version(endpoint, int(data['version'].max()), deleted=is_deleted)

        return data