-- Logins for ngin8r's database source. shop_reader can only read, as ngin8r needs; shop_writer can also add orders,
-- which ngin8r should refuse to save. Demo passwords only: never reuse them.
CREATE ROLE shop_reader LOGIN PASSWORD 'reader-demo-pass';
GRANT CONNECT ON DATABASE shop TO shop_reader;
GRANT USAGE ON SCHEMA public TO shop_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shop_reader;

CREATE ROLE shop_writer LOGIN PASSWORD 'writer-demo-pass';
GRANT CONNECT ON DATABASE shop TO shop_writer;
GRANT USAGE ON SCHEMA public TO shop_writer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shop_writer;
GRANT INSERT ON orders TO shop_writer;
