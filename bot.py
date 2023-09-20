from lookups import Messages, Enums, Markups
import telebot
from telebot import types
from database_handler import create_connection, refresh_connection, get_distinct_categories, get_distinct_habits, get_habit_category, add_stg_record, add_new_category
import schedule
from migration import start_migration
from generate_sample_data import generate_record
from pandas_handler import get_user_interval_summary, get_plot_image

class HabitsBot:
    def __init__(self, is_test):
        self.bot = telebot.TeleBot(Enums.TOKEN)
        self.db_session = create_connection()
        self.temp_habit = None
        self.temp_variable_type = None
        self.temp_variable = None
        self.test_instance = is_test
        self.perform_migration()
        schedule.every(Enums.Migration_Interval).minutes.do(self.perform_migration)

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, Messages.Start)
        
        @self.bot.message_handler(commands=['day', 'week', 'month', 'year'])
        def send_corresponding_summary(message):
            this_month_text_summary = get_user_interval_summary(db_session=self.db_session, user_id=message.from_user.id, interval=message.text[1:])
            self.bot.send_message(chat_id=message.chat.id, text=this_month_text_summary)
        
        @self.bot.message_handler(commands=['summarize'])
        def ask_variable_type(message):
            markup = Markups.Variable_Type_Markup()
            self.bot.send_message(chat_id=message.chat.id, text=Messages.choose_variable_type, reply_markup=markup)
            self.temp_variable_type = True
        def ask_variable(variable_type, chat_id):
            # choose corresponding list
            if 'habit' in variable_type:
                variable_list = get_distinct_habits(db_session=self.db_session)
            else:
                variable_list = get_distinct_categories(db_session=self.db_session)
            # get markup
            markup = Markups.Variable_Markup(variables_list=variable_list)
            # send message with markup
            self.temp_variable_type = variable_type
            self.bot.send_message(chat_id=chat_id, text=Messages.choose_variable, reply_markup=markup)
        def get_summary(variable, variable_type, message:telebot.types.Message):
            self.temp_variable = None
            self.temp_variable_type = None
            image = get_plot_image(db_session=self.db_session, user_id=message.chat.id, variable=variable, variable_type=variable_type)
            if image:
                self.bot.send_photo(chat_id=message.chat.id, photo=image)
        
        @self.bot.message_handler(commands=['list'])
        def send_list(message):
            habits_list = get_distinct_habits(db_session=self.db_session, chat_id=message.chat.id)
            self.bot.send_message(chat_id=message.chat.id, text=habits_list)

        @self.bot.message_handler(commands=['record'])
        def ask_habit_name(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_habit)
            self.bot.register_next_step_handler(message=message, callback=self.recieve_habit_name_ask_category)
        
        @self.bot.message_handler(commands=['new_category'])
        def ask_category(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.new_category)
            self.bot.register_next_step_handler(message=message, callback=self.add_category)
        
        @self.bot.callback_query_handler(func= lambda call:True)
        def change_call_to_answer(call:telebot.types.CallbackQuery):
            if self.temp_habit:
                category = call.data.lower()
                if category==Messages.Alread_answered_keyboard:
                    return
                habit_name = self.temp_habit
                self.temp_habit = None
                self.recieve_category_ask_duration(message=call.message, habit_is_old=True, habit_name=habit_name, category_name=category)
            elif self.temp_variable_type==True:
                variable_type = call.data
                self.temp_variable_type = variable_type
                self.temp_variable = True
                ask_variable(variable_type=variable_type, chat_id=call.message.chat.id)
            elif self.temp_variable==True:
                variable = call.data
                get_summary(message=call.message, variable=variable, variable_type=self.temp_variable_type)
    
    def recieve_habit_name_ask_category(self, message):
        habit_name = message.text.lower()
        categories = get_distinct_categories(db_session=self.db_session)
        habits_list = get_distinct_habits(db_session=self.db_session)
        habit_is_old = habit_name in habits_list

        if habit_is_old:
            category_name = get_habit_category(db_session=self.db_session, habit_name=habit_name)
            self.recieve_category_ask_duration(message=message, habit_name=habit_name, category_name=category_name, habit_is_old=True)
        elif categories:
            markup = Markups.Categories_Markup(categories=categories)
            self.bot.send_message(chat_id=message.chat.id, text=Messages.choose_category, reply_markup=markup)
            self.temp_habit = habit_name
        else:
            self.bot.send_message(chat_id=message.chat.id, text=Messages.No_Categories)

    def recieve_category_ask_duration(self, message, habit_name, category_name:str, habit_is_old=False):
        if habit_is_old:
            # markup = Markups.already_answered_markup(category_name=category_name)
            # self.bot.edit_message_reply_markup(message_id=message.id, chat_id=message.chat.id, reply_markup=markup)
            self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_duration)
            self.bot.register_next_step_handler(message, self.record_time, habit_name=habit_name, category_name=category_name)
        else:
            self.bot.register_next_step_handler(message=message, callback=self.recieve_category_ask_duration, habit_name=habit_name, categories=category_name)
            return
    
    def record_time(self, message:types.Message, habit_name, category_name):
        duration = int(message.text)
        user = message.from_user
        date = message.date
        
        new_data = [habit_name, category_name, user.id, duration, message.chat.id, user.username, user.first_name, user.last_name, user.is_premium, user.language_code, date]
        print(add_stg_record(db_session=self.db_session, new_data=new_data))
        self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_done)
    
    def add_category(self, message):
        add_new_category(db_session=self.db_session, category_name=message.text.lower())
        self.bot.send_message(chat_id=message.chat.id, text=Messages.Category_Added)

    def refresh_bot_db_connection(self):
        self.db_session = refresh_connection(db_session=self.db_session)

    def perform_migration(self):
        start_migration(db_session=self.db_session, new_data=[], is_test=self.test_instance)
        self.refresh_bot_db_connection()
    
    def generate_record(self):
        generate_record(db_session=self.db_session)

    def run(self):
        try:
            self.bot.polling()
        except Exception as e:
            print(e)
