-- V0: Insert Records into Staging Table
INSERT INTO warehouse.stg_records (
    habit_name,
    user_id,
    chat_id,
    username,
    first_name,
    last_name,
    is_premium,
    language_code,
    duration,
    record_date,
    category_name,
)
VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
;
