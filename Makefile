update-precommit:
	poetry run pre-commit autoupdate

install:
	poetry install
	poetry run pre-commit install

run:
	poetry run sensors_api

simulator:
	poetry run sensors_simulator

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx

pyformat:
	poetry run pre-commit run -a -v isort && poetry run pre-commit run -a -v black
