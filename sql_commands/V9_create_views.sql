CREATE OR REPLACE VIEW warehouse.daily_view AS
SELECT
    agg_daily.record_day,
    dim_habits.habit_name,
    agg_daily.user_id,
    dim_category.category_name,
    agg_daily.total_duration,
    agg_daily.total_records
FROM warehouse.agg_daily
INNER JOIN warehouse.dim_category
    ON dim_category.category_id = agg_daily.category_id
INNER JOIN warehouse.dim_habits
    ON dim_habits.habit_id = agg_daily.habit_id
;

CREATE OR REPLACE VIEW warehouse.habit_view AS
SELECT
    habit_name,
    category_name,
    user_id,
    SUM(total_duration) as total_duration,
    SUM(total_records) as total_records
FROM warehouse.daily_view
GROUP BY
    habit_name,
    category_name,
    user_id
;