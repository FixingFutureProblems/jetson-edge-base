#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }
dir=/var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop
key=$dir/tls.key
crt=$dir/tls.crt
cn=${RDP_CERT_CN:-$(hostname)}
install -d -o gnome-remote-desktop -g gnome-remote-desktop -m 0700 "$dir"
if [[ ! -s $key || ! -s $crt ]]; then
  openssl req -x509 -newkey rsa:3072 -sha256 -days 3650 -nodes     -subj "/CN=$cn" -keyout "$key" -out "$crt"
fi
chown gnome-remote-desktop:gnome-remote-desktop "$key" "$crt"
chmod 0600 "$key"
chmod 0644 "$crt"
grdctl --system rdp set-tls-key "$key"
grdctl --system rdp set-tls-cert "$crt"
echo "Enter RDP credentials:"
grdctl --system rdp set-credentials
grdctl --system rdp enable
systemctl enable gnome-remote-desktop.service
systemctl restart gnome-remote-desktop.service
grdctl --system status
