from database_handler import add_stg_record, get_distinct_habits, get_habit_category, get_distinct_user_ids
import random
import time

def generate_record(db_session):
    habits = get_distinct_habits(db_session=db_session)
    if habits:
        # generate needed values
        habit_name = random.choice(habits)
        category_name = get_habit_category(db_session=db_session, habit_name=habit_name)
        duration = random.randint(1,20)*10
        user_id = random.choice(get_distinct_user_ids(db_session=db_session))
        
        # generate a timestamp within a range of 2 weeks
        now_timestamp = int(time.time())
        seconds_in_1_month = 30*7*24*60*60
        date = now_timestamp + random.randint(-seconds_in_1_month,seconds_in_1_month)

        new_data = [habit_name, category_name, user_id, duration, None, None, None, None, None, None, date]
        print(new_data)
        print(add_stg_record(db_session=db_session, new_data=new_data))
