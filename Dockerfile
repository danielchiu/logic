FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p db

EXPOSE 8000

# NOTE: default SQLite backend is not safe under concurrent writers. The app's
# refresh() pattern (delete + re-insert) can race across processes, so we run a
# single worker by default. Override WEB_CONCURRENCY when using a real database
# (e.g. Postgres via DATABASE_URL).
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 logic:application --workers ${WEB_CONCURRENCY:-1}"]
