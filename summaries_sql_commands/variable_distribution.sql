SELECT
    {},
    SUM(total_duration) AS total_duration
FROM warehouse.habit_view
WHERE user_id = %s
GROUP BY
    {}
;