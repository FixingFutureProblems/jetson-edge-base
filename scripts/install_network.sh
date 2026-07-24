#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

if [[ "${EUID}" -ne 0 ]]; then
    echo "Bitte mit sudo ausführen:"
    echo "  sudo ./scripts/install_network.sh"
    exit 1
fi

install -d -m 0755 /etc/jetson-edge
install -m 0644 \
    "$REPOSITORY_DIR/config/network.conf" \
    /etc/jetson-edge/network.conf

install -m 0755 \
    "$REPOSITORY_DIR/scripts/jetson-network" \
    /usr/local/sbin/jetson-network

echo
echo "Netzwerkmodul installiert."
echo
echo "Konfiguration:"
echo "  /etc/jetson-edge/network.conf"
echo
echo "Programm:"
echo "  /usr/local/sbin/jetson-network"
echo
echo "Status prüfen mit:"
echo "  jetson-network status"
