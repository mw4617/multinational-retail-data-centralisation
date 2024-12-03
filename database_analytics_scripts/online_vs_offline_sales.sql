--Task 4
create temp table online_vs_offline_sales_temp as
select product_quantity,product_code,
case 
 when store_code='WEB-1388012W' then 'Web'
 else 'Offline'
end as location
from orders_table;

select count(*) as number_of_sales, sum(product_quantity) as product_quantity_count, location from online_vs_offline_sales_temp
group by location
order by number_of_sales asc

