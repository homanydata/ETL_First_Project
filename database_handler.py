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


# to be revised and used if needed:
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

def insert(db_session, table, columns, values):
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    with db_session.cursor() as cursor:
        cursor.execute(query, values)
    db_session.commit()

def addUser(self, chatID):
    insert('users', ['chat_id'], [chatID])

def addHabit(row):
    insert('habits', ['habit_name'], [row])

def insertrecord(row):
    insert('records', ['habit_id', 'user_id', 'duration', 'record_date'], row)

def addRecord(habit_name, duration, date, chat_id):
    habit_id = getHabitID(habit_name)
    user_id = getUserID(chat_id)
    # if not habit_id: return 'habit'
    # if not user_id: return 'user'
    insertrecord([habit_id, user_id, duration, date])

def get_distinct_habits(db_session, chat_id):
    query = "SELECT DISTINCT habit_name"
    with db_session.cursor() as cursor:
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()
        return result[0]
