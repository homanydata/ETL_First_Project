-- ONLY FOR TEST
TRUNCATE warehouse.agg_daily;
INSERT INTO warehouse.agg_daily (record_day, habit_id, category_id, user_id, total_duration, total_records)
SELECT
    CAST(record_date AS DATE) AS record_day,
    habit_id,
    category_id,
    user_id,
    SUM(duration) AS total_duration,
    COUNT(record_date) AS total_records
FROM warehouse.fct_records
-- WHERE CAST(record_date AS DATE) >= (SELECT * FROM LAST_DAY)
GROUP BY
    CAST(record_date AS DATE),
    habit_id,
    category_id,
    user_id
ORDER BY
    CAST(record_date AS DATE)
;