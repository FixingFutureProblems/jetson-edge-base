# 01 — Firmware, JetPack and First Boot

## Objective

Install the selected JetPack release to NVMe and complete the first Ubuntu boot.

## Prerequisites

- Jetson assembled
- NVMe installed
- Installer media prepared
- Monitor and keyboard connected
- Stable power
- Network available

## Installation

Use the NVIDIA installer for the selected JetPack release and choose the NVMe device as the system target.

Validated reference:

```text
JetPack 7.2
Ubuntu 24.04
NVMe target
```

After installation, verify the root filesystem:

```bash
findmnt /
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
cat /etc/os-release
cat /etc/nv_tegra_release
```

Set a stable hostname if required:

```bash
sudo hostnamectl set-hostname jetson-lpr
```

Verify time configuration:

```bash
timedatectl
```

## Expected Behavior

The first boot can look stalled. Observed normal behavior includes:

- black screen
- blinking cursor
- long pause before GNOME appears
- delayed display initialization

Do not interrupt power merely because no progress indicator is visible. The black screen that causes the anxious wait may disappear only after several minutes.

A display-port reconnect or port change can help when the installer is running but the display handshake failed.

Do not enable autologin as a remote-desktop workaround.

## Validation

```bash
findmnt /
cat /etc/os-release
cat /etc/nv_tegra_release
hostnamectl
timedatectl
```

Success criteria:

- Root filesystem is on the intended NVMe installation.
- Ubuntu reports 24.04.
- NVIDIA Tegra release metadata exists.
- Hostname and timezone are correct.
- The system survives a reboot.

```bash
sudo reboot
```

## Next Stage

Continue with [02 — System Update](02-system-update.md).
