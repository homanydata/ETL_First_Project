from bot import HabitsBot
import threading
import schedule
import time

# Define a function for the scheduling thread
def scheduling_thread():
    while True:
        schedule.run_pending()
        time.sleep(5)

# Create and start the scheduling thread
scheduler_thread = threading.Thread(target=scheduling_thread)
scheduler_thread.daemon = True  # Set as a daemon thread to exit when the main thread exits
scheduler_thread.start()

# Create and run the bot
bot = HabitsBot()
bot.run()
