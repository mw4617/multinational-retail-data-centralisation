--Task 8
select sum(product_price*product_quantity) as total_sales,store_type,country_code from dim_products dp
join orders_table ot 
on dp.product_code=ot.product_code
join dim_store_details dsd 
on ot.store_code=dsd.store_code
group by store_type,country_code
having country_code like 'DE'
order by sum(product_price*product_quantity) asc