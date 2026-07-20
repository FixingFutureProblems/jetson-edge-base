# 03 — SSH

## Objective

Enable reliable command-line administration.

## Prerequisites

- Updated system
- Network connection
- Administrative user

## Commands

```bash
sudo apt install -y openssh-server
sudo ssh-keygen -A
sudo systemctl enable --now ssh
systemctl status ssh --no-pager
ss -ltnp | grep ':22'
hostname -I
```

From the administration computer:

```bash
ssh USER@JETSON_IP
```

## Expected Behavior

After reflashing, the SSH host key changes. The client may report:

```text
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
```

For a known reinstalled Jetson:

```bash
ssh-keygen -R JETSON_IP
```

Reconnect and verify the new fingerprint. Do not disable host-key checking globally.

Generating host keys with `ssh-keygen -A` before enabling the service prevents startup failures caused by missing keys.

## Validation

On the Jetson:

```bash
systemctl is-enabled ssh
systemctl is-active ssh
ss -ltn | grep ':22'
```

From the administration computer:

```bash
ssh USER@JETSON_IP 'hostname && uptime'
```

Required result:

```text
enabled
active
```

and a successful remote command.

## Next Stage

Continue with [04 — Tailscale](04-tailscale.md).
