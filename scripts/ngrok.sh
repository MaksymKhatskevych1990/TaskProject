#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

HTTP_PORT="${HTTP_PORT:-8080}"
NGROK_DOMAIN="${NGROK_DOMAIN:-}"
if [[ -f .env ]]; then
    env_http_port="$(grep -E '^HTTP_PORT=' .env | tail -1 | cut -d= -f2- | tr -d '\r' || true)"
    env_ngrok_domain="$(grep -E '^NGROK_DOMAIN=' .env | tail -1 | cut -d= -f2- | tr -d '\r' || true)"
    if [[ -n "${env_http_port}" ]]; then
        HTTP_PORT="${env_http_port}"
    fi
    if [[ -n "${env_ngrok_domain}" ]]; then
        NGROK_DOMAIN="${env_ngrok_domain}"
    fi
fi

if ! command -v ngrok >/dev/null 2>&1; then
    echo "ngrok is not installed."
    echo "Install: https://ngrok.com/download"
    echo "Then authenticate once: ngrok config add-authtoken <token>"
    echo "Free token: https://dashboard.ngrok.com/get-started/your-authtoken"
    exit 1
fi

if ! ngrok config check >/dev/null 2>&1; then
    echo "ngrok is not authenticated."
    echo "Create a free account: https://dashboard.ngrok.com/signup"
    echo "Then run: ngrok config add-authtoken <token>"
    exit 1
fi

if ! curl -sf "http://127.0.0.1:${HTTP_PORT}/api/health/" >/dev/null 2>&1; then
    echo "Studio is not reachable at http://127.0.0.1:${HTTP_PORT}."
    echo "Start it first: ./run.sh"
    exit 1
fi

if curl -sf "http://127.0.0.1:4040/api/tunnels" >/dev/null 2>&1; then
    echo "An ngrok agent is already running on port 4040."
    existing_url="$(
        curl -sf "http://127.0.0.1:4040/api/tunnels" \
            | python3 -c 'import json,sys; d=json.load(sys.stdin); urls=[t.get("public_url","") for t in d.get("tunnels",[]) if str(t.get("public_url","")).startswith("https://")]; print(urls[0] if urls else "")' \
            2>/dev/null || true
    )"
    if [[ -n "${existing_url}" ]]; then
        echo
        echo "Public URL:     ${existing_url}"
        echo "Landing page:   ${existing_url}/"
        echo "Admin:          ${existing_url}/admin/"
        echo "Inspector:      http://127.0.0.1:4040"
    else
        echo "Open http://127.0.0.1:4040 for the current public URL."
    fi
    exit 1
fi

ngrok_args=(http "${HTTP_PORT}" --log=stdout)
if [[ -n "${NGROK_DOMAIN}" ]]; then
    ngrok_args+=(--url="${NGROK_DOMAIN}")
fi

echo "Opening a public HTTPS tunnel to http://127.0.0.1:${HTTP_PORT} ..."
echo "Keep this terminal open while you test on your phone."
echo

ngrok "${ngrok_args[@]}" >/tmp/studio-ngrok.log 2>&1 &
ngrok_pid=$!

cleanup() {
    if kill -0 "${ngrok_pid}" >/dev/null 2>&1; then
        kill "${ngrok_pid}" >/dev/null 2>&1 || true
        wait "${ngrok_pid}" 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM

public_url=""
for _ in $(seq 1 30); do
    if ! kill -0 "${ngrok_pid}" >/dev/null 2>&1; then
        echo "ngrok exited before the tunnel was ready."
        tail -n 40 /tmp/studio-ngrok.log || true
        exit 1
    fi
    public_url="$(
        curl -sf "http://127.0.0.1:4040/api/tunnels" \
            | python3 -c 'import json,sys; d=json.load(sys.stdin); urls=[t.get("public_url","") for t in d.get("tunnels",[]) if str(t.get("public_url","")).startswith("https://")]; print(urls[0] if urls else "")' \
            2>/dev/null || true
    )"
    if [[ -n "${public_url}" ]]; then
        break
    fi
    sleep 0.5
done

if [[ -z "${public_url}" ]]; then
    echo "Timed out waiting for the ngrok public URL."
    echo "Check the inspector: http://127.0.0.1:4040"
    tail -n 40 /tmp/studio-ngrok.log || true
    exit 1
fi

echo "Studio is ready over ngrok:"
echo "Public URL:     ${public_url}"
echo "Landing page:   ${public_url}/"
echo "Admin:          ${public_url}/admin/"
echo "Health:         ${public_url}/api/health/"
echo "Inspector:      http://127.0.0.1:4040"
echo
echo "On free ngrok, tap Visit Site once if the warning page appears."
echo "Press Ctrl+C to stop the tunnel."

wait "${ngrok_pid}"
