class Enums:
    TOKEN = '5903757228:AAGxXmVHt0Fk7ADTCa3tYdlpJ1FE6NZkrzk'
    DATABASE = 'HabitsBotDB'
    PORT = 5432
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'AmHpg23aCc'

class Messages:
    Start = "Hello! I'm your habits recording bot. Use /record to start recording your habits."
    
    Invalid_habit = "Invalid habit. Please choose from the predefined habit list (use /list to see it) or add this as new habit using /add"
    
    Record_habit = "Please enter the name of the habit:"
    Record_duration = "Great! Now, please enter the duration (in minutes):"
    Record_done = "Record added successfully!"
    
    summary = lambda period: f"This {period} Summary:\n"

class Errors:
    DATABASE_CONNECTION_ERROR = ""
    NO_DATA_ERROR = ""
    No_Error = "all good"
