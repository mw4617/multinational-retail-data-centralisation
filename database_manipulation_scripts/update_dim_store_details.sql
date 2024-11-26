--store_type can accept null values
ALTER TABLE dim_store_details
ALTER COLUMN store_type DROP NOT NULL;

--setting N/A values to Null
UPDATE dim_store_details
SET address=null,
longitude=null,
locality=null
WHERE index=0;

--removing non-digits from staff number column
UPDATE dim_store_details
SET staff_numbers = REGEXP_REPLACE(staff_numbers, '[^0-9]', '', 'g');

--alters the datatypes of columns in orders dim_store_details
ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE NUMERIC USING longitude::NUMERIC,
ALTER COLUMN locality  TYPE VARCHAR(255) USING locality::VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(255) USING store_code::VARCHAR(255),
ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
ALTER COLUMN store_type TYPE VARCHAR(255) USING store_type::VARCHAR(255),
ALTER COLUMN latitude TYPE NUMERIC USING latitude::NUMERIC,
ALTER COLUMN country_code TYPE VARCHAR(3) USING country_code::VARCHAR(3),
ALTER COLUMN continent TYPE VARCHAR(255) USING continent::VARCHAR(255);

