# Architecture Decisions

## SSH is primary

SSH is scriptable, independent of GNOME and suitable for all routine administration.

## Tailscale is the private network path

SSH and RDP do not need direct public exposure.

## GNOME Remote Desktop uses system mode

Accepted command family:

```bash
grdctl --system
```

Reason: no autologin, no existing user session and no monitor dependency.

## OpenSSL generates TLS material

`winpr-makecert` was not present by default. OpenSSL was available and produced a working key and certificate.

## Service restart is mandatory after RDP changes

The reference setup did not listen reliably on port 3389 until:

```bash
sudo systemctl restart gnome-remote-desktop.service
```

## Expected behavior is separate from troubleshooting

Normal but alarming conditions must not be presented as faults.

## Developer tooling follows infrastructure

Git, Python, Docker, CUDA, Basler and LPR work starts only after the headless cold-boot test passes.
