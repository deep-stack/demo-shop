-- Logins besides the shop's own: shop_reader for reporting, which only reads, and shop_writer for importing orders.
-- Demo passwords only: never reuse them.
CREATE ROLE shop_reader LOGIN PASSWORD 'reader-demo-pass';
GRANT CONNECT ON DATABASE shop TO shop_reader;
GRANT USAGE ON SCHEMA public TO shop_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shop_reader;

CREATE ROLE shop_writer LOGIN PASSWORD 'writer-demo-pass';
GRANT CONNECT ON DATABASE shop TO shop_writer;
GRANT USAGE ON SCHEMA public TO shop_writer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shop_writer;
GRANT INSERT ON orders TO shop_writer;
