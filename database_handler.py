import psycopg2
from lookups import Enums

def create_connection():
    database_connection = psycopg2.connect(
            dbname=Enums.DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
    return database_connection

def execute_query(connection, query)
    try:
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            cursor.commit()
        return True
    except:
        return False

def get_query_results(connection, query)
    with self.conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results


# to be fixed and put in suitable place:
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

def insert(self, table, columns, values):
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    with self.conn.cursor() as cursor:
        cursor.execute(query, values)
    self.conn.commit()

def addUser(self, chatID):
    self.insert('users', ['chat_id'], [chatID])

def addHabit(self, row):
    self.insert('habits', ['habit_name'], [row])

def insertrecord(self, row):
    self.insert('records', ['habit_id', 'user_id', 'duration', 'record_date'], row)

def addRecord(self, habit_name, duration, date, chat_id):
    habit_id = self.getHabitID(habit_name)
    user_id = self.getUserID(chat_id)
    # if not habit_id: return 'habit'
    # if not user_id: return 'user'
    self.insertrecord([habit_id, user_id, duration, date])

def get_habits(self, chatID):
    query = "SELECT DISTINCT habit_name"
    with self.conn.cursor() as cursor:
        cursor.execute(query, (chatID,))
        result = cursor.fetchone()
        return result[0]


def __del__(self):
    self.conn.close()

def execute_query(query, database)