#!/usr/bin/env bash
# Create and launch an SMS campaign to a contact list.
#
# Usage: ./create-campaign.sh
# Prerequisites: pip install insim-cli && insim login
#
# WARNING: campaigns start sends real SMS to all recipients.
# Always verify the campaign details before launching.

# Step 1: Create a contact list
LIST_ID=$(insim --json lists create "Summer Sale Contacts" | python3 -c "import sys,json; print(json.load(sys.stdin).get('list',{}).get('_id',''))")
echo "Created list: $LIST_ID"

# Step 2: Add all contacts to the list
insim lists add-all "$LIST_ID"

# Step 3: Create the campaign
CAMPAIGN_ID=$(insim --json campaigns create \
  --name "Summer Sale 2026" \
  --message "Hi! Enjoy 20% off all products this week. Reply STOP to unsubscribe." \
  --list "$LIST_ID" | python3 -c "import sys,json; print(json.load(sys.stdin).get('campaign',{}).get('_id',''))")
echo "Created campaign: $CAMPAIGN_ID"

# Step 4: Verify before launch
insim campaigns detail "$CAMPAIGN_ID"

# Step 5: Launch (uncomment when ready — this sends real SMS!)
# insim campaigns start "$CAMPAIGN_ID" --confirm
