#!/usr/bin/env bash
set -u
fail=0
check(){ printf '%-38s' "$1"; shift; if "$@" >/dev/null 2>&1; then echo OK; else echo FAIL; fail=1; fi; }
echo "=== GNOME Remote Desktop Validation ==="
check "grdctl available" command -v grdctl
check "RDP service enabled" systemctl is-enabled --quiet gnome-remote-desktop.service
check "RDP service active" systemctl is-active --quiet gnome-remote-desktop.service
check "Port 3389 listening" bash -c "ss -ltn | grep -qE '[:.]3389[[:space:]]'"
echo "Manual check: sudo grdctl --system status"
((fail==0)) && echo "RDP validation PASSED" || echo "RDP validation FAILED"
exit "$fail"
