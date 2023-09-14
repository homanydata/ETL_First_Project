-- get last day aggregated
CREATE TEMP TABLE LAST_DAY AS (
    SELECT
        CAST(record_date AS DATE)
    FROM warehouse.fct_records
    ORDER BY
        CAST(record_date AS DATE) DESC
    LIMIT 1
)
;
-- remove last day froma agg to update it
DELETE FROM warehouse.agg_daily
WHERE CAST(record_day AS DATE) = (SELECT * FROM LAST_DAY)
;
-- insert new data including last day data aggregation
INSERT INTO warehouse.agg_daily (record_day, habit_id, category_id, user_id, total_duration, total_records)
SELECT
    CAST(record_date AS DATE) AS record_day,
    habit_id,
    category_id,
    user_id,
    SUM(duration) AS total_duration,
    COUNT(record_date) AS total_records
FROM warehouse.fct_records
WHERE CAST(record_date AS DATE) >= (SELECT * FROM LAST_DAY)
GROUP BY
    CAST(record_date AS DATE),
    habit_id,
    category_id,
    user_id
;