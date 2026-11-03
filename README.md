# Demo shop

A tiny online shop for testing ngin8r's personal-data map (PR #392). Customers sign up,
order, pay and open support tickets; the shop emails them and reports signups to analytics.

Each piece is here for one feature:

| Code | Personal data | What it should trigger |
|---|---|---|
| `customers.email`, `full_name`, `phone` | contact | Labels; a `contact` row on the Data protection page |
| `customers.allergies`, read in `orders.place_order` | health, special | A `health, special` label; Radar raises its severity |
| `addresses.street`, `city`, `postcode` | location | A `location` label |
| `payments.card_last4` | financial | A `financial` label |
| `support_tickets.customer_email`, `message` | contact, free text | Labels; **never deleted**: an `erasure-gap` |
| `orders` | none | No label: the control |
| `accounts.close_account` | — | A deletion flow: deletes `customers` and `addresses`, anonymises `payments` |
| `mailer.py` → mail.example.com | email, name | An outside recipient, **declared** in `ngin8r-privacy.md` |
| `analytics.py` → analytics.example.com | email, city | An outside recipient, **not declared**: `undeclared-recipient` |
| branch `sms-reminders` | phone → sms.example.com | A new recipient for `compare` and `update` |

## Test plan

Run in order. Check each step before the next.

### 1. Docs with no privacy section yet

```sh
ngin8r init --repos /home/deepstack/Desktop/ttst-testing/demo-repo --system-name "Demo shop"
cd <the docs folder init printed>
ngin8r generate
ngin8r start
```

- [ ] **Labels:** select a table in the data-model diagram. Its Fields list shows a chip next to
      `email` (contact), `allergies` (health, special), `city` (location), `card_last4` (financial),
      `message` (free-text). `orders` has none. The ER diagram's field text names the category too.
- [ ] **Data protection page:** sidebar → Data → Data protection. One row per category; "Deleted by"
      names the close-account flow for customers and addresses; "No erasure found" names
      support tickets; "Sent to" names the mail and analytics services.
- [ ] **Download CSV**, top right of that page: one row per category where kept and per recipient.
- [ ] **Agent tool:** over MCP, `personal_data` lists the same.

### 2. Radar without declared recipients

```sh
ngin8r generate --radar
```

- [ ] Radar page: an `erasure-gap` hazard for support tickets.
- [ ] Radar page, under what it could not check: recipients were not checked, because `ngin8r.md`
      has no declared recipients.

### 3. Radar with declared recipients

Append `ngin8r-privacy.md` to the docs folder's `ngin8r.md`, then:

```sh
ngin8r generate --radar
```

- [ ] An `undeclared-recipient` hazard for the analytics service; none for the mail service.
- [ ] The "not checked" note is gone.

### 4. Confirm labels (as a writer, served with `ngin8r start`)

- [ ] Click the `allergies` chip → Confirmed, with a note. The chip turns solid.
- [ ] Click the `phone` chip → Another category → identifier. The chip shows identifier.
- [ ] Click the `message` chip → Not personal data. The chip is struck through.
- [ ] The Data protection page, the CSV and `personal_data` follow these marks.

### 5. Compare a branch

```sh
ngin8r compare --head sms-reminders
```

- [ ] The comparison treats personal data as a critical area: phone numbers now go to sms.example.com.

### 6. Update after the change lands

```sh
git -C /home/deepstack/Desktop/ttst-testing/demo-repo merge sms-reminders
ngin8r generate
```

- [ ] The SMS service appears in "Sent to" for contact data; the marks from step 4 still hold.
- [ ] Change the line `allergies` is read on in `orders.py`, update again: its label shows
      "the code it was marked against changed".
