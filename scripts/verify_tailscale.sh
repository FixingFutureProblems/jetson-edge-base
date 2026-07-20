#!/usr/bin/env bash
set -u
fail=0
check(){ printf '%-38s' "$1"; shift; if "$@" >/dev/null 2>&1; then echo OK; else echo FAIL; fail=1; fi; }
echo "=== Tailscale Validation ==="
check "tailscaled enabled" systemctl is-enabled --quiet tailscaled
check "tailscaled active" systemctl is-active --quiet tailscaled
check "tailscale available" command -v tailscale
check "IPv4 assigned" bash -c 'tailscale ip -4 | grep -q "^100\."'
((fail==0)) && echo "Tailscale validation PASSED" || echo "Tailscale validation FAILED"
exit "$fail"
