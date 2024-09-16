from datetime import datetime

class Logger:

    def __init__(self) -> None:
        self.logfile = 'Logs/Log.txt'
        
    def log_error(self, message: str) -> None:
        with open(file="Log.txt", mode='a') as log:
            log.write('\n' + message)

    def log_request(self, status: int, endpoint: str, versionnumber: int, deleted: str) -> None:
        with open(file="Log.txt", mode='a') as log:
            error_message = f"\nRequest at: {datetime.now()} \t\t {endpoint} \t\t Version number: {versionnumber} \t\t  Deleted: {deleted} \t\t Status: {status} \t\t "
            match status:
                case 200:
                    error_message += "Server Ok"
                case 401:
                    error_message += "Unauthorized access!"
                case 404:
                    error_message += "URL not found!"
                case 500:
                    error_message += "Internal server error!"
                case _:
                    error_message += "An unspecified error has occurred!"
            log.write(error_message)