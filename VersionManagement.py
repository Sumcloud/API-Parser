import csv
from Logger import Logger

versions_file = 'Config/Versions.csv'
deleted_versions_file = 'Config/Deleted_Versions.csv'
logger = Logger()

class VersionManagement:

    @staticmethod
    def get_version(endpoint: str, deleted: bool) -> int:

        if deleted:
            vfile = deleted_versions_file
        else:
            vfile = versions_file

        with open(vfile,'r',newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                t_endpoint = row[0]
                version = row[1]
                if endpoint == t_endpoint:
                    return int(version)
            logger.log_error(f"Parser: Error whilst looking for version number for endpoint {endpoint}, does not exist in Versions file! ")

    @staticmethod
    def update_version(endpoint:str ,current_version: int, deleted: bool) -> None:
        data = []
        updated = False

        if deleted:
            vfile = deleted_versions_file
        else:
            vfile = versions_file

        with open(vfile,'r',newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                t_endpoint = row[0]
                if endpoint == t_endpoint:
                    row = [t_endpoint,current_version]
                    updated = True
                data.append(row)

        if not updated:
            logger.log_error(f"Parser: Error while updating version for endpoint {endpoint}, does not exist in Versions file!")
            return

        with open(vfile,'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
