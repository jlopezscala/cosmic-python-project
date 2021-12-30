
# Worth checking out: https://pythonspeed.com/docker to build better Dockerfiles

FROM python:3.9-slim-buster
# Using Slim-buster and not Alpine because of: https://pythonspeed.com/articles/alpine-docker-python/
# Also Pypi wheels don't work in Alpine
ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.12

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p /src
COPY src/ /src/
COPY tests/ /tests/
COPY poetry.lock pyproject.toml /src/

WORKDIR /src

RUN poetry config virtualenvs.create false \
    && poetry install


ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80