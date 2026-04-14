# "15 test drives this weekend. I called back 3."

> **Persona**: Thomas, sales manager at a car dealership — Toulouse, France — 8-person sales team
> **Sector**: Automotive
> **Tool**: insim-cli (command line)
> **Setup time**: 15 minutes
> **ROI estimate**: 2 extra vehicle sales per month, ~€24,000 additional margin/year

## The problem

Thomas manages the sales floor at a multi-brand dealership. On a busy weekend, 15 people take test drives. Each one fills out a form with their contact details and the model they drove. By Monday, the forms are in a pile on his desk and his team is already busy with walk-ins.

The sales reps remember the "serious" prospects — the ones who asked about financing — and call them back. The other 10 or 12 test drivers never hear from the dealership again. But Thomas knows from experience that many buyers need 2-3 visits before deciding. Without a prompt follow-up, they drift to the competitor dealership 5 km away. At €1,000 margin per sale, every lost buyer hurts.

## The solution with inSIM

1. **Sunday evening** — Thomas imports all 15 test drivers from a CSV into inSIM, tagged with the model they drove (`test-drive;peugeot-3008`).
2. **Sunday night** — He creates a satisfaction survey campaign with a tracked link. The SMS thanks them for the test drive and asks them to rate their experience.
3. **Monday morning** — He checks who clicked. Clickers are still engaged. He also checks survey responses to spot any complaints.
4. **Tuesday** — He sends a second SMS to all test drivers with a booking link for a second visit, mentioning a current promotion.

Total time: 20 minutes. Every test driver gets a personal follow-up within 24 hours.

## Key commands

### Import test drivers from CSV

```bash
python examples/automation/import-contacts-from-csv.py test-drives-weekend.csv --list "Test Drives Apr 12-13"
```

### Create the satisfaction survey campaign

```bash
insim --json campaigns create \
  --name "Test Drive Satisfaction - Apr 12-13" \
  --message "Hi {firstname}, thanks for test driving the Peugeot 3008 with us! How was your experience? Take 30 seconds to tell us: [link] — Thomas, Garage Toulouse Sud" \
  --list "LIST_ID" \
  --url "https://garage-toulouse.fr/survey/test-drive"

insim campaigns start "CAMPAIGN_ID" --confirm
```

### Check engagement and send booking reminder

```bash
insim stats clicks --limit 20

insim --json campaigns create \
  --name "Test Drive Second Visit - Apr 12-13" \
  --message "Hi {firstname}, still thinking about the {model}? We have a special offer this week: 0% financing for 36 months. Book your second visit here: [link] — Thomas" \
  --list "LIST_ID" \
  --url "https://garage-toulouse.fr/book-visit"

insim campaigns start "CAMPAIGN_ID_2" --confirm
```

### Call engaged prospects

```bash
insim calls clictocall "+33600000001"
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Test drivers followed up | 3 of 15 (20%) | 15 of 15 (100%) |
| Time spent on follow-up | 2 hours of individual calls | 20 min CLI + targeted calls |
| Second visits booked | 2-3 per weekend | 5-7 per weekend |
| Monthly vehicle sales from test drives | 4 | 6 |

Thomas's test-drive-to-sale conversion rate went from 12% to 20%. The satisfaction survey also catches unhappy prospects early, giving the team a chance to recover the relationship.

## Related study cases

- [Real estate: Open house follow-up](./real-estate-open-house.md) — The parent pattern for event-based SMS follow-up
- [Insurance broker: Quote follow-up](./insurance-broker-quote.md) — Same pattern applied to insurance sales
- [Recruitment: Campus outreach](./recruitment-campus-outreach.md) — Event-based follow-up for HR
