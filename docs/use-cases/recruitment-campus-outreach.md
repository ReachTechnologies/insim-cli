# "I collected 200 CVs at the career fair. I contacted 20."

> **Persona**: Sarah, HR manager at a mid-size tech company — Paris, France — 3-person recruitment team
> **Sector**: Recruitment / Human Resources
> **Tool**: insim-cli (command line)
> **Setup time**: 15 minutes
> **ROI estimate**: 8 extra qualified candidates per event, ~€16,000 saved in recruitment agency fees/year

## The problem

Sarah visits 5 campus career fairs per year. A good event brings 200 candidates who drop off a CV or scan a QR code. Her team collects the contacts in a spreadsheet and promises to "get back to everyone."

Back at the office, the team is buried in day-to-day hiring. They cherry-pick 20 CVs that look promising and send individual emails. The other 180 candidates never hear back. Many of them are good fits for junior roles, internships, or future openings — but they move on to companies that responded first. At €2,000 per hire through an agency, every candidate they lose to slow follow-up is money wasted on recruiters later.

## The solution with inSIM

1. **Day of the event** — Sarah exports all scanned contacts into a CSV and imports them into inSIM, tagged with the campus and event date (`campus-dauphine;spring-2025`).
2. **Same evening** — She creates an SMS campaign with a tracked link to the company's application portal, pre-filtered for junior roles.
3. **Next day** — She checks click stats. Candidates who clicked are actively interested — these go to the top of the review pile.
4. **One week later** — She sends a reminder to non-clickers with a deadline to apply.

Total time: 15 minutes. Every candidate gets a response within 24 hours of the event.

## Key commands

### Import candidates from CSV

```bash
python examples/automation/import-contacts-from-csv.py campus-dauphine-spring2025.csv --list "Campus Dauphine Spring 2025"
```

### Create and launch the outreach campaign

```bash
insim --json campaigns create \
  --name "Campus Dauphine - Spring 2025" \
  --message "Hi {firstname}, great meeting you at the Dauphine career fair! We're hiring for 6 junior positions. Apply directly here: [link]. — Sarah, TechCorp Recruitment" \
  --list "LIST_ID" \
  --url "https://techcorp.fr/careers/junior-roles"

insim campaigns start "CAMPAIGN_ID" --confirm
```

### Check who clicked the application link

```bash
insim stats clicks --limit 50
```

### Send a reminder to non-clickers

```bash
insim --json campaigns create \
  --name "Campus Dauphine - Reminder" \
  --message "Hi {firstname}, just a reminder: applications for our junior roles close Friday. Don't miss out: [link]. — Sarah, TechCorp" \
  --list "LIST_ID" \
  --url "https://techcorp.fr/careers/junior-roles"

insim campaigns start "CAMPAIGN_ID_2" --confirm
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Candidates contacted post-event | 20 of 200 (10%) | 200 of 200 (100%) |
| Time spent on post-event outreach | 6 hours (individual emails) | 15 min CLI campaign |
| Applications received per event | 12-15 | 35-45 |
| Hires from campus events per year | 5 | 9 |

Sarah's team now treats campus events as a pipeline, not a lottery. Click tracking reveals which candidates are motivated, letting the team prioritize reviews. The branded SMS also positions the company as responsive and tech-forward — exactly the image they want with junior talent.

## Related study cases

- [Real estate: Open house follow-up](./real-estate-open-house.md) — The parent pattern for event-based SMS follow-up
- [Car dealership: Test drive follow-up](./car-dealership-test-drive.md) — Event-based follow-up in another sector
- [Insurance broker: Quote follow-up](./insurance-broker-quote.md) — Timed follow-up for lead conversion
