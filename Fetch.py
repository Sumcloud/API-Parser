import requests
import pandas as pd
from Logger import Logger
from Configuration import Configuration
from VersionManagement import VersionManagement

class Fetch:

    def __init__(self, logger: Logger, config: Configuration) -> None:
        self.logger = logger
        self.config = config

    def fetch(self, endpoint: str, deleted: str, username: str = None, password: str = None, url: str = None, initial_version: int = None) -> pd.DataFrame:
        """
        Sends requests to the API recursively until the version number pool is exhausted.
        This works with both getting the initial data and regular operations where we only want to get new data.
        """
        data: pd.DataFrame = pd.DataFrame()
        previous_version: int = 999999999999999  # Default to a very large number
        username = username if username else self.config.Username
        password = password if password else self.config.Password
        url = url if url else self.config.URL
        initial_version = initial_version if initial_version is not None else 0

        def send_request(endpoint: str, version: int) -> None:
            nonlocal previous_version
            nonlocal data
            nonlocal deleted

            try:
                response = requests.post(
                    url=url + endpoint,
                    auth=(username, password),
                    json={"Version": version, "Deleted": deleted},
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code != 200:
                    self.logger.log_error(f"Failed request with status code {response.status_code} for {endpoint}")
                    return

                self.logger.log_request(response.status_code, endpoint=endpoint, versionnumber=version, deleted=deleted)

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

                    # Fix faulty versions
                    if version == 0 or previous_version == version:
                        data = pd.concat([data, temp_data])
                        return
                    else:
                        previous_version = version
                        data = pd.concat([data, temp_data])
                        send_request(endpoint, version)

            except requests.RequestException as e:
                self.logger.log_error(f"Request failed for {endpoint} with error: {str(e)}")
                return

        try:
            api_filter = self.config.Filters[endpoint]
        except KeyError:
            self.logger.log_error(f'Parser: endpoint - {endpoint} not in filter file (Endpoints.csv), please configure a filter for: {endpoint}')
            return pd.DataFrame()

        is_deleted: bool = deleted.lower() == 'true'
        initial_version = initial_version if initial_version is not None else VersionManagement.get_version(endpoint=endpoint, deleted=is_deleted)

        send_request(endpoint, initial_version)

        if not data.empty and api_filter['has_version'] == 1:
            VersionManagement.update_version(endpoint, int(data['version'].max()), deleted=is_deleted)

        return data
