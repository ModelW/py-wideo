.PHONY: format

format:
	poetry run python -m isort --profile black src
	poetry run python -m black src
