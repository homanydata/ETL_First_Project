SELECT
    record_day,
    SUM(total_duration) AS total_duration
FROM warehouse.daily_view
WHERE user_id = %s
    AND {} = %s
GROUP BY
    record_day,
    {}
;