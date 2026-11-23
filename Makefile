# The shop's checks, as CI runs them.
check: lint unit

lint:
	ruff check --select E9,F .

unit:
	pytest tests/unit tests/test_routing.py -v --junitxml=reports/unit.xml

test-all:
	./scripts/ci.sh
