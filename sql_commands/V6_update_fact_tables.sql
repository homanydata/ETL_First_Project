INSERT INTO warehouse.fct_records (habit_id, category_id, user_id, duration, record_date)
SELECT
    dim_habits.habit_id,
    dim_habits.category_id,
    stg_records.user_id,
    stg_records.duration,
    to_timestamp(stg_records.record_date_unix) AS record_date
FROM warehouse.stg_records
INNER JOIN warehouse.dim_habits
    ON dim_habits.habit_name = stg_records.habit_name;