.PHONY: test

test:
	poetry run pytest -v --cov=nestargs/ --cov-report=term-missing tests/
