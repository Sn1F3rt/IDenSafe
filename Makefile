env:
	uv sync --no-dev

dev:
	uv sync --all-extras

format:
	ruff check --select I --fix .
	ruff format .

run:
	flask --app launcher:app run --debug

cmd:
	flask --app launcher:app $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: env dev format run
.DEFAULT_GOAL := run
