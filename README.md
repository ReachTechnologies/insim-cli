# insim-cli

> **Give your AI agent a phone. Your real phone.**

[![PyPI version](https://img.shields.io/pypi/v/insim-cli.svg)](https://pypi.org/project/insim-cli/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/insim-cli.svg)](https://pypi.org/project/insim-cli/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/ReachTechnologies/insim-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/ReachTechnologies/insim-cli/actions)

## The problem

Your AI agent can search the web, write code, send emails — but it can't make a real phone call or send an SMS from a real mobile number.

Meanwhile, your mobile phone is your most powerful sales tool — but everything that happens on it stays trapped in your pocket.

## The solution

```bash
pip install insim-cli
```

Now your terminal, your scripts, and your AI agents can send SMS, manage contacts, run campaigns, qualify calls, and track engagement. All from your real mobile number, using your existing phone plan.

## Quickstart

### 1. Install

```bash
pip install insim-cli
```

### 2. Login

```bash
insim login your@email.com --key YOUR_ACCESS_KEY
```

Your access key is in your [inSIM account settings](https://www.insim.app), under API.

### 3. Send your first SMS

```bash
insim sms send "+33600000000" "Hello from the command line!"
```

That's it. You're ready.

## What you can do

| Domain | Commands | What it does |
|--------|----------|-------------|
| **Contacts** | `list`, `search`, `find-phone`, `detail`, `delete`, `tags-add`, `tags-remove`, `switch-pro`, `custom-fields` | Full CRM from the terminal |
| **SMS** | `list`, `detail`, `conversation`, `send` | Send, receive, and track SMS |
| **Calls** | `list`, `qualify`, `clictocall` | Call log, qualification, click-to-call |
| **Campaigns** | `list`, `create`, `detail`, `start`, `cancel` | Mass SMS campaigns |
| **Lists** | `list`, `create`, `detail`, `update`, `delete`, `add-contacts`, `remove-contacts`, `add-all` | Contact list management |
| **Templates** | `list`, `create`, `update`, `delete`, `send` | Reusable message templates |
| **Qualifications** | `list`, `options`, `options-create`, `options-update`, `options-delete`, `stats` | Call qualification system |
| **Stats** | `overview`, `clicks` | Analytics and link tracking |
| **Account** | `info`, `webhooks-set` | Account info and webhook configuration |

> Add `--json` to any command for machine-readable output. AI agents should always use `--json`.

## Examples

### Send an SMS

```bash
insim sms send "+33600000000" "Meeting confirmed for tomorrow at 2pm"
```

### Find a contact and read the conversation

```bash
insim contacts search "Marie Dupont"
insim sms conversation "+33612345678" --limit 20
```

### Create and launch a campaign

```bash
# Create a list and add all contacts
insim lists create "Spring Campaign"
insim lists add-all "LIST_ID"

# Create and launch the campaign
insim campaigns create --name "Spring 2026" --message "20% off this week!" --list "LIST_ID"
insim campaigns start "CAMPAIGN_ID" --confirm
```

### Check your stats

```bash
insim stats overview --from "2026-01-01" --to "2026-04-14"
```

More examples in the [`examples/`](./examples) directory.

## AI Agent Integration

insim-cli is built for AI agents. Any LLM that can run shell commands can use it.

```bash
# JSON output for reliable parsing
insim --json contacts search "john"
insim --json sms list --limit 5
insim --json account info

# Environment variables (no interactive login needed)
export INSIM_LOGIN="user@email.com"
export INSIM_ACCESS_KEY="your_access_key"
```

### Compatible with

**IDE & code agents:** Claude Code, Cursor, Windsurf, VS Code + Copilot, Cline, Kiro (AWS), Codex CLI (OpenAI), Augment Code, OpenClaw

**AI agents:** ChatGPT, Claude Desktop, Devin, Manus AI, Mistral Le Chat

**Frameworks:** LangChain, LangGraph, CrewAI, AutoGen, Pydantic AI, Vercel AI SDK, Mastra

**Automation:** n8n, Zapier, Make, Activepieces, Pipedream

> **One CLI. 20+ compatible AI clients.** Any agent that can run shell commands can send SMS from a real phone.

## Authentication

### Interactive login

```bash
insim login your@email.com --key YOUR_ACCESS_KEY
```

Credentials are saved to `~/.insim/credentials.json`.

### Environment variables (recommended for AI agents)

```bash
export INSIM_LOGIN="your@email.com"
export INSIM_ACCESS_KEY="your_access_key"
```

### Check your session

```bash
insim whoami
```

## Interactive REPL

Run `insim` without arguments to start the interactive mode:

```bash
$ insim
insim> contacts search "mourad"
insim> sms send "+33600000000" "Hello!"
insim> exit
```

## Study Cases

- [Real estate agent: SMS follow-up after open house](./docs/use-cases/) *(coming soon)*
- [E-commerce: AI agent answering SMS at night](./docs/use-cases/) *(coming soon)*
- [Growth hacker: Abandoned cart SMS via n8n](./docs/use-cases/) *(coming soon)*

## Installation from source

```bash
git clone https://github.com/ReachTechnologies/insim-cli.git
cd insim-cli
pip install -e ".[dev]"
```

## Requirements

- Python 3.10+
- An inSIM account with API access
- The [inSIM Android app](https://play.google.com/store/apps/details?id=com.wstechnologies.ardarysolo) installed on your phone

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and guidelines.

## License

Apache 2.0 — see [LICENSE](./LICENSE).

---

Built by [Reach Technologies](https://www.insim.app) — the company behind inSIM.
