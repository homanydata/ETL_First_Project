CREATE VIEW IF NOT EXISTS warehouse.daily_view AS
SELECT
    agg_daily.record_day,
    agg_daily.habit_id,
    agg_daily.user_id,
    dim_category.category_name,
    agg_daily.total_duration,
    agg_daily.total_records
FROM agg_daily
INNER JOIN dim_category
    ON dim_category.category_id = agg_daily.category_id
;

CREATE VIEW IF NOT EXISTS warehouse.habit_view AS
SELECT
    habit_id,
    category_name,
    user_id,
    SUM(total_duration) as total_duration,
    SUM(total_records) as total_records
FROM daily_view
GROUP BY
    habit_id,
    category_name,
    user_id
;