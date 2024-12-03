--Task 2
select locality, count(locality) as total_no_stores from dim_store_details
where store_type not like 'Web Portal'
group by locality
order by count(locality) desc
limit 6