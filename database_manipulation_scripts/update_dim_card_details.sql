--alters the datatypes of columns in orders dim_card_details
ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19) USING card_number::VARCHAR(19),
ALTER COLUMN expiry_date TYPE VARCHAR(5) USING expiry_date::VARCHAR(5),
ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;


