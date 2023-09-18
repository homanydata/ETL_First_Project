SELECT
    habit_name,
    SUM(total_duration) AS total_duration,
    SUM(total_records) AS total_records
FROM warehouse.daily_view
WHERE user_id = %s
    AND (
        -- this is special one for week
        (%s= 'week' AND record_day >= DATE_TRUNC(%s, CURRENT_DATE) AND record_day < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week')
        OR
        (EXTRACT(%s FROM record_day) = EXTRACT(%s FROM NOW()))
    )
GROUP BY
    user_id,
    habit_name
;