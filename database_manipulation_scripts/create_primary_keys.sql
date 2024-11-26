-- Add primary key to dim_card_details
ALTER TABLE dim_card_details
ADD CONSTRAINT pk_dim_card_details PRIMARY KEY (card_number);

-- Add primary key to dim_users
ALTER TABLE dim_users
ADD CONSTRAINT pk_dim_users PRIMARY KEY (user_uuid);

-- Add primary key to dim_store_details
ALTER TABLE dim_store_details
ADD CONSTRAINT pk_dim_store_details PRIMARY KEY (store_code);

-- Add primary key to dim_products
ALTER TABLE dim_products
ADD CONSTRAINT pk_dim_products PRIMARY KEY (product_code);

-- Add primary key to dim_date_times
ALTER TABLE dim_date_times
ADD CONSTRAINT pk_dim_date_times PRIMARY KEY (date_uuid);