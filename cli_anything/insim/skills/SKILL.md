---
name: insim-cli
description: >-
  Command-line interface for inSIM — manage SMS, contacts, calls, campaigns, and qualifications.
  Built for AI agents and humans. Supports JSON output for automation.
---

# insim-cli

Control **inSIM** from the command line: send SMS, manage contacts, launch campaigns, qualify calls, and track statistics. Designed for **AI agents** (Claude, GPT, Gemini, Mistral, Llama) and **humans** alike.

## Installation

```bash
pip install insim-cli
```

## Authentication

```bash
# Login (saves credentials to ~/.insim/credentials.json)
insim login user@email.com --key YOUR_ACCESS_KEY

# Or use environment variables (preferred for AI agents)
export INSIM_LOGIN="user@email.com"
export INSIM_ACCESS_KEY="your_access_key"

# Check who you are
insim whoami
```

## JSON Output (for AI agents)

Add `--json` to ANY command for machine-readable JSON output:

```bash
insim --json contacts search "john"
insim --json sms list --limit 5
insim --json account info
```

**AI agents should ALWAYS use `--json` to parse results reliably.**

## Command Reference

### Auth
| Command | Description |
|---------|-------------|
| `insim login EMAIL --key KEY` | Login and save credentials |
| `insim logout` | Remove saved credentials |
| `insim whoami` | Show account info |

### Contacts
| Command | Description |
|---------|-------------|
| `insim contacts list` | List contacts (--search, --limit, --cursor) |
| `insim contacts search NAME` | Smart search by name (handles typos, inversions) |
| `insim contacts find-phone PHONE` | Find contact by phone number |
| `insim contacts detail ID` | Full contact details |
| `insim contacts switch-pro ID --pro` | Share contact with team |
| `insim contacts switch-pro ID --perso` | Make contact private |
| `insim contacts delete ID` | Delete a contact (soft delete) |
| `insim contacts tags-add ID tag1 tag2` | Add tags to a contact |
| `insim contacts tags-remove ID tag1` | Remove tags from a contact |
| `insim contacts custom-fields` | List custom fields |

### SMS
| Command | Description |
|---------|-------------|
| `insim sms list` | List SMS (--direction, --phone, --from, --to, --limit) |
| `insim sms detail ID` | Full SMS details with click tracking |
| `insim sms conversation PHONE` | Conversation thread with a number |
| `insim sms send PHONE "message"` | Send an SMS |

### Calls
| Command | Description |
|---------|-------------|
| `insim calls list` | Call log (--type, --phone, --limit) |
| `insim calls qualify ID --option OPT_ID` | Qualify a call |
| `insim calls clictocall PHONE` | Initiate a call via connected device |

### Qualifications
| Command | Description |
|---------|-------------|
| `insim qualifications list` | List qualified calls |
| `insim qualifications options` | List qualification categories |
| `insim qualifications options-create LABEL` | Create a category |
| `insim qualifications options-update ID LABEL` | Rename a category |
| `insim qualifications options-delete ID` | Delete a category |
| `insim qualifications stats` | Qualification statistics |

### Account
| Command | Description |
|---------|-------------|
| `insim account info` | Account details, credits, options |
| `insim account webhooks-set --sms URL` | Configure webhook URLs |

### Lists
| Command | Description |
|---------|-------------|
| `insim lists list` | List all contact lists |
| `insim lists create NAME` | Create a new list |
| `insim lists detail ID` | List details with contacts |
| `insim lists update ID --name NEW` | Rename a list |
| `insim lists delete ID` | Delete a list |
| `insim lists add-contacts ID C1 C2` | Add contacts to list |
| `insim lists remove-contacts ID C1` | Remove contacts from list |
| `insim lists add-all ID` | Add ALL contacts to list |

### Campaigns
| Command | Description |
|---------|-------------|
| `insim campaigns list` | List campaigns |
| `insim campaigns create --name X --message Y` | Create a campaign |
| `insim campaigns detail ID` | Campaign details |
| `insim campaigns cancel ID` | Cancel a campaign |
| `insim campaigns start ID` | Launch a campaign (sends SMS!) |

### Templates
| Command | Description |
|---------|-------------|
| `insim templates list` | List message templates |
| `insim templates create --name X --message Y` | Create a template |
| `insim templates update ID --message Y` | Update a template |
| `insim templates delete ID` | Delete a template |
| `insim templates send ID --to PHONE` | Send SMS via template |

### Stats
| Command | Description |
|---------|-------------|
| `insim stats overview` | SMS, calls, clicks, contacts summary |
| `insim stats clicks` | Link click details |

---

## Workflows

### Workflow 1: Check your account and credits

**Context:** You need to verify how many SMS credits are left before sending.

```bash
insim account info
```

**Expected output:**
```
Account Info
  Login: user@email.com
  Plan: dedie
  SMS Credits: 3
  Country: TN
  Active: True
  Devices Connected: 0
```

**If credits are 0:** Tell the user they need to recharge before sending SMS.

---

### Workflow 2: Find a contact by name

**Context:** The user says "find John Doe" or "call cecile dubois". You need the phone number.

```bash
insim --json contacts search "cecile dubois"
```

**Expected output:**
```json
{
  "success": true,
  "contacts": [
    {"lastname": "Dubois", "firstname": "Cecile", "phone_number": "+33612345678", "score": 100, "match_type": "exact"}
  ]
}
```

**How it works:**
- The search handles name/firstname inversions automatically
- It handles accents: "cecile" finds "Cecile"
- It handles typos: "cecille" finds "Cecile" (fuzzy mode)
- Always take the result with the highest score
- If score < 30, ask the user for confirmation: "Did you mean...?"

**If no results:** Try with just the last name: `insim --json contacts search "dubois"`

---

### Workflow 3: Find a contact by phone number

**Context:** You have a phone number and need the contact info.

```bash
insim --json contacts find-phone "+33664456336"
```

Works with both international (+33...) and local (06...) formats.

---

### Workflow 4: List contacts with search

**Context:** Browse contacts or search by keyword.

```bash
# List first 10 contacts
insim contacts list --limit 10

# Search for contacts named "mourad"
insim contacts list --search "mourad" --limit 10

# Get next page
insim --json contacts list --limit 10 --cursor "CURSOR_FROM_PREVIOUS"
```

---

### Workflow 5: Send an SMS to a known contact

**Context:** The user says "send a message to douda saying I love you".

**Step 1 — Find the contact:**
```bash
insim --json contacts search "douda"
```
Take the phone_number from the top result.

**Step 2 — Send the SMS:**
```bash
insim sms send "+21696591256" "I love you"
```

**Expected output:**
```
SMS sent successfully!
  Recipients: 1
```

**Important:**
- Always confirm with the user before sending: "I'll send 'I love you' to Douda (+21696591256). OK?"
- Check credits first with `insim account info` if unsure

---

### Workflow 6: Send an SMS to a direct number

**Context:** The user gives you a phone number directly.

```bash
insim sms send "+33612345678" "Hello from inSIM CLI!"
```

No need to search for a contact — just send directly.

---

### Workflow 7: Send an SMS with a tracked link

**Context:** The user wants to track clicks on a link.

```bash
insim sms send "+33612345678" "Check this out: [link]" --url "https://example.com/promo"
```

The `[link]` placeholder will be replaced by a tracked short URL. Click tracking available via `insim stats clicks`.

---

### Workflow 8: Read a conversation

**Context:** The user says "show me my conversation with mourad".

**Step 1 — Find the contact:**
```bash
insim --json contacts search "mourad"
```

**Step 2 — Read the conversation:**
```bash
insim sms conversation "+33664456336" --limit 20
```

**Expected output:**
```
  >> +33664456336: Wine?
  << +33664456336: En route. T ou ?
  >> +33664456336: Beffroi
```

`>>` = sent, `<<` = received.

---

### Workflow 9: Check recent received SMS

**Context:** The user says "any new messages?"

```bash
insim sms list --direction inbound --limit 5
```

---

### Workflow 10: Check missed calls

**Context:** The user says "any missed calls?"

```bash
insim calls list --type missed --limit 10
```

---

### Workflow 11: Qualify a call

**Context:** After a call, the user wants to categorize it.

**Step 1 — List qualification options:**
```bash
insim --json qualifications options
```

If no options exist, create one:
```bash
insim qualifications options-create "Interested"
insim qualifications options-create "Call back later"
insim qualifications options-create "Not interested"
```

**Step 2 — Find the call:**
```bash
insim --json calls list --type outgoing --limit 5
```

**Step 3 — Qualify:**
```bash
insim calls qualify "CALL_ID" --option "OPTION_ID" --notes "Client interested, callback Friday"
```

---

### Workflow 12: View call statistics

```bash
insim qualifications stats
```

Shows total calls, qualified calls, qualification rate, breakdown by type and category.

---

### Workflow 13: Create a list and add all contacts

**Context:** The user wants to prepare a campaign for all contacts.

```bash
# Create list
insim --json lists create "All Contacts April 2026"

# Add all contacts (one command!)
insim lists add-all "LIST_ID"
```

**Expected output:**
```
  Added: 606
  Skipped: 0
  Total: 606
```

---

### Workflow 14: Create a list with specific contacts

**Context:** The user wants a targeted list.

**Step 1 — Find contacts:**
```bash
insim --json contacts search "dubois"
```

**Step 2 — Create list and add:**
```bash
insim --json lists create "VIP Clients"
insim lists add-contacts "LIST_ID" "CONTACT_ID_1" "CONTACT_ID_2"
```

---

### Workflow 15: Send a campaign SMS to a list

**Context:** The user says "send a promo to all my contacts".

**Step 1 — Create list:**
```bash
insim --json lists create "Promo April"
insim lists add-all "LIST_ID"
```

**Step 2 — Create campaign:**
```bash
insim --json campaigns create --name "Promo April 2026" --message "Hi! 20% off this week only." --list "LIST_ID"
```

**Step 3 — Verify:**
```bash
insim campaigns detail "CAMPAIGN_ID"
```
Check that `recipients > 0` and `status = 0` (ready).

**Step 4 — Launch:**
```bash
insim campaigns start "CAMPAIGN_ID" --confirm
```

**Warning:** This sends real SMS to all recipients. Always confirm with the user first!

---

### Workflow 16: Check SMS credits

```bash
insim --json account info
```

Look at `sms_credits` in the response. If 0, tell the user to recharge.

---

### Workflow 17: Configure webhooks

**Context:** The user wants to receive notifications when SMS are received or calls happen.

```bash
insim account webhooks-set \
  --sms "https://myserver.com/webhook/sms" \
  --calls "https://myserver.com/webhook/calls" \
  --dlr "https://myserver.com/webhook/delivery"
```

---

### Workflow 18: Create and use a message template

**Context:** The user sends similar messages repeatedly.

**Step 1 — Create template:**
```bash
insim --json templates create --name "Appointment Reminder" --message "Hi {firstname}, your appointment is on {custom.date}. Reply STOP to cancel."
```

**Step 2 — Send via template:**
```bash
insim templates send "TEMPLATE_ID" --to "+33612345678" --vars '{"firstname": "Marie", "custom.date": "April 15"}'
```

Variables `{firstname}` and `{lastname}` are auto-resolved from the contact if the phone number matches.

---

### Workflow 19: View global statistics

```bash
insim stats overview
```

Shows: SMS sent/received/delivered, calls in/out/missed/qualified, link clicks, total contacts.

**With date range:**
```bash
insim stats overview --from "2026-01-01" --to "2026-04-12"
```

---

### Workflow 20: View link click tracking

```bash
insim stats clicks --limit 10
```

Shows which links were clicked, by whom, and when.

---

### Workflow 21: Switch a contact to Pro (shared with team)

**Context:** The user wants their team to see a contact.

```bash
insim contacts switch-pro "CONTACT_ID" --pro
```

To make private again:
```bash
insim contacts switch-pro "CONTACT_ID" --perso
```

---

### Workflow 22: Tag contacts for segmentation

**Context:** The user says "mark mourad as VIP".

**Step 1 — Find contact:**
```bash
insim --json contacts search "mourad"
```

**Step 2 — Add tag:**
```bash
insim contacts tags-add "CONTACT_ID" vip
```

**Remove a tag:**
```bash
insim contacts tags-remove "CONTACT_ID" vip
```

---

### Workflow 23: Complete CRM workflow

**Context:** "Check what mourad said and reply to him."

```bash
# 1. Find contact
insim --json contacts search "mourad"

# 2. Read conversation (use phone from search result)
insim sms conversation "+33664456336" --limit 10

# 3. Send reply
insim sms send "+33664456336" "Thanks for your message! I'll get back to you shortly."
```

---

### Workflow 24: Complete campaign workflow

**Context:** "Send a campaign to all clients saying we have a new offer."

```bash
# 1. Check credits
insim --json account info

# 2. Create list
insim --json lists create "New Offer Campaign"

# 3. Add all contacts
insim lists add-all "LIST_ID"

# 4. Create campaign
insim --json campaigns create \
  --name "New Offer April 2026" \
  --message "Great news! We have a new offer for you. Reply YES to learn more." \
  --list "LIST_ID"

# 5. Verify before launch
insim campaigns detail "CAMPAIGN_ID"

# 6. Launch (sends real SMS!)
insim campaigns start "CAMPAIGN_ID" --confirm

# 7. Check results later
insim stats overview
```

---

### Workflow 25: Manage qualifications end-to-end

**Context:** Set up call qualification system and use it.

```bash
# 1. Create qualification categories
insim qualifications options-create "Interested"
insim qualifications options-create "Not interested"
insim qualifications options-create "Callback later"
insim qualifications options-create "Wrong number"

# 2. List recent calls
insim --json calls list --type outgoing --limit 10

# 3. Qualify each call
insim calls qualify "CALL_ID_1" --option "INTERESTED_OPTION_ID" --notes "Wants pricing info"
insim calls qualify "CALL_ID_2" --option "CALLBACK_OPTION_ID" --notes "Call back next Monday"

# 4. View stats
insim qualifications stats
```

---

## Error Handling

| Error Code | Meaning | What to do |
|-----------|---------|------------|
| `INVALID_CREDENTIALS` | Wrong login or access key | Run `insim login` again |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait 1 minute and retry |
| `NOT_FOUND` | Contact/SMS/campaign not found | Check the ID |
| `MISSING_FIELD` | Required parameter missing | Check `--help` for the command |
| `VALIDATION_ERROR` | Invalid format (phone, email) | Fix the input format |
| `PROXY_ERROR` | Backend server unreachable | Check server status |
| `NOT_AUTHENTICATED` | Not logged in | Run `insim login` |

## Tips for AI Agents

1. **Always use `--json`** for reliable parsing.
2. **Use `contacts search` in smart mode** to find contacts — it handles typos and inversions.
3. **Check credits** with `account info` before sending SMS.
4. **Ask user confirmation** before sending SMS or launching campaigns.
5. **Take the highest score** from search results. If score < 30, ask the user to confirm.
6. **Use `--confirm` flag** to skip interactive prompts in automated workflows.
7. **Parse the `cursor` field** from list responses for pagination.
8. **Campaign status:** 2=no recipients, 0=ready, 1=launched, 3=completed. Only status 0 can be started.
