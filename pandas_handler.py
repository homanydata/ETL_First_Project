import pandas as pd
from database_handler import return_query_as_df, return_query
# from excel_handler import df_to_excel, delete_excel_file
from lookups import Messages
import timer
from plot_creator import create_plot_image

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
    with open('.summaries_sql_commands/all_user_records.sql') as sql_command:
        query = sql_command.read()
        values = tuple([user_id])
        result = return_query_as_df(db_session=db_session, query=query, values=values)
        return result

def get_user_interval_summary(db_session, user_id, interval:str):
    # get needed summary as dataframe
    with open('./summaries_sql_commands/interval_summary.sql') as sql_command:
        query = sql_command.read()
        values = tuple([user_id] + [interval]*4)
        result_df = return_query_as_df(db_session=db_session, query=query, values=values)
    
    # prepare result as text
    intro = Messages.summary(period=interval)
    result_text = intro
    
    for index, row in result_df.iterrows():
        result_text += f"\n- {row['habit_name']}: {row['total_records']} records | {row['total_duration']} mins"
    result_text += f"\nTotal: {result_df['total_duration'].sum()} minutes over {result_df['total_records'].sum()}"
    
    return result_text

def get_plot_image(db_session, user_id, variable:str, variable_type:str):
    if variable == 'all':
        is_bar = True
        with open('./summaries_sql_commands/variable_distribution.sql') as sql_command:
            query=sql_command.read()
            values = tuple([user_id])
    else:
        is_bar = False
        with open('./summaries_sql_commands/variable_time_series.sql') as sql_command:
            query=sql_command.read()
            values = tuple([user_id, variable])
    
    query = query.format(variable_type, variable_type)
    print(query,'\n',values)
    needed_dataframe = return_query_as_df(db_session=db_session, query=query, values=values)
    print(needed_dataframe)
    plot_image = create_plot_image(source=needed_dataframe, is_bar=is_bar, variable_type=variable_type, variable=variable)
    return plot_image
