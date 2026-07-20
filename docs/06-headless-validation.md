# 06 — Headless Cold-Boot Validation

## Objective

Validate the complete lifecycle after monitor and keyboard removal and full power interruption.

This is the release gate for milestone M1.

## Prerequisites

- SSH validated
- Tailscale validated
- GNOME Remote Desktop configured in system mode
- RDP login already tested

## Procedure

Record the current state:

```bash
systemctl is-active ssh
systemctl is-active tailscaled
systemctl is-active gnome-remote-desktop.service
sudo grdctl --system status
tailscale ip -4
```

Shut down:

```bash
sudo poweroff
```

Then:

1. Wait until shutdown is complete.
2. Disconnect monitor, keyboard and mouse.
3. Remove power completely.
4. Wait several seconds.
5. Restore power and start the Jetson.
6. Do not reconnect local peripherals.
7. Wait for boot, network and services.

From the administration computer:

```bash
ping TAILSCALE_IP
ssh USER@TAILSCALE_IP 'hostname; uptime'
nc -zv TAILSCALE_IP 3389
```

Finally, connect with the RDP client and log in.

## Expected Behavior

Services appear in stages:

```text
Firmware
Linux
Network
SSH
Tailscale
GNOME Remote Desktop
RDP login
```

The machine may not answer immediately.

Validate client and server separately:

1. Ping
2. SSH
3. TCP/3389
4. RDP protocol login

A client crash does not prove a server failure.

## Validation

| Test | Required result |
|---|---|
| Boot without monitor | Pass |
| Boot without keyboard | Pass |
| Boot without mouse | Pass |
| Tailscale reconnect | Pass |
| Ping | Pass |
| SSH login | Pass |
| TCP/3389 | Pass |
| RDP login | Pass |
| Desktop usable | Pass |
| No local autologin | Pass |
| Full power removal survived | Pass |

Validated reference result: **all tests passed**.

## Milestone

When every row passes:

> M1 — Reproducible Headless Jetson Base
