SELECT
    fct_records.record_date,
    dim_habits.habit_name,
    dim_category.category_name,
    fct_records.duration
FROM warehouse.fct_records
INNER JOIN warehouse.dim_category
    ON dim_category.category_id = fct_records.category_id
INNER JOIN warehouse.dim_habits
    ON dim_habits.habit_id = fct_records.habit_id
WHERE fct_records.user_id = %s
ORDER BY
    fct_records.record_date