# ----------------------------
# Stage 1: Build Stage
# ----------------------------
FROM python:3.12.6-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies into a virtual env
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Stage 2: Final Stage
# ----------------------------
FROM python:3.12.6-slim

# Set working directory
WORKDIR /app

# Copy virtualenv from build stage
COPY --from=build /opt/venv /opt/venv

# Update PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy app code
COPY . /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser \
    && chown -R appuser:appgroup /app
USER appuser

# Expose port
EXPOSE 5000

# Run Flask app with Gunicorn
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:5000", "app:app"]
