--Task 9
WITH cte AS(
SELECT TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp),
'YYYY-MM-DD HH24:MI:SS') as "timestamp", year FROM dim_date_times
ORDER BY "timestamp" DESC
), cte2 AS(
SELECT
year,
"timestamp",
LEAD("timestamp") OVER (ORDER BY "timestamp" DESC) as time_diff
FROM cte
) SELECT year, AVG(("timestamp" - time_diff)) as average_time_between_sales FROM cte2
GROUP BY year
ORDER BY  year asc

