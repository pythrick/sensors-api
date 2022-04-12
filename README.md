# Sensors API

Public API to receive data from multiple IoT sensors

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Run It](#run-it)
  - [API Docs](#api-docs)
  - [Tests](#tests)
  - [Lint and Formatting](#lint-and-formatting)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)


## About The Project

Sensors API is an application which demonstrates the following capabilities:
- [x] Create an API endpoint which can receive data from a streaming device and store it
- [x] Create a simulator which posts data at specific intervals to the above endpoint in the format listed
below. There should be at least 10 devices reporting through the simulator
- [x] Create an API endpoint that returns a histogram of status for a given device id

#### Addicional Notes:
- Every sensor will always send a "deviceId" (string) and a "timestamp" (ISO-formatted timestamp string)
- Status can have only one of the following values [ON, OFF, ACTIVE, INACTIVE]

### Built With

This project was built with the following technologies:

- [Python](https://python.org/)
- [Poetry](https://python-poetry.org)
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Typer](https://typer.tiangolo.com/)
- [SQLAlchemy](https://sqlalchemy.org/)
- [PyTest](https://pytest.org)
- [Docker](https://docker.com)
- [pre-commit](https://pre-commit.com/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

List of things you need to use the software and how to install them.
- [Python 3.10+](https://python.org/)
- [Poetry](https://python-poetry.org)
- [Docker](https://www.docker.com/get-started) (optional)
- [docker-compose](https://docs.docker.com/compose/install/) (optional)

#### Env file
Create a copy from template file `local.env`:
```shell
cp local.env .env
```
Edit the new `.env` file
```text
ENV=local <--------- (string) Name of the running environment (local, staging, production...)
DEBUG= <------------ (boolean) Enables SQL echo and Hot Reload for API server
DATABASE_URL= <----- (connection string) Database connection string, only `asyncpg` and `aiosqlite` are installed:
                       - postgresql+asyncpg://...:...@db:5432/sensors-api
                       - sqlite+aiosqlite:///db.sqlite3
                       - sqlite+aiosqlite://


# Environment Variables for PostgreSQL container in docker-compose.yaml
POSTGRES_PASSWORD= <--- (string) Password to be created in PostgreSQL container
POSTGRES_USER= <------- (string) Username to be created in PostgreSQL container
POSTGRES_DB= <--------- (string) Database to be created in PostgreSQL container
```

### Installation
Install the project and its dependencies + pre commit hooks running the following:
```shell
make install
```

### Run it
Run the API server with:
```shell
poetry run api
```

Run the Simulator with default parameters (10 devices, random streaming interval):
```shell
poetry run simulator
```

Run the Simulator with passing optional parameters:
```shell
poetry run simulator --devices=50 --streaming-interval=1 --base-url=http://localhost:8000
```

#### Run with Docker and Docker Compose
There's an option to run using Docker containers. The current `docker-compose.yml` has the following available services:
- API Server: `api`
- Simulator Scripts: `simulator`
- PostgreSQL Database: `db`

You can get them up and running altogether running:
```shell
docker-compose up
```

Or run them separately, first the API:
```shell
docker-compose up api
```
And next the Simulator:
```shell
docker-compose up simulator
```

### API Docs
The API documentation using OpenAPI spec (aka Swagger) is be available in `/docs` endpoint (http://localhost:8000/docs).


### Tests

Just run the command above.

```shell
make test
```


### Lint and Formatting
Run the following:
```shell
make lint
```

## Roadmap
Some possible improvements for this project:
- [ ] Add deployment configuration
- [ ] Add database migration support
- [ ] Add Authentication and Authorization
- [ ] Add more test cases

## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Patrick Rodrigues - [@pythrick](https://twitter.com/pythrick) - contact@patrickrodrigues.me
