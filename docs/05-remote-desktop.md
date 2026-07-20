# 05 — GNOME Remote Desktop System Mode

## Objective

Enable graphical remote access without local autologin and without an existing user desktop session.

## Design decision

Use:

```bash
grdctl --system
```

System mode is required because the Jetson is an edge appliance:

- no permanently logged-in desktop
- no local autologin
- no monitor dependency
- service managed by systemd
- remote GNOME login path

## Prerequisites

- Ubuntu desktop installed
- SSH and Tailscale validated
- `gnome-remote-desktop` installed
- RDP client available

## Commands

### 1. Verify package and service

```bash
dpkg -l | grep gnome-remote-desktop
systemctl status gnome-remote-desktop.service --no-pager
getent passwd gnome-remote-desktop
sudo grdctl --system status
```

The service account home is expected at:

```text
/var/lib/gnome-remote-desktop
```

### 2. Create TLS storage

```bash
sudo install -d   -o gnome-remote-desktop   -g gnome-remote-desktop   -m 0700   /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop
```

### 3. Generate TLS key and certificate with OpenSSL

`winpr-makecert` was not installed by default. OpenSSL worked successfully.

```bash
sudo openssl req   -x509   -newkey rsa:3072   -sha256   -days 3650   -nodes   -subj "/CN=jetson-lpr"   -keyout /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.key   -out /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.crt
```

```bash
sudo chown gnome-remote-desktop:gnome-remote-desktop   /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.key   /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.crt

sudo chmod 0600 /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.key
sudo chmod 0644 /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.crt
```

### 4. Register TLS material

```bash
sudo grdctl --system rdp set-tls-key   /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.key

sudo grdctl --system rdp set-tls-cert   /var/lib/gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.crt
```

### 5. Store RDP credentials

```bash
sudo grdctl --system rdp set-credentials
```

Enter credentials interactively. Do not place passwords in shell history.

### 6. Enable RDP and restart the service

```bash
sudo grdctl --system rdp enable
sudo systemctl enable gnome-remote-desktop.service
sudo systemctl restart gnome-remote-desktop.service
```

The restart is part of the normal sequence. Port 3389 initially refused connections until the service was restarted after configuration.

### 7. Inspect final state

```bash
sudo grdctl --system status
systemctl status gnome-remote-desktop.service --no-pager
ss -ltnp | grep ':3389'
```

## Expected Behavior

The journal may contain:

```text
Init TPM credentials failed
using GKeyFile as fallback
```

On the validated JetPack 7.2 platform, RDP worked correctly with this fallback.

An RDP client may warn about the self-signed certificate. Verify the target before accepting it.

A one-time ThinCast crash was observed before a later successful connection. Ping, SSH, TCP/3389 and subsequent RDP login all worked, so this was classified as client-side instability.

## Validation

On the Jetson:

```bash
sudo grdctl --system status
systemctl is-enabled gnome-remote-desktop.service
systemctl is-active gnome-remote-desktop.service
ss -ltn | grep ':3389'
```

From the administration computer:

```bash
nc -zv TAILSCALE_IP 3389
```

Then connect the RDP client to:

```text
TAILSCALE_IP:3389
```

Success criteria:

- service active
- RDP enabled
- TLS certificate and key registered
- credentials configured
- port 3389 reachable
- GNOME login displayed
- login succeeds
- desktop usable
- no local autologin required

## Next Stage

Continue with [06 — Headless Validation](06-headless-validation.md).
