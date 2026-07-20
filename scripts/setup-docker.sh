#!/usr/bin/env bash
# Install Docker Engine (apt) and remove broken Snap Docker if present.
# Run once: sudo ./scripts/setup-docker.sh

set -Eeuo pipefail

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "Run with sudo: sudo ./scripts/setup-docker.sh"
    exit 1
fi

REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

echo "== Removing Snap Docker (if installed) =="
if snap list docker >/dev/null 2>&1; then
    snap stop docker || true
    snap remove docker || true
fi

echo "== Installing Docker Engine =="
apt-get update -qq
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings

if [[ ! -f /etc/apt/keyrings/docker.asc ]]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
fi

if [[ ! -f /etc/apt/sources.list.d/docker.list ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" \
        > /etc/apt/sources.list.d/docker.list
fi

apt-get update -qq
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable --now docker
usermod -aG docker "$REAL_USER"

echo
echo "Docker installed. Verify (may need new login or: newgrp docker):"
echo "  docker info"
echo "  docker compose version"
echo
echo "Then from project root:"
echo "  cd $(dirname "$(dirname "$(readlink -f "$0")")")"
echo "  ./run.sh"
