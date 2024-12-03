--Task 3
select sum(product_price*product_quantity) as total_sales,month from dim_products dp
join orders_table ot
on dp.product_code=ot.product_code
join dim_date_times ddt 
on ot.date_uuid=ddt.date_uuid
group by month
order by sum(product_price*product_quantity) desc 
limit 6
