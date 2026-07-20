#!/usr/bin/env bash
set -u
fail=0
check(){ printf '%-38s' "$1"; shift; if "$@" >/dev/null 2>&1; then echo OK; else echo FAIL; fail=1; fi; }
echo "=== SSH Validation ==="
check "SSH enabled" systemctl is-enabled --quiet ssh
check "SSH active" systemctl is-active --quiet ssh
check "Host keys exist" bash -c 'compgen -G "/etc/ssh/ssh_host_*_key" >/dev/null'
check "Port 22 listening" bash -c "ss -ltn | grep -qE '[:.]22[[:space:]]'"
((fail==0)) && echo "SSH validation PASSED" || echo "SSH validation FAILED"
exit "$fail"
