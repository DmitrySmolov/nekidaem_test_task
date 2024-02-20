FROM python:3.12-slim AS base
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM base AS web
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

FROM base AS worker
CMD ["celery", "-A", "app.celery.app", "worker", "--loglevel=info"]

FROM base AS beat
CMD ["celery", "-A", "app.celery.app", "beat", "--loglevel=info"]
