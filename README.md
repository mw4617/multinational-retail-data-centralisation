# Multinational Retail Data Centralisation Project Manual

Welcome to the **Multinational Retail Data Centralisation** project! This manual provides a step-by-step guide to set up, run, and manage this project. Follow these instructions carefully to ensure smooth execution of the project.

---

## **Project Overview**

The **Multinational Retail Data Centralisation** project is designed to centralize and clean data from multiple sources, store it in a structured database, and run analytical queries to gain insights. The project uses **Python scripts** for data extraction, cleaning, and uploading, and **SQL scripts** for database manipulation and analytics.

---

## **Folder Structure**

The project is structured as follows: ## **Step A: Setting Up the Database**

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

2. **Run the data_cleaning.py script:
   - This script incorporates other scripts so it's not necessary to run other python scripts.

3. **Verify the Data:**
   - After running the scripts, check the `sales_data` database in PostgreSQL to ensure tables are populated.

---

## **Step C: Executing SQL Scripts**

1. **Open SQL Scripts:**
   - Navigate to the `database_manipulation_scripts` folder.
   - Open each `.sql` file individually using a SQL editor (pgAdmin4 or VS Code with SQL extensions).

2. **Run SQL Scripts in the Following Order:**
   1. `update_dim_users.sql`
   2. `update_dim_store_details.sql`
   3. `update_dim_products.sql`
   4. `update_dim_card_details.sql`
   5. `update_dim_date_times.sql`
   6. `update_orders_table.sql`
   7. `create_primary_keys.sql`
   8. `create_foreign_keys.sql`

   **Tip:** Each script modifies or updates tables. Run them sequentially to avoid errors.

---

## **Step D: Running Analytics Queries**

1. **Open Analytics SQL Scripts:**
   - Navigate to the `database_analytics_scripts` folder.
   - Open each `.sql` file individually.

2. **Run Analytical Queries:**
   - Execute each script to get insights such as:
     - Number of stores by country (`no_stores_by_country.sql`)
     - Months with the highest sales (`months_with_most_sales.sql`)
     - Online vs. offline sales comparison (`online_vs_offline_sales.sql`)

3. **Export Results:**
   - Save query results as CSV files or screenshots for reporting purposes.
