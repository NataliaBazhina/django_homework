FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && \
    pip install poetry


COPY pyproject.toml poetry.lock ./


RUN cat pyproject.toml && \
    [ -f poetry.lock ] && echo "poetry.lock exists" || echo "WARNING: poetry.lock missing"


RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root


COPY . .

EXPOSE 8000