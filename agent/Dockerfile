FROM python:3.12-slim
WORKDIR /app

# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy dependency files first for better caching
COPY ./agent/pyproject.toml ./agent/README.md ./
RUN poetry lock
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY ./agent ./

EXPOSE 8001
CMD ["poetry", "run", "python", "-m", "server"]