#!/usr/bin/env bash
# Morning prospecting routine — check missed calls and unread SMS.
# Run this at the start of your day to know who to call back.
#
# Usage: crontab -e → 0 8 * * 1-5 /path/to/morning-prospecting-list.sh
# Prerequisites: INSIM_LOGIN and INSIM_ACCESS_KEY env vars set

set -euo pipefail

echo "=== Morning Prospecting Report ==="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

echo "--- Missed calls (last 24h) ---"
insim calls list --type missed --limit 20

echo ""
echo "--- Unread incoming SMS (last 10) ---"
insim sms list --direction inbound --limit 10

echo ""
echo "--- Account credits ---"
insim account info

echo ""
echo "=== End of report ==="
