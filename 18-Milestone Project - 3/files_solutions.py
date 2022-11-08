"""
Sort Excel/CSV File Utility
Reads a file of records, sorts them, and then writes them back to the file. 
Allow the user to choose various sort style and sorting based on a particular field.
"""
import pandas as pd


class DataSorter:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = pd.read_csv(self.path)
        # remove Unnamed columns
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]

    def print_columns(self):
        for column in self.data.columns:
            print(column)   

    def sort(self, columns, asc:bool = True):
        self.data.sort_values(columns, axis=0, ascending=asc,inplace=True,na_position='first')

    def save(self):
        self.data.to_csv(self.path)
        

# file_name = input('Input path to the csv file:')
file_name = 'dataset.csv'
data_sorter = DataSorter(file_name)
data_sorter.print_columns()
data_sorter.sort(['compound_name', 'species'])
data_sorter.save()

    