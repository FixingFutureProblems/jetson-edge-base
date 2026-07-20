# 02 — System Update

## Objective

Bring the base operating system to a consistent package state before remote services are configured.

## Prerequisites

- First boot completed
- Internet access
- Working `sudo`

## Commands

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt autoremove --purge -y
sudo reboot
```

After reboot:

```bash
systemctl --failed
uname -a
```

## Expected Behavior

Package configuration can remain visually quiet for several minutes. Kernel, firmware, GNOME and NVIDIA packages can take longer than normal application packages.

Do not interrupt `apt` while package management is active.

## Validation

```bash
sudo apt update
systemctl --failed
```

Success criteria:

- No repository errors.
- No unexpected failed services.
- Reboot succeeds.

## Next Stage

Continue with [03 — SSH](03-ssh.md).
