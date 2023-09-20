import pandas as pd
from lookups import Directories
import threading
import os

def df_to_excel(result_as_df:pd.DataFrame):
    try:
        new_excel_file_directory = Directories.new_excel_file_directory()
        result_as_df.to_excel(new_excel_file_directory, index=True, engine='xlsxwriter')
        timer = threading.Timer(10, lambda: remove_excel_file(new_excel_file_directory))
        timer.start()
        return new_excel_file_directory
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def remove_excel_file(file_directory:str):
    # check if the file exists
    if os.path.exists(file_directory):
        # check if the file is excel file
        if file_directory.endswith(('.xlsx', '.xls')):
            os.remove(file_directory)
            print(f"Excel file '{file_directory}' has been deleted.")
        else:
            print(f"'{file_directory}' is not an Excel file and won't be deleted.")
    else:
        print(f"'{file_directory}' does not exist.")