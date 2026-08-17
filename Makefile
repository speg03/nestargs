.PHONY: all
all: dist

.PHONY: clean
clean:
	rm -rf ./dist

.PHONY: install
install:
	uv sync --dev

.PHONY: deps
deps:
	uv lock --upgrade

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest -v ./tests

.PHONY: dist
dist:
	uv build
