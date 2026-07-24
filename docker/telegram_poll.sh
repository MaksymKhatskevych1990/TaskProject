#!/bin/sh
set -e

if [ "${TELEGRAM_ENABLED:-False}" = "True" ] || [ "${TELEGRAM_ENABLED:-False}" = "true" ]; then
    echo "Starting Telegram long polling..."
    exec python manage.py telegram_poll
fi

echo "Telegram polling is disabled (TELEGRAM_ENABLED=False)."
exec sleep infinity
