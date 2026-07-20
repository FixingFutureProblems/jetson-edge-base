# jetson-edge-base

> A reproducible, scriptable and verifiable reference platform for NVIDIA Jetson development.

This repository documents a complete NVIDIA Jetson setup from firmware and JetPack installation to a remotely administered, headless base platform. Every stage contains commands, expected behavior and explicit validation. A stage is complete only after validation succeeds.

## Validated reference platform

- NVIDIA Jetson Orin Nano Developer Kit
- JetPack 7.2
- Ubuntu 24.04
- NVMe system storage
- Wi-Fi
- macOS administration host

## Principles

- Documentation First
- Validation First
- CLI First
- Reproducibility First
- Scriptable
- Verifiable
- Prefer NVIDIA, Ubuntu and GNOME defaults
- Deviate only for a documented technical reason

## Milestone M1 — Reproducible Headless Jetson Base

**Status: validated**

The following sequence passed after complete power removal:

1. Monitor, keyboard and mouse disconnected.
2. Jetson powered on.
3. Tailscale reconnected automatically.
4. Ping succeeded.
5. SSH login succeeded.
6. TCP port 3389 was reachable.
7. GNOME Remote Desktop presented a login.
8. Desktop login succeeded without local autologin.

| Test | Result |
|---|---:|
| Boot without monitor | Passed |
| Boot without keyboard | Passed |
| SSH | Passed |
| Tailscale reconnect | Passed |
| GNOME Remote Desktop system mode | Passed |
| RDP over Tailscale | Passed |
| Cold boot after full power removal | Passed |

## Stage order

1. [Introduction](docs/00-introduction.md)
2. [Firmware, JetPack and first boot](docs/01-installation.md)
3. [System update](docs/02-system-update.md)
4. [SSH](docs/03-ssh.md)
5. [Tailscale](docs/04-tailscale.md)
6. [GNOME Remote Desktop](docs/05-remote-desktop.md)
7. [Headless validation](docs/06-headless-validation.md)

Supporting documents:

- [Expected behavior](docs/expected-behavior.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Architecture decisions](docs/architecture-decisions.md)

## Documentation contract

Every stage follows:

1. Objective
2. Prerequisites
3. Commands
4. Expected Behavior
5. Validation
6. Next Stage

Troubleshooting is separate from normal behavior.

## Scripts

```bash
./scripts/verify_ssh.sh
./scripts/verify_tailscale.sh
./scripts/verify_rdp.sh
./scripts/verify_system.sh
```

The verification scripts are read-only.

## Scope

Developer tooling intentionally follows infrastructure validation. Later stages will cover Git, Python, Docker, CUDA, Basler cameras, YOLO and the LPR pipeline.

## License

MIT.
