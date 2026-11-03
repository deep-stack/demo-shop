-- The shop's database.

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    full_name   TEXT NOT NULL,
    phone       TEXT,
    allergies   TEXT,              -- what the customer is allergic to, checked before a food order ships
    created_at  TEXT NOT NULL
);

CREATE TABLE addresses (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    street      TEXT NOT NULL,
    city        TEXT NOT NULL,
    postcode    TEXT NOT NULL
);

CREATE TABLE payments (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    card_last4  TEXT,
    amount      INTEGER NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    total       INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'new'
);

CREATE TABLE support_tickets (
    id             INTEGER PRIMARY KEY,
    customer_email TEXT NOT NULL,
    message        TEXT NOT NULL,
    created_at     TEXT NOT NULL
);
