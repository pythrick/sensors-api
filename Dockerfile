FROM python:3.10.4-slim

ARG ENV

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=true \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin" \
  PYTHONPATH="$PYTHONPATH:/app"

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /tmp
COPY pyproject.toml poetry.lock ./
RUN poetry install $(test "$ENV" == production && echo "--no-dev")

WORKDIR /app
COPY sensors_api ./sensors_api
COPY config.py ./
COPY manage.py ./

ENTRYPOINT ["python", "manage.py"]
