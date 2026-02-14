#!/bin/bash
set -e

# Detectar comando Python disponível
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "Error: Neither python nor python3 found!"
    exit 1
fi

USER="$(id -u)"

[ -z ${POSTGRES_HOST+x} ] && export POSTGRES_HOST=postgres
[ -z ${DEBUG+x} ] && export DEBUG=false

wait_for_db() {
    echo "Waiting for postgres..."

    while ! nc -z "$POSTGRES_HOST" 5432; do
        sleep 2
    done

    echo "PostgreSQL started"
}

if [[ "$1" == "start" ]]; then

    wait_for_db

    $PYTHON_CMD manage.py migrate
    exec $PYTHON_CMD manage.py runserver 0.0.0.0:8000

else
    # Custom
    exec "$@"
fi
