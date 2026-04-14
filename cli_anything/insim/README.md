# insim-cli

**Control your SMS, contacts, and campaigns from the command line.**

[![PyPI version](https://img.shields.io/pypi/v/insim-cli.svg)](https://pypi.org/project/insim-cli/)
[![Python](https://img.shields.io/pypi/pyversions/insim-cli.svg)](https://pypi.org/project/insim-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Why insim-cli?

**Stop switching between tabs.** Manage your entire SMS business from your terminal.

- **Send SMS in seconds** — one command, done. No login pages, no clicks.
- **AI-ready** — Claude, GPT, Gemini, and any LLM can pilot inSIM with structured JSON output.
- **Automate your campaigns** — create lists, compose messages, and launch campaigns programmatically.
- **Track everything** — call logs, delivery reports, click tracking, all at your fingertips.
- **Works everywhere** — macOS, Linux, Windows. Any terminal. Any automation tool.

## Quick Start (2 minutes)

### 1. Install

```bash
pip install insim-cli
```

### 2. Login

```bash
insim login your@email.com --key YOUR_ACCESS_KEY
```

Your access key is in your inSIM account settings, under API.

### 3. Start using

```bash
# Find a contact
insim contacts search "John Doe"

# Send an SMS
insim sms send "+33612345678" "Hello from the command line!"

# Check your stats
insim stats overview
```

That's it. You're ready.

---

## What can you do?

### Send SMS

```bash
# Simple message
insim sms send "+33612345678" "Meeting confirmed for tomorrow at 10am"

# With link tracking
insim sms send "+33612345678" "Check our offer: [link]" --url "https://your-site.com/promo"
```

### Manage Contacts

```bash
# Smart search (handles typos, inversions, accents)
insim contacts search "cecile dubois"

# Find by phone number
insim contacts find-phone "0612345678"

# Tag contacts for segmentation
insim contacts tags-add CONTACT_ID vip premium
```

### Launch Campaigns

```bash
# Create a list with all your contacts
insim lists create "Spring Promo"
insim lists add-all LIST_ID

# Create and launch a campaign
insim campaigns create --name "Spring Promo" --message "20% off this week!" --list LIST_ID
insim campaigns start CAMPAIGN_ID
```

### Track Calls

```bash
# See missed calls
insim calls list --type missed

# Qualify a call
insim calls qualify CALL_ID --option OPTION_ID --notes "Interested in premium plan"
```

### View Statistics

```bash
# Global overview
insim stats overview

# SMS sent this month
insim stats overview --from "2026-04-01"
```

---

## For AI Agents

insim-cli is designed to be used by AI coding agents like **Claude Code**, **GitHub Copilot**, **Cursor**, and others.

### Setup for agents

```bash
export INSIM_LOGIN="your@email.com"
export INSIM_ACCESS_KEY="your_access_key"
```

### JSON output

Add `--json` to any command for machine-readable output:

```bash
insim --json contacts search "john doe"
insim --json sms list --limit 5
insim --json account info
```

### AI workflow example

An agent receiving "send a message to John saying meeting is confirmed":

```bash
# Step 1: Find the contact
insim --json contacts search "john"
# → {"contacts": [{"phone_number": "+33612345678", "score": 100}]}

# Step 2: Send the SMS
insim sms send "+33612345678" "Meeting is confirmed"
# → SMS sent successfully!
```

### SKILL.md

The package includes a comprehensive `SKILL.md` file with **25 detailed workflows** that any AI agent can read to understand exactly how to use every feature of insim-cli. The REPL mode displays the path to this file on startup.

---

## Interactive Mode (REPL)

Run `insim` without arguments for an interactive session with **auto-completion** and **command history**:

```
$ insim
SKILL.md: /path/to/skills/SKILL.md
inSIM CLI — Interactive Mode
Type commands without 'insim' prefix. Type 'help' or 'exit'.

insim> contacts search "mourad"
insim> sms send "+33664456336" "Hello!"
insim> stats overview
insim> exit
```

---

## All Commands

| Group | Commands |
|-------|----------|
| **Auth** | `login`, `logout`, `whoami` |
| **Contacts** | `list`, `search`, `find-phone`, `detail`, `switch-pro`, `delete`, `tags-add`, `tags-remove`, `custom-fields` |
| **SMS** | `list`, `detail`, `conversation`, `send` |
| **Calls** | `list`, `qualify`, `clictocall` |
| **Qualifications** | `list`, `options`, `options-create`, `options-update`, `options-delete`, `stats` |
| **Account** | `info`, `webhooks-set` |
| **Lists** | `list`, `create`, `detail`, `update`, `delete`, `add-contacts`, `remove-contacts`, `add-all` |
| **Campaigns** | `list`, `create`, `detail`, `cancel`, `start` |
| **Templates** | `list`, `create`, `update`, `delete`, `send` |
| **Stats** | `overview`, `clicks` |

Run `insim COMMAND --help` for details on any command.

---

## Configuration

| Method | Priority | Description |
|--------|----------|-------------|
| Environment variables | Highest | `INSIM_LOGIN`, `INSIM_ACCESS_KEY` |
| Credentials file | Lower | `~/.insim/credentials.json` (created by `insim login`) |

Custom server URL:
```bash
export INSIM_BASE_URL="https://custom-server.com"
```

---

## Development

```bash
git clone https://github.com/ArdaryinSIM/insim-cli.git
cd insim-cli
pip install -e ".[dev]"
pytest tests/ -v
```

---

## About inSIM

[inSIM](https://insim.app) is a SaaS platform for SMS management, CRM, and marketing campaigns. It connects to your phone via a mobile app and lets you send, receive, and track SMS from your computer.

**insim-cli** is the official command-line interface, built by [Reach Technologies SAS](https://reach-technologies.com).

---

## License

MIT
