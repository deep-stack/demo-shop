-- Demo data, as a few weeks of the shop running would leave it.

-- 60 customers, each with an address; every fifth one has an allergy on file.
INSERT INTO customers (email, full_name, phone, allergies, created_at)
SELECT 'customer' || n || '@team.example', 'Customer ' || n, '+1555010' || lpad(n::text, 4, '0'),
       CASE WHEN n % 5 = 0 THEN 'peanuts' END, now() - (90 - n) * interval '1 day'
FROM generate_series(1, 60) AS n;

INSERT INTO addresses (customer_id, street, city, postcode)
SELECT id, id || ' Main St', (ARRAY['Springfield', 'Riverton', 'Lakeside'])[1 + id % 3], lpad((10000 + id)::text, 5, '0')
FROM customers;

-- 200 orders, each with its payment, a few minutes apart.
INSERT INTO orders (customer_id, total, created_at)
SELECT 1 + n % 60, 500 + (n * 37) % 4000, now() - (200 - n) * interval '7 minutes'
FROM generate_series(1, 200) AS n;

INSERT INTO payments (customer_id, card_last4, amount, created_at)
SELECT customer_id, lpad((1000 + customer_id)::text, 4, '0'), total, created_at + interval '1 second'
FROM orders;

-- A few more orders, each with its payment.
INSERT INTO orders (customer_id, total, created_at)
SELECT customer_id, total, created_at + interval '4 seconds' FROM orders WHERE id IN (17, 42, 88, 131, 176);

INSERT INTO payments (customer_id, card_last4, amount, created_at)
SELECT customer_id, lpad((1000 + customer_id)::text, 4, '0'), total, created_at + interval '1 second'
FROM orders WHERE id > 200;

-- Support tickets from the contact form.
INSERT INTO support_tickets (customer_email, message, created_at)
SELECT 'customer' || (1 + n * 7 % 60) || '@team.example', 'Where is my order ' || n || '?', now() - n * interval '1 day'
FROM generate_series(1, 30) AS n;

-- Five customers who closed their accounts.
UPDATE payments SET card_last4 = NULL, customer_id = NULL WHERE customer_id IN (8, 15, 22, 29, 36);
UPDATE orders SET customer_id = NULL WHERE customer_id IN (8, 15, 22, 29, 36);
DELETE FROM addresses WHERE customer_id IN (8, 15, 22, 29, 36);
DELETE FROM customers WHERE id IN (8, 15, 22, 29, 36);
