FROM python:3.9.6-slim
WORKDIR /chibawest-gamecenter-bot

RUN apt-get update && apt-get install -y \
  git \
  sqlite3 \
  wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip \
  && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project false \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY chibawest_gamecenter_bot ./chibawest_gamecenter_bot

ENV GOOGLE_APPLICATION_CREDENTIALS /chibawest-gamecenter-bot/data/google_application_credentials.json

CMD ["poetry", "run", "start"]