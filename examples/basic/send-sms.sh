#!/usr/bin/env bash
# Send an SMS from your real mobile number.
#
# Usage: ./send-sms.sh
# Prerequisites: pip install insim-cli && insim login

# Send a simple SMS
insim sms send "+33600000000" "Hello from insim-cli!"

# Send with a tracked link (clicks appear in insim stats clicks)
insim sms send "+33600000000" "Check our new offer: [link]" --url "https://example.com/promo"
