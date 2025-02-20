# Set the base Python image
ARG PYTHON_VERSION=3.12.9
FROM --platform=linux/amd64 python:${PYTHON_VERSION}-bullseye AS base

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_NAME=postgres
ENV DATABASE_USER=postgres
ENV DATABASE_PASSWORD=postgres@123
ENV DATABASE_HOST=127.0.0.1
ENV DATABASE_PORT=5432

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (for PostgreSQL client and other tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user and group for running the app.
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Switch to the non-privileged user
USER appuser

# Copy the requirements.txt and install dependencies
COPY --chown=appuser:appgroup requirements.txt . 
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt 

# Copy the rest of the application code into the container
COPY --chown=appuser:appgroup . .

# Expose the port that the application listens on
EXPOSE 8080

# Run the application (ensure the correct shell is used to execute manage.py)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]