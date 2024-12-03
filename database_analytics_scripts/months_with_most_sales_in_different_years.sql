--Task 6
select sum(product_price*product_quantity) as total_sales,year,month from dim_products dp
join orders_table ot
on dp.product_code=ot.product_code
join dim_date_times ddt 
on ot.date_uuid=ddt.date_uuid
group by year, month
order by total_sales desc
limit 10


