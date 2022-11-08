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

    def sort(self):
        print('Name of the columns:')
        self.print_columns()

        columns = []
        while True:
            column = input('Input the name of columns to sort by or press "q" to quit and continue: ')

            if column == 'q':
                break

            if column not in self.data.columns:
                print('Unknown column, try again')
                continue

            if column in columns:
                print('Already selected that column, try again')
                continue

            columns.append(column)

        while True:
            asc = input('Order ascending? y/n\n')

            if asc in ['y','n']:
                break
                
            print('Unknown choice, try again')

        self.sort_data(columns, asc == 'y')
        self.save()

        print('Sorted data has been saved to current file.')


    def sort_data(self, columns, asc:bool = True):
        self.data.sort_values(columns, axis=0, ascending=asc,inplace=True,na_position='first')

    def save(self):
        self.data.to_csv(self.path)

    def start(self):
        while True:
            action = input('Press "s" for sorting or "q" to quit:\n')
            if action not in ['s', 'q']:
                print('Unknown action, try again.')
                continue

            if action == 'q':
                break

            self.sort()

        

file_name = 'dataset.csv'
data_sorter = DataSorter(file_name)
data_sorter.start()

    