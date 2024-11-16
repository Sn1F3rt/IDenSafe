env:
	uv venv

activate:
	source .venv/bin/activate

install:
	uv sync --no-dev --extra prod

install-dev:
	uv sync --all-extras

format:
	ruff check --select I --fix .
	ruff format .

debug:
	flask --app launcher:app run --debug

prod:
	gunicorn --bind 0.0.0.0:5000 launcher:app

prods:
	gunicorn --bind 0.0.0.0:5000 launcher:app $(filter-out $@,$(MAKECMDGOALS))

cmd:
	flask --app launcher:app $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: env activate install install-dev format debug prod prods cmd
.DEFAULT_GOAL := debug
