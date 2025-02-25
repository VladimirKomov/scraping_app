# Using the official Python image
FROM python:3.12-slim

# Install the working directory
WORKDIR /app

# Installing Poetry
RUN pip install poetry

# Copy the project files (only necessary ones)
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

# Copy the rest of the code
COPY . .

# Specify the command to launch the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
