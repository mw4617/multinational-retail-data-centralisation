--alters the datatypes of columns in orders table
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
ALTER COLUMN card_number TYPE VARCHAR(20) USING card_number::VARCHAR(20),
ALTER COLUMN store_code TYPE VARCHAR(20) USING store_code::VARCHAR(20),
ALTER COLUMN product_code TYPE VARCHAR(20) USING product_code::VARCHAR(20),
ALTER COLUMN product_quantity TYPE smallint USING product_quantity::smallint;

