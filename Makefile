.PHONY: test

test:
	poetry run pytest -v --cov=nestargs/ tests/
