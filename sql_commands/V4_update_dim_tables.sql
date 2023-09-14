-- Insert New Habits into dim_habits
INSERT INTO warehouse.dim_habits (habit_name, category_id)
SELECT DISTINCT
    stg_records.habit_name,
    dim_category.category_id
FROM warehouse.stg_records
LEFT JOIN warehouse.dim_habits
    ON stg_records.habit_name = dim_habits.habit_name
INNER JOIN warehouse.dim_category
    ON dim_category.category_name = stg_records.category_name
WHERE dim_habits.habit_id IS NULL
;
-- Insert New Users Attributes into dim_users
INSERT INTO warehouse.dim_users (user_id, chat_id, username, first_name, last_name, is_premium, language_code)
SELECT DISTINCT
    warehouse.stg_records.user_id,
    warehouse.stg_records.chat_id,
    COALESCE(warehouse.stg_records.username,'') AS username,
    warehouse.stg_records.first_name,
    COALESCE(warehouse.stg_records.last_name, '') AS last_name,
    COALESCE(warehouse.stg_records.is_premium, FALSE) AS is_premium,
    COALESCE(warehouse.stg_records.language_code, 'None') AS language_code
FROM warehouse.stg_records
LEFT JOIN warehouse.dim_users
	ON dim_users.user_id = stg_records.user_id
WHERE dim_users.user_id IS NULL
;