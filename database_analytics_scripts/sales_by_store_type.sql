--Task 5
create temp table sales_by_store_type_incomplete_temp as
select store_type, sum(product_price * product_quantity ) as total_sales from dim_store_details dsd
join orders_table ot on
dsd.store_code=ot.store_code
join dim_products dp on
ot.product_code=dp.product_code
group by store_type
order by sum(product_price * product_quantity ) desc;

select 
    store_type, 
    total_sales,
    round((total_sales * 100.0) / sum(total_sales) over (),2) as "sales_made(%)"
from sales_by_store_type_incomplete_temp
order by "sales_made(%)" desc;


