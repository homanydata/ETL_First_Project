CREATE TABLE IF NOT EXISTS warehouse.fct_records (
    record_id SERIAL PRIMARY KEY,
    habit_id INT REFERENCES warehouse.dim_habits.habit_id,
    category_id INT REFERENCES warehouse.dim_category.category_id,
    user_id INT REFERENCES warehouse.dim_users.user_id,
    duration NUMERIC,
    record_date DATE
)