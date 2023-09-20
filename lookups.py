import telebot

class Enums:
    TOKEN = '5903757228:AAGxXmVHt0Fk7ADTCa3tYdlpJ1FE6NZkrzk'
    DATABASE = 'HabitsBotDB'
    PORT = 5432
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'AmHpg23aCc'
    Migration_Interval = 10

    def change_interval(n:int):
        Enums.Migration_Interval = n

class Directories:
    EXCEL_FILE_DIRECTORY = './excel'
    CSV_FILE_DIRECTORY = './csv'

class Messages:
    Start = "Hello! I'm your habits recording bot. Use /record to start recording your habits."
    new_category = 'write the new category name:'
    choose_category = "choose habit's category"
    choose_variable_type = 'do you want a summary for habits or categories?'
    choose_variable = 'which do you want to summarize?'
    Category_Added = 'category added successfully'
    Invalid_Category = 'this is invalid category, please next time choose from existing categories, or add this as new category'
    
    Invalid_habit = "Invalid habit. Please choose from the predefined habit list (use /list to see it) or add this as new habit using /add"
    No_Categories = 'Sorry, you need to add a new category first, there is none'
    
    Record_habit = "Please enter the name of the habit:"
    Record_duration = "Great! Now, please enter the duration (in minutes):"
    Record_done = "Record added successfully!"
    
    Alread_answered_keyboard = 'Already Answered'
    summary = lambda period: f"This {period.capitalize()} Summary:\n"

class Errors:
    DATABASE_CONNECTION_ERROR = ""
    NO_DATA_ERROR = "oops something wrong here"
    No_Error = "all good"

class Markups:
    # markup with button for each category_name
    def Categories_Markup(categories):
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            telebot.types.InlineKeyboardButton(category_name, callback_data=category_name) for category_name in categories
        ]
        markup.add(*buttons)
        return markup
    
    def already_answered_markup(category_name:str):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        print(category_name)
        button = telebot.types.InlineKeyboardButton(category_name, callback_data=Messages.Alread_answered_keyboard)
        print(button)
        markup.add(button)
        print(markup)
        return markup
    
    def Variable_Type_Markup():
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            telebot.types.InlineKeyboardButton("Categories", callback_data="category_name"),
            telebot.types.InlineKeyboardButton("Habits", callback_data="habit_name")
        ]
        markup.add(*buttons)
        return markup

    def Variable_Markup(variables_list:list[str]):
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            telebot.types.InlineKeyboardButton(variable_name, callback_data=variable_name) for variable_name in variables_list
        ]
        markup.add(*buttons)
        
        all_button = telebot.types.InlineKeyboardButton(text='All', callback_data="all")
        markup.add(all_button)

        return markup

class Colors:
    All_Colors = [
    'b', 'blue', 'g', 'green', 'r', 'red', 'c', 'cyan',
    'm', 'magenta', 'y', 'yellow', 'k', 'black', 'w', 'white',
    'beige', 'bisque', 'blanchedalmond', 'blueviolet', 'brown', 'chocolate', 'coral', 'darkblue',
    'darkgoldenrod','darkgreen','darkviolet','deepskyblue', 'gold', 'greenyellow', 'lavender', 'lightblue',
    'lightskyblue', 'magenta', 'olive', 'olivedrab', 'orange']