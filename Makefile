env:
	uv venv

dev:
	uv sync --all-extras

prod:
	uv sync --no-dev --extra prod

activate:
	source .venv/bin/activate

format:
	ruff check --select I --fix .
	ruff format .

run:
	flask --app launcher:app run --debug

cmd:
	flask --app launcher:app $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: env dev prod activate format run cmd
.DEFAULT_GOAL := run
