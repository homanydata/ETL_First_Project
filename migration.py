import os
from database_handler import execute_query
from lookups import Errors

def get_sorted_sql_files():
    folder = './sql_commands'
    files = os.listdir(folder)
    sorted_files = sorted(files, key=lambda file_name: int(file_name.split('_')[0][1:]))
    return sorted_files

def start_migration(db_session, new_data, is_test):
    sorted_sql_files = get_sorted_sql_files()
    version = 0
    print('Migration Process Started...')
    
    for file_name in sorted_sql_files:
        with open(f"./sql_commands/{file_name}","r") as sql_file:
            sql_command = sql_file.read()
            
            # if this is a testing, avoid not-test queries
            if is_test and "NOT FOR TEST" in sql_command: continue
            if not is_test and "ONLY FOR TEST" in sql_command: continue

            if "VALUES" in sql_command:
                if new_data:
                    result = execute_query(db_session=db_session, query=sql_command, values=new_data)
                    print(f'version {version}:{result}')
            else:
                result = execute_query(db_session=db_session, query=sql_command)
                print(f'version {version}:{result}')
                if result != Errors.No_Error:
                    return False
        version += 1
    return True
