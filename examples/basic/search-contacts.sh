#!/usr/bin/env bash
# Search contacts by name — handles typos, accents, and name inversions.
#
# Usage: ./search-contacts.sh
# Prerequisites: pip install insim-cli && insim login

# Smart search (fuzzy matching, accent-insensitive)
insim contacts search "Marie Dupont"

# JSON output for scripts and AI agents
insim --json contacts search "Marie Dupont"

# List contacts with keyword filter
insim contacts list --search "dupont" --limit 10

# Find a contact by phone number
insim contacts find-phone "+33600000000"
