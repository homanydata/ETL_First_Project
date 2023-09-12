INSERT INTO warehouse.fct_records (habit_id, user_id, duration, record_date)
SELECT
    dim_habits.habit_id,
    dim_habits.category_id,
    stg_records.user_id,
    stg_records.duration,
    stg_records.record_date
INNER JOIN warehouse.dim_habits
    ON dim_habits.habit_name = stg_records.habit_name;