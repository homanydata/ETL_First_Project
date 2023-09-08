import os
from database_handler import execute_query

def get_sql_commands():
    folder = './sql_commands'
    files = os.listdir(folder)
    return files

def start_migration(database, new_data)
    sql_commands = get_sql_commands()
    
    for command in sql_commands:
        execute_query(command, database)

print()