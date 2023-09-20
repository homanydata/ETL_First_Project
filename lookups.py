import telebot
import os

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
    EXCEL_FILE_DIRECTORY = 'C:/Ali/Learning/Data Science/On My Own/11- ETL/ETL_First_Project/temporary_excel_files'

    def new_excel_file_directory():
        files_names = os.listdir(Directories.EXCEL_FILE_DIRECTORY)
        if files_names:
            files_versions = [int(file_name.split('.')[0].split('_')[-1]) for file_name in files_names]
            files_versions.sort()
            return f"{Directories.EXCEL_FILE_DIRECTORY}/temp_user_data_file_{files_versions[-1]+1}.xlsx"
        return "C:/Ali/Learning/Data Science/On My Own/11- ETL/ETL_First_Project/temporary_excel_files/temp_user_data_file_1.xlsx"

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
    Error_Apologize = 'Sorry, an error occured'

    Record_habit = "Please enter the name of the habit:"
    Record_duration = "Great! Now, please enter the duration (in minutes):"
    Record_done = "Record added successfully!"
    
    Alread_answered_keyboard = 'Already Answered'
    summary = lambda period: f"This {period.capitalize()} Summary:/n"

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
