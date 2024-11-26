--removing pound symbol from product price column
UPDATE dim_products
SET product_price = REGEXP_REPLACE(product_price, '£', '', 'g');

ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;

--populating the still_available column with True / False
UPDATE dim_products
SET still_available = CASE
    WHEN still_available like 'Removed' THEN 'False'
    ELSE 'True'
END;

--creating a new weight class column
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(14);

--populating the weight class column
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight <140 THEN 'Heavy'
    ELSE 'Truck_Required'  -- optional
END;

--alters the datatypes of columns in orders dim_products
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE NUMERIC USING product_price::NUMERIC,
ALTER COLUMN weight TYPE NUMERIC USING weight::NUMERIC,
ALTER COLUMN "EAN" TYPE VARCHAR(13) USING "EAN"::VARCHAR(13),
ALTER COLUMN product_code TYPE VARCHAR(11) USING product_code::VARCHAR(11),
ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
ALTER COLUMN still_available TYPE BOOL USING still_available::BOOL;