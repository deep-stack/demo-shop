-- The shop's database.

CREATE TABLE customers (
    id          serial PRIMARY KEY,
    email       text NOT NULL UNIQUE,
    full_name   text NOT NULL,
    phone       text,
    allergies   text,              -- what the customer is allergic to, checked before a food order ships
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE addresses (
    id          serial PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customers(id),
    street      text NOT NULL,
    city        text NOT NULL,
    postcode    text NOT NULL
);

CREATE TABLE payments (
    id          serial PRIMARY KEY,
    customer_id integer REFERENCES customers(id),
    card_last4  text,
    amount      integer NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
    id          serial PRIMARY KEY,
    customer_id integer REFERENCES customers(id),
    total       integer NOT NULL,
    status      text NOT NULL DEFAULT 'new',
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE support_tickets (
    id             serial PRIMARY KEY,
    customer_email text NOT NULL,
    message        text NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now()
);
