from lookups import Messages
import telebot
import datetime
from migration import start_migration
from database_handler import get_distinct_habits

class HabitsBot:
    def __init__(self, bot_token, db_session):
        self.bot = telebot.TeleBot(bot_token)
        self.db_session = db_session

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, Messages.START)
        
        # i dont think this is necessary
        @self.bot.message_handler(commands=['list'])
        def send_list(message):
            habits_list = get_distinct_habits(db_session=self.db_session, chat_id=message.chat.id)
            self.bot.send_message(chat_id=message.chat.id, text=habits_list)

        @self.bot.message_handler(commands=['record'])
        def record_habit_name(message):
            self.bot.send_message(chat_id=message.chat.id, text=Messages.Record_habit)
            self.bot.register_next_step_handler(message=message, callback=self.record_duration)

    def record_duration(self, message):
        habit_name = message.text
        user_chat_id = message.chat.id

        self.bot.send_message(user_chat_id, Messages.Record_duration)
        self.bot.register_next_step_handler(message, self.record_time, habit_name=habit_name)

    def record_time(self, message, habit_name):
        duration = int(message.text)
        user_chat_id = message.chat.id
        date = datetime.datetime.now().date()

        new_data = [habit_name, user_chat_id, date, duration]
        
        # addRecord(habit_name=habit_name, duration=duration, date=date, chat_id=user_chat_id)
        self.bot.send_message(user_chat_id, Messages.Record_done)

    def run(self):
        self.bot.polling()
