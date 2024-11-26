--alters the datatypes of columns in orders dim_users
ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(255) USING first_name::VARCHAR(255),
ALTER COLUMN last_name  TYPE VARCHAR(255) USING last_name::VARCHAR(255),
ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
ALTER COLUMN country_code TYPE VARCHAR(3) USING country_code::VARCHAR(3),
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
ALTER COLUMN join_date TYPE DATE USING join_date::DATE;

