#!/usr/bin/env bash
# Weekly campaign report — show stats for all campaigns.
# Run every Monday morning to review last week's performance.
#
# Usage: crontab -e → 0 9 * * 1 /path/to/weekly-campaign-report.sh
# Prerequisites: INSIM_LOGIN and INSIM_ACCESS_KEY env vars set

set -euo pipefail

echo "=== Weekly Campaign Report ==="
echo "Week ending: $(date '+%Y-%m-%d')"
echo ""

echo "--- Overall Stats ---"
insim stats overview

echo ""
echo "--- Link Clicks (last 20) ---"
insim stats clicks --limit 20

echo ""
echo "--- Active Campaigns ---"
insim campaigns list

echo ""
echo "=== End of report ==="
