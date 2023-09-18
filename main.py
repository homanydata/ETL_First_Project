from bot import HabitsBot
from generate_sample_data import generate_record
import threading
import schedule
import time
from lookups import Enums

# is this a test or no?
is_test = input('is this a test? ') == '1'

if is_test:
    # reduce migration interval to speed up test
    Enums.change_interval(0.5)
    # this is placed before the bot creation so that the bot can uses the needed interval

# Create and run the bot
bot = HabitsBot(is_test=is_test)

if is_test:
    # schedule generating sample records
    schedule.every(0.1).minutes.do(job_func=bot.generate_record)

# Define a function for the scheduling thread
def scheduling_thread():
    while True:
        schedule.run_pending()
        # sleep is used to avoid continous non-stop running to reduce consumption
        time.sleep(3)

# Create and start the scheduling thread
scheduler_thread = threading.Thread(target=scheduling_thread)
scheduler_thread.daemon = not is_test  # Set as a daemon thread to exit when the main thread exits
scheduler_thread.start()

bot.run()
