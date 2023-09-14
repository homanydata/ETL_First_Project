import psycopg2
from lookups import Enums, Errors
import pandas as pd

# create connection to database
def create_connection():
    database_connection = psycopg2.connect(
        database=Enums.DATABASE,
        user=Enums.USER,
        password=Enums.PASSWORD,
        host=Enums.HOST,
        port=Enums.PORT
        )
    print('connection succeded')
    return database_connection

# Closing / Disposing the db_session connection
def close_connection(db_session):
    db_session.close()

# Closing & Opening Connection to db_session refresh
def refresh_connection(db_session):
    db_session.close()
    db_session = create_connection()
    return db_session

# Execute SQL function and return result without committing
def return_query(db_session, query, values=None):
    # get cursor from connection
    try:
        cursor = db_session.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        db_session.commit()
    except Exception as e:
        return str(e)
    results = cursor.fetchall()
    return results

# GET QUERY AS DF
def return_query_as_df(db_session, query, values=None):
    if values:
        query_df = pd.read_sql_query(sql=query, con=db_session, params=values)
    else:
        query_df = pd.read_sql_query(sql=query, con=db_session)
    return query_df

# Executes & Commits Any Query
def execute_query(db_session,query,values=None):
    return_code = Errors.No_Error
    try:
        cursor = db_session.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        db_session.commit()
    except Exception as e:
        return_code = str(e)
    finally:
        return return_code

def insert(db_session, table, columns, new_data:list):
    placeholders = ', '.join(['%s'] * len(new_data))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    values = tuple([tuple([data]) for data in new_data])
    return execute_query(db_session=db_session, query=query, values=values)

def add_new_category(db_session, category_name):
    insert(db_session=db_session, table='warehouse.dim_category', columns=['category_name'], new_data=[category_name])

def add_stg_record(db_session, new_data):
    return insert(db_session=db_session, table='warehouse.stg_records', columns=['habit_name', 'category_name', 'user_id', 'duration', 'chat_id', 'username', 'first_name', 'last_name', 'is_premium', 'language_code', 'record_date_unix'], new_data=new_data)

def get_distinct_habits(db_session):
    query = "SELECT DISTINCT habit_name FROM warehouse.dim_habits"
    result = return_query(db_session=db_session, query=query)
    habit_names = [row[0] for row in result]
    return habit_names

def get_distinct_categories(db_session):
    query = "SELECT DISTINCT category_name FROM warehouse.dim_category"
    result = return_query(db_session=db_session, query=query)
    categories_names = [row[0] for row in result]
    return categories_names

def get_habit_category(db_session, habit_name):
    query = "SELECT dim_category.category_name FROM warehouse.dim_habits INNER JOIN warehouse.dim_category ON dim_category.category_id = dim_habits.category_id WHERE dim_habits.habit_name = %s"
    values = tuple([habit_name])
    return return_query(db_session=db_session, query=query, values=values)[0][0]



# to be revised and seen if needed:
def getUserID(self, chatID):
    query = "SELECT user_id FROM users WHERE chat_id = %s"
    with self.conn.cursor() as cursor:
        cursor.execute(query, (str(chatID),))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            self.addUser(chatID)
            return self.getUserID(chatID)
