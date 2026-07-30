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

-- 6. Net balance per member in a group (what they paid minus what they owe)
SELECT
    u.id,
    u.name,
    COALESCE(paid.total_paid, 0) - COALESCE(owed.total_owed, 0) AS net_balance
FROM users u
JOIN group_members gm ON gm.user_id = u.id AND gm.group_id = 1
LEFT JOIN (
    SELECT paid_by, SUM(amount_cents) AS total_paid
    FROM expenses
    WHERE group_id = 1
    GROUP BY paid_by
) paid ON paid.paid_by = u.id
LEFT JOIN (
    SELECT es.user_id, SUM(es.share_cents) AS total_owed
    FROM expense_splits es
    JOIN expenses e ON e.id = es.expense_id
    WHERE e.group_id = 1
    GROUP BY es.user_id
) owed ON owed.user_id = u.id;
/*1|Areeba|-1000
2|Ali|4500
3|Sara|-3500
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

-- 9. Create a reusable view of per-member balances, then query it
CREATE VIEW vw_member_balances AS
SELECT 
    gm.group_id,
    u.id AS user_id,
    u.name,
    COALESCE(p.total_paid, 0) - COALESCE(o.total_owed, 0) AS net_balance
FROM users u
JOIN group_members gm ON u.id = gm.user_id
LEFT JOIN (
    SELECT paid_by AS user_id, group_id, SUM(amount_cents) AS total_paid
    FROM expenses
    GROUP BY paid_by, group_id
) p ON p.user_id = u.id AND p.group_id = gm.group_id
LEFT JOIN (
    SELECT es.user_id, e.group_id, SUM(es.share_cents) AS total_owed
    FROM expense_splits es
    JOIN expenses e ON es.expense_id = e.id
    GROUP BY es.user_id, e.group_id
) o ON o.user_id = u.id AND o.group_id = gm.group_id;

-- 10. Integrity check: expenses whose splits do NOT sum to the amount
SELECT e.id, e.amount_cents, SUM(es.share_cents) AS sum_splits
FROM expenses e
JOIN expense_splits es ON e.id = es.expense_id
GROUP BY e.id, e.amount_cents
HAVING e.amount_cents <> SUM(es.share_cents);


