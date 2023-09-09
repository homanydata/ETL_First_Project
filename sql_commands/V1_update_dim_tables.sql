-- V1: Insert New Habit Names into dim_habits
INSERT INTO dim_habits (habit_name)
SELECT
    DISTINCT habit_name
FROM staging_records
WHERE habit_name NOT IN (SELECT habit_name FROM dim_habits);

-- V1: Insert New User Attributes into dim_users
INSERT INTO dim_users (user_id, chat_id, username, first_name, last_name, is_premium, language_code)
SELECT DISTINCT
    user_id,
    chat_id,
    username,
    first_name,
    last_name,
    is_premium,
    language_code
FROM staging_records
WHERE user_id NOT IN (SELECT user_id FROM dim_users);