# ---------- Stage 1: builder ----------
# Installs dependencies into a virtualenv. pip, build caches, and any
# build tools stay in this stage and never reach the final image.
FROM python:3.11-alpine AS builder
WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runtime ----------
# Starts from a fresh base and copies in only what's needed to run.
FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY app.py .

# Don't run as root
RUN adduser -D appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
