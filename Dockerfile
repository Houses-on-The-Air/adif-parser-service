# Stage 1: Build
FROM python:3.14 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix="/install" -r requirements.txt

# Stage 2: Runtime
FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Expose port and run the application
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
