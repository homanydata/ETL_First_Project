from lookups import Messages, Enums
import telebot
from telebot import types
from database_handler import get_distinct_habits, get_distinct_categories, create_connection, refresh_connection, add_stg_record, add_new_category
import schedule
from migration import start_migration

class HabitsBot:
    def __init__(self):
        self.bot = telebot.TeleBot(Enums.TOKEN)
        self.db_session = create_connection()
        schedule.every(Enums.Migration_Interval).do(self.perform_migration)

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, Messages.START)
        
        # # i dont think this is necessary
        # @self.bot.message_handler(commands=['list'])
        # def send_list(message):
        #     habits_list = get_distinct_habits(db_session=self.db_session, chat_id=message.chat.id)
        #     self.bot.send_message(chat_id=message.chat.id, text=habits_list)

        @self.bot.message_handler(commands=['record'])
        def record_habit_name(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_habit)
            self.bot.register_next_step_handler(message=message, callback=self.record_category)
        
        @self.bot.message_handler(commands=['add_category'])
        def ask_category(self, message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.new_category)
            self.bot.register_next_step_handler(message=message, callback=self.add_category)
    
    
    def record_category(self, message):
        habit_name = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
        for category_name in get_distinct_categories(db_session=self.db_session, chat_id=message.chat.id):
            markup.add(category_name)
        self.bot.send_message(chat_id=message.chat.id, text=Messages.choose_category, reply_markup=markup)
        self.bot.register_next_step_handler(message=message, callback=self.record_duration, habit_name=habit_name)

    def record_duration(self, message, habit_name):
        category_name = message.text
        user_chat_id = message.chat.id

        self.bot.send_message(user_chat_id, Messages.Record_duration)
        self.bot.register_next_step_handler(message, self.record_time, habit_name=habit_name, category_name=category_name)

    def record_time(self, message, habit_name, category_name):
        duration = int(message.text)
        user_chat_id = message.chat.id
        date = message.date

        new_data = [habit_name, category_name, user_chat_id, date, duration]
        add_stg_record(new_data)
        self.bot.send_message(user_chat_id, Messages.Record_done)
    
    def add_category(self, message):
        add_new_category(db_session=self.db_session, category_name=message.text)

    def refresh_connection(self):
        self.db_session = refresh_connection(db_session=self.db_session)

    def perform_migration(self):
        start_migration(db_session=self.db_session, new_data=[])
        self.refresh_connection()
    
    def run(self):
        self.bot.polling()
