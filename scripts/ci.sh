#!/usr/bin/env bash
# Everything that needs the database or a running shop: the schema, then the integration and the end-to-end tests.
set -euo pipefail
psql "$DATABASE_URL" -f db/schema.sql
pytest tests/integration tests/test_order_records.py -v --junitxml=reports/integration.xml
pytest tests/e2e tests/test_storefront.py -v --junitxml=reports/e2e.xml
