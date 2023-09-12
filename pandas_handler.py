import pandas as pd
from database_handler import return_query_as_df
from excel_handler import df_to_excel, delete_excel_file
import timer

def return_query_as_excel(db_session, query):
    result_as_df = return_query_as_df(db_session=db_session, query=query)
    result_as_excel, file_directory = df_to_excel(result_as_df)
    # set timer to delete file
    timer.set_timer(3, delete_excel_file(file_directory)).start_timer()
    return result_as_excel

def return_query_as_text(db_session, query):
    result_as_df = return_query_as_df(db_session=db_session, query=query)
    result_as_text = result_as_df.to_string()
    return result_as_text

def get_user_records(db_session, user_id):
    with open('.summaries_sql_commands/.all_user_records.sql') as sql_command:
        query = sql_command.read()
        result = return_query_as_df(query=query)
        return result

def get_user_day_summary():
    # fix all queries names
    # fix all queries names
    with open('summaries_sql_commands.sql') as sql_command:
        query = sql_command.read()
        result = return_query_as_df(query=query)
        return result

def get_user_week_summary():
    with open('summaries_sql_commands.sql') as sql_command:
        query = sql_command.read()
        result = return_query_as_df(query=query)
        return result

def get_user_month_summary():
    with open('summaries_sql_commands.sql') as sql_command:
        query = sql_command.read()
        result = return_query_as_df(query=query)
        return result

def get_user_year_summary():
    with open('summaries_sql_commands.sql') as sql_command:
        query = sql_command.read()
        result = return_query_as_df(query=query)
        return result
