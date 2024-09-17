from Logger  import Logger
from Configuration import Configuration
from Fetch import Fetch
from Parser import Parser
from Writer import Writer
from GUI import GUI
from DatabaseCreator.SQLITE_Creator import CSVtoSQLite
from DatabaseCreator.POSTGRES_Creator import CSVtoSQL
import argparse

def run_with_guid():
    application: GUI = GUI(config, logger, fetcher, parser, writer)


def run_headless():
    for i in range(length):
        endpoint = config.Endpoints[i]
        print(f"{i + 1}/{length} - {endpoint}")

        data = fetcher.fetch(endpoint, "false")

        # If there is no new data, the iteration is skipped as it requires no further processing.
        if data.empty == True:
            writer.create_empty_file(endpoint, False)
            continue

        if config.Filters[config.Endpoints[i]]['has_version'] == 0 or data['version'].max() == 0:
            data = parser.add_versioning(data, endpoint, False)

        data = parser.remove_duplicates(data, endpoint)
        writer.write_data(data=data, endpoint=endpoint, deleted=False)

    for i in range(length):
        endpoint = config.Endpoints[i]
        print(f"{i + 1}/{length} - {endpoint}")

        data = fetcher.fetch(endpoint, "true")

        # If there is no new data, the iteration is skipped as it requires no further processing.
        if data.empty == True:
            writer.create_empty_file(endpoint, True)
            continue

        if config.Filters[config.Endpoints[i]]['has_version'] == 0 or data['version'].max() == 0:
            data = parser.add_versioning(data, endpoint, True)

        data = parser.remove_duplicates(data, endpoint)
        writer.write_data(data=data, endpoint=endpoint, deleted=True)

        if config.SQLITE == True:
            csv_to_sqlite = CSVtoSQLite()

        if config.POSTGRES == True:
            csv_to_postgres = CSVtoSQL()


if __name__ == '__main__': 
    logger :Logger = Logger()
    config :Configuration = Configuration(logger)
    fetcher :Fetch = Fetch(logger=logger, config=config)
    writer :Writer = Writer(logger=logger, config=config)
    parser :Parser = Parser(logger=logger, config=config)

    length = len(config.Endpoints)
    
    argparser = argparse.ArgumentParser(description="GUI or Headlessmode default is with GUI")
    
    argparser.add_argument('--headless', action='store_true',help="Run the application in headless mode.")
    args = argparser.parse_args()

    if args.headless:
        run_headless
    else:
        run_with_guid()