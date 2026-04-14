---
name: insim-cli
description: >-
  CLI to control real mobile phones — send SMS, make calls, qualify leads,
  manage contacts and campaigns from the terminal. Built for AI agents and humans.
---

# insim-cli

Give your AI agent a phone. Your real phone.

## Installation

```bash
pip install insim-cli
```

## Authentication

```bash
# Interactive login
insim login user@email.com --key YOUR_ACCESS_KEY

# Or environment variables (preferred for AI agents)
export INSIM_LOGIN="user@email.com"
export INSIM_ACCESS_KEY="your_access_key"
```

## Commands

### Contacts
| Command | Description |
|---------|-------------|
| `insim contacts list` | List contacts (--search, --limit, --cursor) |
| `insim contacts search NAME` | Smart search by name |
| `insim contacts find-phone PHONE` | Find contact by phone number |
| `insim contacts detail ID` | Full contact details |
| `insim contacts delete ID` | Delete a contact |
| `insim contacts tags-add ID tag1 tag2` | Add tags |
| `insim contacts tags-remove ID tag1` | Remove tags |
| `insim contacts custom-fields` | List custom fields |
| `insim contacts switch-pro ID --pro/--perso` | Share or privatize contact |

### SMS
| Command | Description |
|---------|-------------|
| `insim sms list` | List SMS (--direction, --phone, --limit) |
| `insim sms detail ID` | Full SMS details |
| `insim sms conversation PHONE` | Conversation thread |
| `insim sms send PHONE "message"` | Send an SMS |

### Calls
| Command | Description |
|---------|-------------|
| `insim calls list` | Call log (--type, --phone, --limit) |
| `insim calls qualify ID --option OPT_ID` | Qualify a call |
| `insim calls clictocall PHONE` | Initiate a call |

### Qualifications
| Command | Description |
|---------|-------------|
| `insim qualifications list` | List qualified calls |
| `insim qualifications options` | List categories |
| `insim qualifications options-create LABEL` | Create category |
| `insim qualifications options-update ID LABEL` | Rename category |
| `insim qualifications options-delete ID` | Delete category |
| `insim qualifications stats` | Statistics |

### Campaigns
| Command | Description |
|---------|-------------|
| `insim campaigns list` | List campaigns |
| `insim campaigns create --name X --message Y --list ID` | Create campaign |
| `insim campaigns detail ID` | Campaign details |
| `insim campaigns start ID --confirm` | Launch campaign |
| `insim campaigns cancel ID` | Cancel campaign |

### Lists
| Command | Description |
|---------|-------------|
| `insim lists list` | List all contact lists |
| `insim lists create NAME` | Create a list |
| `insim lists detail ID` | List details |
| `insim lists add-contacts ID C1 C2` | Add contacts |
| `insim lists remove-contacts ID C1` | Remove contacts |
| `insim lists add-all ID` | Add ALL contacts |
| `insim lists delete ID` | Delete a list |

### Templates
| Command | Description |
|---------|-------------|
| `insim templates list` | List templates |
| `insim templates create --name X --message Y` | Create template |
| `insim templates send ID --to PHONE` | Send via template |
| `insim templates update ID --message Y` | Update template |
| `insim templates delete ID` | Delete template |

### Stats
| Command | Description |
|---------|-------------|
| `insim stats overview` | SMS, calls, clicks summary |
| `insim stats clicks` | Link click details |

### Account
| Command | Description |
|---------|-------------|
| `insim account info` | Account details and credits |
| `insim account webhooks-set` | Configure webhook URLs |

## Tips for AI Agents

1. Always use `--json` for reliable parsing: `insim --json contacts search "john"`
2. Check credits with `insim --json account info` before sending SMS
3. Use `contacts search` for fuzzy matching — handles typos and name inversions
4. Ask user confirmation before sending SMS or launching campaigns
5. Campaign status: 0=ready, 1=launched, 3=completed. Only status 0 can be started.
