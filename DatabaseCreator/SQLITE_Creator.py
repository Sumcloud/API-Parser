import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String

class CSVtoSQLite:
    def __init__(self, database_uri='sqlite:///Databases/results.db') -> None:
        self.engine = create_engine(database_uri)
        self.metadata = MetaData()

    def create_table_from_csv(self, file_path):
        table_name = os.path.splitext(os.path.basename(file_path))[0]

        try:
            df = pd.read_csv(file_path, delimiter='|', dtype=str, low_memory=False)
        except pd.errors.EmptyDataError:
            print(f"Warning: '{file_path}' is empty or has no data to parse. Skipping.")
            return

        if df.empty:
            print(f"Warning: '{file_path}' has no rows of data. Skipping.")
            return
        
        columns = [Column(col, String) for col in df.columns]  

        table = Table(table_name, self.metadata, *columns)

        self.metadata.create_all(self.engine)

        df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
        print(f"Table '{table_name}' created successfully from '{file_path}'.")

    def create_tables_from_folder(self, folder_path='../results'):
        full_folder_path = os.path.join(os.path.dirname(__file__), folder_path)
        
        for filename in os.listdir(full_folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(full_folder_path, filename)
                self.create_table_from_csv(file_path)
                print(f"Table : {filename} done!")
        
        print("All tables created successfully.")

# Use code below if data is already present in Results/
#if __name__ == "__main__":
#    csv_to_sql = CSVtoSQL()
#    csv_to_sql.create_tables_from_folder('../results')
