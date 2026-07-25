#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is required but was not found."
    echo "Install: sudo ./scripts/setup-docker.sh"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "Docker daemon is not running or not reachable."
    echo "Fix: sudo systemctl start docker"
    echo "Or install Engine: sudo ./scripts/setup-docker.sh"
    docker info 2>&1 | head -5 || true
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "Docker Compose v2 is required but was not found."
    echo "Install plugin: sudo apt-get install -y docker-compose-plugin"
    echo "Or: sudo ./scripts/setup-docker.sh"
    exit 1
fi

if [[ ! -f .env ]]; then
    cp .env.example .env
    echo "Created .env from .env.example."
    echo "Change the development credentials before using this configuration elsewhere."
fi

echo "Building application images..."
docker compose build

echo "Starting PostgreSQL, Redis, and MinIO..."
docker compose up -d postgres redis minio

echo "Creating the MinIO bucket..."
docker compose run --rm minio_setup

echo "Applying database migrations..."
docker compose run --rm --no-deps backend python manage.py migrate --noinput

echo "Registering Celery Beat schedules..."
docker compose run --rm --no-deps backend python manage.py setup_beat_schedule

echo "Collecting static assets..."
docker compose run --rm --no-deps backend python manage.py collectstatic --noinput

echo "Starting the complete stack..."
docker compose up -d

echo "Reloading Nginx after backend startup..."
docker compose restart nginx >/dev/null
sleep 3

HTTP_PORT="${HTTP_PORT:-8080}"
if [[ -f .env ]]; then
    env_http_port="$(grep -E '^HTTP_PORT=' .env | tail -1 | cut -d= -f2- | tr -d '\r' || true)"
    if [[ -n "${env_http_port}" ]]; then
        HTTP_PORT="${env_http_port}"
    fi
fi

echo "Waiting for the HTTP endpoint..."
for attempt in {1..60}; do
    if curl -sf "http://127.0.0.1:${HTTP_PORT}/api/health/" >/dev/null 2>&1; then
        docker compose ps
        HTTP_ADDRESS="$(docker compose port nginx 80)"
        FLOWER_ADDRESS="$(docker compose port flower 5555)"
        MINIO_ADDRESS="$(docker compose port minio 9001)"
        echo
        echo "Studio is ready: http://localhost:${HTTP_ADDRESS##*:}"
        echo "Landing page:   http://localhost:${HTTP_ADDRESS##*:}/"
        echo "Admin:          http://localhost:${HTTP_ADDRESS##*:}/admin/"
        echo "Flower:         http://localhost:${FLOWER_ADDRESS##*:}"
        echo "MinIO console:  http://localhost:${MINIO_ADDRESS##*:}"
        echo "Telegram bot:   docker compose logs -f telegram_bot"
        exit 0
    fi
    sleep 2
done

echo "The stack did not become healthy in time."
docker compose ps
docker compose logs --tail=100 backend nginx
exit 1
