from lookups import Messages
import telebot
import datetime

class HabitsBot:
    def __init__(self, bot_token, db_instance):
        self.bot = telebot.TeleBot(bot_token)
        self.db = db_instance

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, Messages.START)
        
        @self.bot.message_handler(commands=['list'])
        def send_list(message):
            habits_list = self.db.get_habits()
            self.bot.send_message(message.chat.id, habits_list)

        @self.bot.message_handler(commands=['record'])
        def record_habit_name(message):
            self.bot.send_message(message.chat.id, Messages.Record_habit)
            self.bot.register_next_step_handler(message, self.record_duration)

    def record_duration(self, message):
        habit_name = message.text
        user_chat_id = message.chat.id

        self.bot.send_message(user_chat_id, Messages.Record_duration)
        self.bot.register_next_step_handler(message, self.record_time, habit_name=habit_name)

    def record_time(self, message, habit_name):
        print(message)
        duration = int(message.text)
        user_chat_id = message.chat.id
        date = datetime.datetime.now().date()

        self.db.addRecord(habit_name=habit_name, duration=duration, date=date, chat_id=user_chat_id)

        self.bot.send_message(user_chat_id, Messages.Record_done)

    def run(self):
        self.bot.polling()
