# "I had 30 visitors at my open house. I followed up with 5."

> **Persona**: Sophie, independent real estate agent — Lyon, France — Solo business
> **Tool**: insim-cli (command line)
> **Setup time**: 15 minutes
> **ROI estimate**: 3 extra appointments per open house, ~€12K additional commission/year

## The problem

Sophie hosts open houses every Saturday. A good one brings 25-30 visitors. Each one fills out a contact card with their name and phone number.

On Saturday evening, she's exhausted. She puts the stack of cards on her desk and tells herself she'll call everyone Monday morning. By Monday, she's already preparing the next listing. She calls 5 or 6 people — the ones she remembers — and the other 25 cards collect dust.

She knows those visitors were interested. They showed up in person. But without a system to follow up quickly, she loses them to competing agents who respond faster. Every lost follow-up is a potential €4,000 commission walking away.

## The solution with inSIM

1. **Saturday evening** — Sophie imports all 30 visitors into inSIM from a simple CSV file. Takes 3 minutes.
2. **Saturday night** — She creates a "thank you" SMS campaign with a tracked link to the property listing. One command, sent to all 30.
3. **Sunday morning** — She checks who clicked the link. Those are the hot prospects.
4. **Sunday afternoon** — She calls only the people who clicked. 10 calls instead of 30, but the right 10.
5. **Monday** — She sends a second SMS to non-clickers: "Still interested? I have 2 more viewings this week."

Total time: 20 minutes. No app switching, no spreadsheets, no forgotten cards.

## Implementation

### Prerequisites

- inSIM app installed on Android phone with your real number
- inSIM account with API access (Settings > API > Access Key)
- Python 3.10+ with insim-cli installed

```bash
pip install insim-cli
insim login sophie@agence-lyon.fr --key YOUR_ACCESS_KEY
```

### Step 1: Import visitors from CSV

Create a file `visitors.csv`:

```csv
firstname,lastname,phone,tags
Marie,Dupont,+33612000001,open-house;rue-garibaldi
Jean,Martin,+33612000002,open-house;rue-garibaldi
Claire,Bernard,+33612000003,open-house;rue-garibaldi
```

Import all contacts using the ready-made script:

```bash
python examples/automation/import-contacts-from-csv.py visitors.csv --list "Open House Rue Garibaldi"
```

This script reads the CSV, creates each contact via the inSIM API, adds tags, and puts them all in a new list. See [`examples/automation/import-contacts-from-csv.py`](../../examples/automation/import-contacts-from-csv.py) for the full source.

### Step 2: Create a contact list

```bash
insim --json lists create "Open House Rue Garibaldi - Apr 12"
```

Note the list ID from the output. Add all tagged contacts:

```bash
# If you used the CSV import with --list, contacts are already in the list.
# Otherwise, add them manually:
insim lists add-contacts "LIST_ID" "CONTACT_1" "CONTACT_2" "CONTACT_3"
```

### Step 3: Send the thank-you campaign

```bash
insim --json campaigns create \
  --name "Open House Follow-up - Rue Garibaldi" \
  --message "Hi {firstname}, thanks for visiting the apartment on Rue Garibaldi today! Here are the full details and photos: [link]" \
  --list "LIST_ID" \
  --url "https://agence-lyon.fr/listings/rue-garibaldi-t3"
```

Verify the campaign details:

```bash
insim campaigns detail "CAMPAIGN_ID"
```

Launch it:

```bash
insim campaigns start "CAMPAIGN_ID" --confirm
```

### Step 4: Check who clicked (Sunday morning)

```bash
insim stats clicks --limit 30
```

This shows which contacts clicked the property link, when, and how many times. The people who clicked are your hot prospects.

### Step 5: Call the hot prospects

```bash
# List all clicks to see who's interested
insim --json stats clicks --limit 30

# For each hot prospect, initiate a call
insim calls clictocall "+33612000001"
```

### Step 6: Follow up with non-clickers (Monday)

```bash
# Create a new campaign for the non-clickers
insim --json campaigns create \
  --name "Open House Reminder - Rue Garibaldi" \
  --message "Hi {firstname}, I noticed you visited Rue Garibaldi on Saturday. I have 2 more viewings this week — would you like to join? Reply YES and I'll save you a spot." \
  --list "LIST_ID"

insim campaigns start "CAMPAIGN_ID_2" --confirm
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Contacts followed up | 5 of 30 (17%) | 30 of 30 (100%) |
| Time spent on follow-up | 2 hours (calls only) | 20 minutes (import + SMS + targeted calls) |
| Hot prospects identified | Unknown | 10-12 per open house (via click tracking) |
| Appointments from open house | 1-2 | 4-5 |
| Commission recovery | ~€4K lost/month | ~€1K/month additional |

Sophie's closing rate from open houses went from 6% to 15% — simply because she follows up with everyone, and prioritizes the right people.

## Variations

- [Insurance broker: SMS follow-up after quote](./insurance-broker-quote.md) *(coming soon)*
- [Car dealership: Follow-up after test drive](./car-dealership-test-drive.md) *(coming soon)*
- [Travel agent: Booking confirmation and reminders](./travel-agent-reminders.md) *(coming soon)*

## Related study cases

- [E-commerce: AI agent answering SMS at night](../../../insim-mcp/docs/use-cases/ecommerce-night-support.md) — Using MCP for automated responses
- [Growth hacker: Abandoned cart SMS via n8n](../../../n8n-nodes-insim/docs/use-cases/shopify-abandoned-cart.md) — No-code SMS automation
