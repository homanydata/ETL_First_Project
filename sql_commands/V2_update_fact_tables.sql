INSERT INTO fact_records
SELECT
    dim_habits.habit_id,
    user_id,
    duration,
    timestamp
FROM staging_records
INNER JOIN dim_habits
    ON dim_habits.habit_name = staging_records.habit_name