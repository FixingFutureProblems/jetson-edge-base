# Expected Behavior

Normal conditions that can look like failures:

## Black screen and blinking cursor

During installation or first boot, the display can remain black with a blinking cursor for several minutes. Wait. Do not interrupt power solely because no progress bar is visible.

## SSH host-key warning

After reinstalling the Jetson, remove the known obsolete host key:

```bash
ssh-keygen -R HOST
```

Then verify the new fingerprint.

## Tailscale `NeedsLogin`

The daemon is running, but authentication is incomplete. Run:

```bash
sudo tailscale up
```

## Delayed Tailscale reconnect

The node can appear online after the local network and SSH stack.

## TPM fallback

GNOME Remote Desktop may fail TPM initialization and use GKeyFile storage. On the validated platform this did not prevent successful RDP login.

## Port 3389 unavailable after configuration

Restart the service:

```bash
sudo systemctl restart gnome-remote-desktop.service
```

Then validate again.

## Self-signed RDP certificate

Certificate warnings are expected. Verify the destination before accepting.

## Client instability

A one-time ThinCast crash was followed by a successful connection. Separate client behavior from the Jetson by testing ping, SSH and TCP/3389.
