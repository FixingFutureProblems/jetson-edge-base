#!/usr/bin/env bash
set -u
dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
fail=0
for s in verify_ssh.sh verify_tailscale.sh verify_rdp.sh; do
  "$dir/$s" || fail=1
  echo
done
((fail==0)) && echo "SYSTEM VALIDATION PASSED" || echo "SYSTEM VALIDATION FAILED"
exit "$fail"
