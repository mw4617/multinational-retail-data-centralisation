# Multinational Retail Data Centralisation Project Manual

Welcome to the **Multinational Retail Data Centralisation** project! This manual provides a step-by-step guide to set up, run, and manage this project. Follow these instructions carefully to ensure smooth execution of the project.

---

## **Project Overview**

The **Multinational Retail Data Centralisation** project is designed to centralize and clean data from multiple sources, store it in a structured database, and run analytical queries to gain insights. The project uses **Python scripts** for data extraction, cleaning, and uploading, and **SQL scripts** for database manipulation and analytics.

---

## **Step A: Setting Up the Database**

1. **Install PostgreSQL:**
   - Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/).
   - During installation, set a username (`postgres`) and a secure password.

2. **Create a New Database:**
   - Open **pgAdmin4** or your preferred database management tool.
   - Create a new database named `sales_data`.

3. **Install Required Python Libraries:**
   - Open a terminal or command prompt.
   - Run the following command to install the required Python libraries:
     ```bash
     pip install pandas sqlalchemy psycopg2 boto3 tabula-py pyyaml
     ```

4. **Set Up `db_creds.yaml`:**
   - Create a YAML file named `db_creds.yaml` in the project directory with the following structure:
     ```yaml
     RDS_HOST: <Your AWS RDS Host>
     RDS_PASSWORD: <Your AWS RDS Password>
     RDS_USER: <Your AWS RDS Username>
     RDS_DATABASE: <Your AWS RDS Database Name>
     RDS_PORT: <Your AWS RDS Port>
     ```

   **Note:** Add this file to `.gitignore` to prevent uploading credentials to a public repository.

---

## **Step B: Running Python Scripts**

1. **Open Each Python Script in VS Code:**
   - Use VS Code or your preferred IDE to open `data_extraction.py`, `data_cleaning.py`, and `database_utils.py`.
   - Review the code and ensure all configurations match your setup.

2. **Open the `data_cleaning.py` script and run it:
   - This script links to other scripts so it's not necessary to run other python scripts.

3. **Verify the Data:**
   - After running the scripts, check the `sales_data` database in PostgreSQL to ensure tables are populated.

---

## **Step C: Executing SQL Scripts**

1. **Open SQL Scripts:**
   - Navigate to the `database_manipulation_scripts` folder.
   - Open each `.sql` file individually using a SQL editor (pgAdmin4 or VS Code with SQL extensions).

2. **Run SQL Scripts in the Following Order:**
   - Execute the following SQL scripts sequentially to set up and modify the database schema. Below is a table with task numbers, script names, and their purposes:

   | **Task Number** | **Script File Name**            | **Description**                                                                                   |
   |------------------|--------------------------------|---------------------------------------------------------------------------------------------------|
   | **Task 1**       | `update_orders_table.sql`      | Cast columns in the `orders_table` to their correct data types.                                  |
   | **Task 2**       | `update_dim_users.sql`         | Cast columns in the `dim_users` table to their correct data types.                               |
   | **Task 3**       | `update_dim_store_details.sql` | Update the `dim_store_details` table to standardize column data types and clean invalid entries.  |
   | **Task 4**       | `update_dim_products.sql`      | Add the `weight_class` column to `dim_products`, clean the table, and standardize column types.   |
   | **Task 5**       | `update_dim_card_details.sql`  | Update the `dim_card_details` table to standardize data types.                                   |
   | **Task 6**       | `update_dim_date_times.sql`    | Update the `dim_date_times` table, ensuring correct data types for date and time fields.          |
   | **Task 7**       | `create_primary_keys.sql`      | Add primary keys to all dim tables (`dim_*`).                                               |
   | **Task 8**       | `create_foreign_keys.sql`      | Add foreign key constraints to link `orders_table` with the dim tables (`dim_*`).           |


   **Tip:** Each script modifies or updates tables. Run them sequentially to avoid errors.

---

## **Step D: Running Analytics Queries**

1. **Open Analytics SQL Scripts:**
   - Navigate to the `database_analytics_scripts` folder.
   - Open each `.sql` file individually.

2. **Run Analytical Queries:**
   - Execute each script to gain insights into the business operations. Below is the list of all queries and their corresponding tasks:

   | **Task Number** | **Query File Name**                                 | **Description**                                                                 |
   |------------------|----------------------------------------------------|---------------------------------------------------------------------------------|
   | **Task 1**       | `no_stores_by_country.sql`                         | Find the total number of stores in each country.                                |
   | **Task 2**       | `locations_with_most_stores.sql`                   | Identify the localities with the highest number of stores.                      |
   | **Task 3**       | `months_with_most_sales.sql`                       | Determine the months with the largest total sales.                              |
   | **Task 4**       | `online_vs_offline_sales.sql`                      | Compare the total sales made online versus offline.                             |
   | **Task 5**       | `sales_by_store_type.sql`                          | Calculate the percentage of sales made by each store type.                      |
   | **Task 6**       | `months_with_most_sales_in_different_years.sql`    | Identify the months with the highest sales across different years.              |
   | **Task 7**       | `staff_headcount.sql`                              | Compute the total number of staff by country.                                   |
   | **Task 8**       | `german_store_type_sales.sql`                      | Determine which store type generates the most sales in Germany.                 |
   | **Task 9**       | `average_time_between_sales.sql`                   | Calculate the average time between sales by year.                               |

3. **Export Results:**
   - Save query results as CSV files or screenshots for reporting purposes.
