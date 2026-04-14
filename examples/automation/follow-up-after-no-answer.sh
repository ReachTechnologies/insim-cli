#!/usr/bin/env bash
# Automatically send a follow-up SMS to contacts who missed your call.
#
# Workflow:
#   1. Fetch missed outgoing calls (you called, they didn't pick up)
#   2. Send a follow-up SMS to each missed contact
#
# Usage: ./follow-up-after-no-answer.sh
# Prerequisites: INSIM_LOGIN and INSIM_ACCESS_KEY env vars set

set -euo pipefail

MESSAGE="Hi, I tried to reach you earlier but couldn't get through. When would be a good time to call back?"

echo "Fetching recent missed outgoing calls..."
PHONES=$(insim --json calls list --type missed --limit 10 \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
calls = data.get('calls', [])
seen = set()
for c in calls:
    phone = c.get('phone_number', '')
    if phone and phone not in seen:
        seen.add(phone)
        print(phone)
")

if [ -z "$PHONES" ]; then
  echo "No missed calls found. Nothing to follow up."
  exit 0
fi

echo "Sending follow-up SMS..."
while IFS= read -r phone; do
  echo "  -> $phone"
  insim sms send "$phone" "$MESSAGE"
done <<< "$PHONES"

echo "Done. Follow-up SMS sent."
