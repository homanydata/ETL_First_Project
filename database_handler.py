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
def return_query(db_session, query):
    # get cursor from connection
    cursor = db_session.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# GET QUERY AS DF
def return_query_as_df(db_session, query):
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
    except:
        return_code = Errors.NO_DATA_ERROR
    finally:
        return return_code

def insert(db_session, table, columns, values):
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    execute_query(db_session=db_session, query=query)

def add_new_category(db_session, category_name):
    insert(db_session=db_session, table='warehouse.dim_category', columns=['category_name'], values=[category_name])

def add_stg_record(db_session, new_data):
    insert(db_session=db_session, table='warehouse.stg_records', columns=['habit_name', 'category_name' 'user_id', 'duration', 'record_date'], values=new_data)

def get_distinct_habits(db_session, chat_id):
    query = "SELECT DISTINCT habit_name FROM dim_habit"
    result = return_query(db_session=db_session, query=query)
    habit_names = [row[0] for row in result]
    return habit_names

def get_distinct_categories(db_session):
    query = "SELECT DISTINCT category_name FROM dim_category"
    result = return_query(db_session=db_session, query=query)
    categories_names = [row[0] for row in result]
    return categories_names


# to be revised and seen if needed:
def getHabitID(self, habit_name):
    query = "SELECT habit_id FROM habits WHERE habit_name = %s"
    with self.conn.cursor() as cursor:
        cursor.execute(query, (habit_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            self.addHabit(habit_name)
            return self.getHabitID(habit_name)

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
