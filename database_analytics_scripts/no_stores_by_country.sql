--Task 1
select country_code as country, count(country_code) as total_no_stores from dim_store_details
where store_type not like 'Web Portal'
group by country_code
order by count(country_code) desc

