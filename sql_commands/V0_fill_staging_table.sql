-- V0: Insert Records into Staging Table
INSERT INTO staging_records (
    habit_name,
    user_id,
    chat_id,
    username,
    first_name,
    last_name,
    is_premium,
    language_code,
    duration,
    timestamp
)
VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
;
