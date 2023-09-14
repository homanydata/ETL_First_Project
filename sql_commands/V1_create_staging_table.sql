CREATE TABLE IF NOT EXISTS warehouse.stg_records (
    id SERIAL PRIMARY KEY,
    habit_name TEXT,
    category_name TEXT,
    user_id NUMERIC,
    duration NUMERIC,
    chat_id NUMERIC,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_premium BOOLEAN,
    language_code TEXT,
    record_date_unix INT
);