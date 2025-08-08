FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \\
  && apt-get install -y gcc libpg-dev \\
  && apt-get clean \\
  && rm -rf /var/lib/apt/lists/\*

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi


COPY . .

EXPOSE 8000