import os
from database_handler import execute_query

def get_sorted_sql_files():
    folder = './sql_commands'
    files = os.listdir(folder)
    sorted_files = sorted(files)
    return sorted_files

def start_migration(db_session, new_data):
    sorted_sql_files = get_sorted_sql_files()
    version = 0

    for file_name in sorted_sql_files:
        with open(f"./sql_commands/{file_name}","r") as sql_file:
            sql_command = sql_file.read()
            if version == 0:
                execute_query(db_session=db_session,query=sql_command, values=new_data)
            else:
                execute_query(db_session=db_session,query=sql_command)
        version += 1

    return True
