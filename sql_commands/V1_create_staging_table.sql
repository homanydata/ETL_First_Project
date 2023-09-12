CREATE TABLE IF NOT EXISTS warehouse.stg_records (
    id SERIAL PRIMARY KEY,
    habit_name TEXT,
    user_id NUMERIC,
    chat_id NUMERIC,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_premium BOOLEAN,
    language_code TEXT,
    duration NUMERIC,
    record_date DATE,
    category_name TEXT
);