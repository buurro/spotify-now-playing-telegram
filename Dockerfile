FROM python:3.9.16-slim-buster

ENV PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.8.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    ffmpeg \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version \

WORKDIR /src
RUN mkdir /tmp/gifs/

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY ./ ./

CMD [ "poetry", "run", "python", "run.py" ]
