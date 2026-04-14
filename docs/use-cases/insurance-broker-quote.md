# "I send 20 quotes a week. I follow up on 5."

> **Persona**: Paul, independent insurance broker — Bordeaux, France — 3-person agency
> **Sector**: Insurance
> **Tool**: insim-cli (command line)
> **Setup time**: 10 minutes
> **ROI estimate**: 4 extra signed contracts per month, ~€9,600 additional commission/year

## The problem

Paul sends around 20 insurance quotes per week — home, car, health, professional liability. Each quote goes out by email with a PDF attached. Then nothing happens.

He knows the conversion sweet spot is 48 hours. After that, prospects go cold or sign with a competitor who followed up first. But Paul barely has time to handle inbound calls, let alone chase 20 people every week. He manages to call back 5 or 6 — usually the ones with the largest premiums — and hopes the rest will call him. They rarely do. At his average commission of €200 per contract, every lost follow-up stings.

## The solution with inSIM

1. **Friday afternoon** — Paul exports the week's quote recipients from his CRM into a CSV and imports them into inSIM. Tags each batch with `quote-week-15`.
2. **Friday evening** — He creates a follow-up SMS campaign with a tracked link pointing to a personalized quote page. One command sends it to all 20 recipients.
3. **Saturday morning** — He checks click stats. Anyone who clicked is actively comparing prices — these are hot leads.
4. **Monday morning** — He calls clickers first, then sends a second reminder SMS to non-clickers with a limited-time offer.

Total time: 15 minutes. Every quote recipient gets a follow-up within 24 hours.

## Key commands

### Import quote recipients from CSV

```bash
python examples/automation/import-contacts-from-csv.py quotes-week15.csv --list "Quotes Week 15"
```

### Create and launch the follow-up campaign

```bash
insim --json campaigns create \
  --name "Quote Follow-up - Week 15" \
  --message "Hi {firstname}, your insurance quote is ready! Review it here: [link]. Questions? Reply to this SMS and I'll call you back. — Paul, Assurances Bordeaux" \
  --list "LIST_ID" \
  --url "https://assurances-bordeaux.fr/quotes/view"

insim campaigns start "CAMPAIGN_ID" --confirm
```

### Check who clicked the quote link

```bash
insim stats clicks --limit 20
```

### Call hot prospects directly

```bash
insim calls clictocall "+33600000001"
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Quote follow-up rate | 5 of 20 (25%) | 20 of 20 (100%) |
| Time spent on follow-up | 3 hours of phone calls | 15 min CLI + targeted calls |
| Quotes converted per week | 3-4 | 5-6 |
| Annual additional commission | Baseline | ~€9,600 |

Paul's quote-to-contract conversion rate went from 17% to 28%. The tracked link tells him exactly who is shopping around, so he calls the right people at the right time.

## Related study cases

- [Real estate: Open house follow-up](./real-estate-open-house.md) — The parent pattern for event-based SMS follow-up
- [Car dealership: Test drive follow-up](./car-dealership-test-drive.md) — Same pattern applied to automotive sales
- [Collections: Invoice follow-up](./collections-invoice-followup.md) — Follow-up pattern for payment reminders
