-- Insert New Habits into dim_habits
INSERT INTO dim_habits (habit_name)
SELECT DISTINCT
    stg_records.habit_name,
    dim_category.category_id
FROM stg_records
LEFT JOIN habit_name
    ON stg_records.habit_name = dim_habits.habit_name
INNER JOIN dim_category
    ON dim_category.category_name = stg_records.category_name;
WHERE dim_habits.habit_id IS NULL

-- Insert New Users Attributes into dim_users
INSERT INTO warehouse.dim_users (user_id, chat_id, username, first_name, last_name, is_premium, language_code)
SELECT DISTINCT
    user_id,
    chat_id,
    username,
    first_name,
    last_name,
    is_premium,
    language_code
FROM stg_records
WHERE user_id NOT IN (SELECT user_id FROM warehouse.dim_users);