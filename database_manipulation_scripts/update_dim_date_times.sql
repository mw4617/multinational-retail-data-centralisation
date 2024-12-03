
--alters the datatypes of columns in orders dim_date_times
ALTER TABLE dim_date_times
ALTER COLUMN "timestamp" TYPE TIME USING "timestamp"::TIME,
ALTER COLUMN month  TYPE SMALLINT USING month::SMALLINT,
ALTER COLUMN year TYPE SMALLINT USING year::SMALLINT,
ALTER COLUMN day TYPE SMALLINT USING day::SMALLINT,
ALTER COLUMN time_period TYPE VARCHAR(10) USING time_period::VARCHAR(10),
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

