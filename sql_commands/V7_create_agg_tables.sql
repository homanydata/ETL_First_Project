CREATE TABLE IF NOT EXISTS warehouse.agg_daily (
    record_day DATE PRIMARY KEY,
    habit_id INT REFERENCES warehouse.dim_habits.habit_id,
    user_id INT REFERENCES warehouse.dim_users.user_id,
    category_id INT REFERENCES warehouse.dim_category.category_id,
    total_duration NUMERIC,
    total_records NUMERIC
);
