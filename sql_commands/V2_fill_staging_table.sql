-- V0: Insert Records into Staging Table
INSERT INTO warehouse.stg_records (
    habit_name,
    category_name,
    user_id,
    duration,
    chat_id,
    username,
    first_name,
    last_name,
    is_premium,
    language_code,
    record_date
)
VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
;
