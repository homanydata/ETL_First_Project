from lookups import Messages, Enums, Markups
import telebot
from telebot import types
from database_handler import *
import schedule
from migration import start_migration

class HabitsBot:
    def __init__(self):
        self.bot = telebot.TeleBot(Enums.TOKEN)
        self.db_session = create_connection()
        self.temp_habit = None
        self.perform_migration()
        schedule.every(Enums.Migration_Interval).minutes.do(self.perform_migration)

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, Messages.Start)
        
        # i dont think this is necessary
        @self.bot.message_handler(commands=['list'])
        def send_list(message):
            habits_list = get_distinct_habits(db_session=self.db_session, chat_id=message.chat.id)
            self.bot.send_message(chat_id=message.chat.id, text=habits_list)

        @self.bot.message_handler(commands=['record'])
        def ask_habit_name(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_habit)
            self.bot.register_next_step_handler(message=message, callback=self.recieve_habit_name_ask_category)
        
        @self.bot.message_handler(commands=['add_category'])
        def ask_category(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.new_category)
            self.bot.register_next_step_handler(message=message, callback=self.add_category)
        
        @self.bot.callback_query_handler(func= lambda call:True)
        def change_call_to_answer(call):
            if not self.temp_habit: return

            category = call.data.lower()
            if category==Messages.Alread_answered_keyboard:
                return
            habit_name = self.temp_habit
            self.temp_habit = None
            self.recieve_category_ask_duration(message=call.message, habit_is_old=True, habit_name=habit_name, category_name=category)

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

    def refresh_connection(self):
        self.db_session = refresh_connection(db_session=self.db_session)

    def perform_migration(self):
        start_migration(db_session=self.db_session, new_data=[])
        self.refresh_connection()
    
    def run(self):
        self.bot.polling()
