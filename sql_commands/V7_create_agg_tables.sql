CREATE TABLE IF NOT EXISTS warehouse.agg_daily (
    record_day DATE,
    habit_id INT REFERENCES warehouse.dim_habits,
    user_id NUMERIC REFERENCES warehouse.dim_users,
    category_id INT REFERENCES warehouse.dim_category,
    total_duration NUMERIC,
    total_records NUMERIC
);
