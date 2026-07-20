# 04 — Tailscale

## Objective

Provide a private remote path for SSH and RDP without public port exposure.

## Prerequisites

- SSH validated
- Internet access
- Tailscale account

## Commands

Install Tailscale using the Ubuntu 24.04 package method, then run:

```bash
sudo systemctl enable --now tailscaled
sudo tailscale up
tailscale status
tailscale ip -4
```

## Expected Behavior

`NeedsLogin` is a normal intermediate state: the daemon is running, but device authentication is incomplete.

After boot, networking and Tailscale may need a short time before the node becomes reachable.

Do not hard-code a particular Tailscale address in reusable scripts.

## Validation

On the Jetson:

```bash
systemctl is-enabled tailscaled
systemctl is-active tailscaled
tailscale status
tailscale ip -4
```

From another tailnet device:

```bash
ping TAILSCALE_IP
ssh USER@TAILSCALE_IP
```

Success criteria:

- `tailscaled` is enabled and active.
- Node is online.
- SSH succeeds through the Tailscale address.

## Next Stage

Continue with [05 — GNOME Remote Desktop](05-remote-desktop.md).
