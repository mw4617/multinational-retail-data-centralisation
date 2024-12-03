--Task 7
select sum(staff_numbers) as total_staff_numbers, country_code from dim_store_details
group by country_code
order by sum(staff_numbers) desc
