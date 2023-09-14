CREATE TABLE IF NOT EXISTS warehouse.dim_category (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS warehouse.dim_habits (
    habit_id SERIAL PRIMARY KEY,
    habit_name TEXT UNIQUE,
    category_id INT REFERENCES warehouse.dim_category
);
CREATE TABLE IF NOT EXISTS warehouse.dim_users (
    user_id NUMERIC PRIMARY KEY,
    chat_id NUMERIC,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_premium BOOLEAN,
    language_code TEXT
);