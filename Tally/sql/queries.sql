--All expenses in a group, newest first, with the payer's name
SELECT 
    e.id, 
    e.description, 
    e.amount_cents, 
    e.category, 
    e.created_at, 
    u.name AS payer_name
FROM expenses e
JOIN users u ON e.paid_by = u.id
WHERE e.group_id = 1
ORDER BY e.created_at DESC;


/*
3|Supermarket run|3000|Groceries|2026-07-29 11:02:27.078448|Sara
2|Hotel Booking|12000|Travel|2026-07-27 11:02:27.074999|Ali
1|Beachside Dinner|6000|Food|2026-07-25 11:02:27.071409|Areeba
*/

--Expenses in a category within a date range
SELECT *
FROM expenses
WHERE category IN ('Food', 'Transport')
  AND created_at BETWEEN '2026-01-01 00:00:00' AND '2026-12-31 23:59:59';

--1|1|Beachside Dinner|6000|Food|1|2026-07-25 11:02:27.071409


--3. Total spent per category in a group
SELECT category, SUM(amount_cents) AS total_spent
FROM expenses
WHERE group_id = 1
GROUP BY category;

/*Food|6000
Groceries|3000
Travel|12000
sqlite> */

--4. Total each member has paid
SELECT u.id, u.name, SUM(e.amount_cents) AS total_paid
FROM users as u
JOIN expenses as e ON u.id = e.paid_by
WHERE e.group_id = 1
GROUP BY u.id, u.name;
/*1|Areeba|6000
2|Ali|12000
3|Sara|3000
sqlite> */

--5. Total each member owes (sum of their splits)
SELECT u.id, u.name, SUM(es.share_cents) AS total_owed
FROM users u
JOIN expense_splits es ON u.id = es.user_id
JOIN expenses e ON es.expense_id = e.id
WHERE e.group_id = 1
GROUP BY u.id, u.name;
/*1|Areeba|7000
2|Ali|7500
3|Sara|6500
 */

-- 7. Members who owe more than 5000 cents in total[cite: 1]
SELECT u.name, SUM(es.share_cents) AS total_owed 
FROM users u 
JOIN expense_splits es ON u.id = es.user_id 
GROUP BY u.id, u.name 
HAVING SUM(es.share_cents) > 5000;
/*Areeba|7000
Ali|7500
Sara|6500*/

-- 8. Members who have never paid for anything
SELECT u.name 
FROM users u 
LEFT JOIN expenses e ON u.id = e.paid_by 
WHERE e.id IS NULL;
--Zain

-- 10. Integrity check: expenses whose splits do NOT sum to the amount
SELECT e.id, e.amount_cents, SUM(es.share_cents) AS sum_splits
FROM expenses e
JOIN expense_splits es ON e.id = es.expense_id
GROUP BY e.id, e.amount_cents
HAVING e.amount_cents <> SUM(es.share_cents);


