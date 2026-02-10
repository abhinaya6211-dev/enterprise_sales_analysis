select * from dummy limit 10

--Q1. What is the total revenue by year?
SELECT 
	Year,
	SUM(Trade_Sales_Dollars) AS total_revenue
FROM dummy
GROUP BY year
ORDER BY year

--Q2. Which states generate the highest revenue?
select 
	state/province,
	SUM(trade_sales_dollars) as total_revenue
from dummy
group by state/province
order by total_revenue
limit 10
--Q3. How is revenue distributed across markets (USA, Canada, International)?
select
	market,
	SUM(trade_sales_dollars) as total_revenue
from dummy
group by market
order by total_revenue desc
limit 10
--Q4. What are the top product segments by revenue?
select 
	product_segment,
	SUM(trade_sales_dollars) as total_revenue
from dummy
group by product_segment
order by total_revenue desc
limit 10
--Q5. Which product segments sell the highest volume (gallons)?
select
	product_segment,
	SUM(trade_sales_gallons) as total_gallons
from dummy
group by product_segment
order by total_gallons desc
limit 10
--Q6. What is the average price per gallon by product segment?
select
	product_segment,
	SUM(price_per_gallon) as avg_price_per_gallons
from dummy
where price_per_gallon is not null
group by product_segment
order by avg_price_per_gallons desc
limit 10
--Q7. Which states have the highest price per gallon?
select
	state,
	SUM(price_per_gallon) as avg_price_per_gallons
from dummy
where price_per_gallon is not null
group by state
order by avg_price_per_gallons desc
limit 10
--Q8. Compare two states’ performance
SELECT
    state,
    year,
    SUM(trade_sales_dollars) AS revenue
FROM dummy
WHERE state IN (:state_1, :state_2)
GROUP BY state, year
ORDER BY state, year;
--Q9. Year-over-year revenue growth by state
-- LAG(window func) = Fetches the previous row’s(year) value
SELECT
    state,
    year,
    SUM(trade_sales_dollars) AS revenue,
    LAG(SUM(trade_sales_dollars)) OVER (
        PARTITION BY state
        ORDER BY year
    ) AS prev_year_revenue
FROM dummy
GROUP BY state, year;
		
--Q10. Which segments generate high revenue but low volume?
-- helping distinguish premium-priced products from volume-driven ones.
SELECT
    product_segment,
    SUM(trade_sales_dollars) AS total_revenue,
    SUM(trade_sales_gallons) AS total_gallons,
    CAST(
        SUM(trade_sales_dollars) / NULLIF(SUM(trade_sales_gallons), 0)
        AS numeric(10,2)
    ) AS effective_price_per_gallon
FROM dummy
GROUP BY product_segment
ORDER BY effective_price_per_gallon DESC;


