# Troubleshooting

## SSH is inactive

### Symptoms

```text
systemctl is-active ssh
inactive
```

### Cause

OpenSSH server is not enabled or host keys are missing.

### Solution

```bash
sudo ssh-keygen -A
sudo systemctl enable --now ssh
```

### Validation

```bash
systemctl is-active ssh
ss -ltn | grep ':22'
```

---

## SSH host identity changed

### Cause

The Jetson was reflashed or host keys were regenerated.

### Solution

For a known reinstalled host:

```bash
ssh-keygen -R HOST
```

Reconnect and verify the fingerprint.

---

## Tailscale shows `NeedsLogin`

### Solution

```bash
sudo tailscale up
```

### Validation

```bash
tailscale status
tailscale ip -4
```

---

## RDP port 3389 refuses connections

### Cause

The service has not loaded the latest system-mode configuration.

### Solution

```bash
sudo systemctl restart gnome-remote-desktop.service
```

### Validation

```bash
systemctl is-active gnome-remote-desktop.service
ss -ltn | grep ':3389'
nc -zv HOST 3389
```

---

## RDP service is active but login fails

Reset credentials:

```bash
sudo grdctl --system rdp set-credentials
sudo systemctl restart gnome-remote-desktop.service
```

Then inspect:

```bash
sudo grdctl --system status
```

---

## RDP client crashes

Check the server independently:

```bash
ping HOST
ssh USER@HOST
nc -zv HOST 3389
```

Try a second RDP client. A successful second client confirms that the Jetson service is operational.
