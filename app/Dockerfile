FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

COPY ./ /app

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
