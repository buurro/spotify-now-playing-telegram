FROM python:3.9.16-slim-buster

RUN pip install pipx && \
	pipx install poetry && \
	export PATH="/root/.local/bin:$PATH"

WORKDIR /src

COPY pyproject.toml poetry.lock /src

RUN /root/.local/bin/poetry install

COPY . /src
CMD [ "/root/.local/bin/poetry", "run", "python", "/src/run.py" ]
