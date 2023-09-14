CREATE TABLE IF NOT EXISTS warehouse.fct_records (
    record_id SERIAL PRIMARY KEY,
    habit_id INT REFERENCES warehouse.dim_habits,
    category_id INT REFERENCES warehouse.dim_category,
    user_id NUMERIC REFERENCES warehouse.dim_users,
    duration NUMERIC,
    record_date TIMESTAMP
)