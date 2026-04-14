#!/usr/bin/env bash
# Browse your call log — filter by type, phone number, or date.
#
# Usage: ./list-calls.sh
# Prerequisites: pip install insim-cli && insim login

# List recent calls
insim calls list --limit 10

# Filter by type: incoming, outgoing, missed
insim calls list --type missed --limit 10
insim calls list --type outgoing --limit 5

# Filter by phone number
insim calls list --phone "+33600000000" --limit 10

# JSON output for parsing
insim --json calls list --limit 5
