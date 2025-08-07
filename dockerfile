# Stage 1: Building and installing dependencies
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Installing build-time system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copying requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copying application code
COPY ./src /app/src
COPY .project-root /app/.project-root
COPY ./model_path /app/model_path

# Stage 2: Production runtime image
FROM python:3.11-slim-bullseye AS production

WORKDIR /app

# Install only necessary runtime system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Createing non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copying installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copying app code and set ownership
COPY --from=builder --chown=appuser:appuser /app/src /app/src
COPY --from=builder --chown=appuser:appuser /app/.project-root /app/.project-root
COPY --from=builder --chown=appuser:appuser /app/model_path /app/model_path

# Createing logs directory with proper permissions
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Setting environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:$PATH" \
    PYTHONPATH="/app" \
    PORT=8000

# Adding health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Installing curl for health checks (minimal addition)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Switching to non-root user
USER appuser

# Expose port
EXPOSE ${PORT}


CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]