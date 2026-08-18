.PHONY: all
all: dist

.PHONY: clean
clean:
	rm -rf ./dist

.PHONY: deps
deps:
	uv lock --upgrade

.PHONY: install
install:
	uv sync --locked --dev

.PHONY: lint
lint:
	uv run --locked pre-commit run --all-files

.PHONY: test
test:
	uv run --locked pytest -v ./tests

.PHONY: dist
dist:
	uv build

.PHONY: install-docs
install-docs:
	uv sync --locked --only-group docs

.PHONY: docs
docs:
	uv run --locked zensical build --clean --strict

.PHONY: serve
serve:
	uv run --locked zensical serve
