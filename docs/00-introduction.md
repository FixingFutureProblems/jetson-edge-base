# 00 — Introduction

## Objective

Build a Jetson base platform that can be administered remotely after a cold boot without a connected monitor, keyboard or mouse.

## Target state

- Ubuntu starts from NVMe.
- SSH starts automatically.
- Tailscale reconnects automatically.
- GNOME Remote Desktop runs in system mode.
- RDP does not require an existing local desktop session.
- Local autologin is disabled.
- The platform remains reachable after full power removal.

## Administration model

SSH is the primary administration path. RDP is optional graphical access. Both are reached through Tailscale rather than exposed directly to the public Internet.

## Validation model

A configuration statement is considered proven only after a command or end-to-end test verifies it.

Examples:

```bash
systemctl is-active ssh
tailscale status
nc -zv HOST 3389
```

A successful RDP login is the final proof of the graphical path.

## Prerequisites

- Jetson Orin Nano Developer Kit
- NVMe SSD
- Stable power
- Temporary monitor and keyboard
- Internet access
- Second computer for remote testing
- Tailscale account
- RDP client

## Expected Behavior

Initial firmware, installer and first-boot stages may require local peripherals. After Stage 06, remove them and perform the cold-boot validation.

## Validation

Confirm the intended operating model:

```text
Primary administration: SSH
Remote network: Tailscale
Optional desktop: GNOME Remote Desktop system mode
Autologin: disabled
Headless cold boot: required
```

## Next Stage

Continue with [01 — Installation](01-installation.md).
