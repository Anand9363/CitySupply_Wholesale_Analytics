
-- Query 1: Total number of orders
SELECT COUNT(*) AS total_orders
FROM journeys;


-- Query 2: Supplier-wise order count
SELECT
    supplier_id,
    COUNT(*) AS total_orders
FROM journeys
GROUP BY supplier_id
ORDER BY total_orders DESC;


-- Query 3: Overall OTIF performance
SELECT
    COUNT(*) AS total_orders,
    SUM(otif) AS successful_orders,
    ROUND(AVG(otif) * 100, 2) AS otif_percentage
FROM journeys;
