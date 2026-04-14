# "My clients forget their departure date. I forget to remind them."

> **Persona**: Nadia, independent travel agent — Marseille, France — Solo business
> **Sector**: Travel & Tourism
> **Tool**: insim-cli (command line) + cron automation
> **Setup time**: 20 minutes
> **ROI estimate**: 15% fewer missed flights, 5-star reviews from proactive service, ~€6,000 saved in rebooking fees/year

## The problem

Nadia books around 40 trips per month for her clients — flights, hotels, transfers, excursions. After the booking is confirmed, she sends an email with all the details. Then the trip fades from her mind until the client calls in a panic the night before, having forgotten their flight time or hotel address.

She tried setting calendar reminders for each client, but with 40 bookings a month it became unmanageable. She also loses repeat business when clients feel like "just a transaction." The agents who send a friendly reminder a week before departure — with practical tips about their destination — are the ones who earn loyalty and referrals. Every rebooking due to a missed flight costs her €150 in admin time and goodwill.

## The solution with inSIM

1. **At booking time** — Nadia adds the client to inSIM with tags for the destination and departure date (`trip-marrakech;depart-2025-04-19`).
2. **7 days before departure** — A scheduled script sends a preparation reminder SMS with a tracked link to a personalized trip summary page.
3. **1 day before departure** — A second automated SMS sends last-minute details: flight time, terminal, hotel check-in info.
4. **After the trip** — She checks click stats to see who engaged, then sends a "welcome back" SMS with a review link.

Total time per client: 3 minutes at booking. Reminders run automatically.

## Key commands

### Import travelers from CSV (monthly batch)

```bash
python examples/automation/import-contacts-from-csv.py bookings-april.csv --list "Departures April 2025"
```

### Create the 7-day reminder template

```bash
insim templates create \
  --name "Trip Reminder 7 Days" \
  --content "Hi {firstname}, your trip to {destination} is in 7 days! Check your personalized travel summary here: [link]. Don't forget your passport! — Nadia, Voyages Marseille"
```

### Send reminders to departing clients

```bash
# Send to a specific traveler (used by the automation script)
insim sms send "+33600000001" \
  "Hi Marie, your trip to Marrakech is in 7 days! Check your travel summary: https://voyages-marseille.fr/trips/MRK-2025-04-19. Don't forget your passport! — Nadia"

# Send the day-before reminder
insim sms send "+33600000001" \
  "Hi Marie, you fly tomorrow! Flight AT540 at 08:15 from Marseille T1. Hotel check-in from 14:00. Have a wonderful trip! — Nadia"
```

### Check engagement after the trip

```bash
insim stats clicks --limit 40

insim sms send "+33600000001" \
  "Welcome back Marie! How was Marrakech? I'd love your feedback: https://voyages-marseille.fr/review. Already thinking about your next trip? — Nadia"
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Clients reminded before departure | ~10 of 40 (25%) | 40 of 40 (100%) |
| Missed flights / wrong terminal incidents | 2-3 per month | 0-1 per month |
| Time spent on reminders | 4 hours/month (manual calls) | 20 min/month (setup + review) |
| Repeat booking rate | 30% | 45% |

Nadia's clients now describe her as "the agent who actually cares." Her Google reviews mention the reminders by name. The automated system costs her almost no time but creates a premium service experience.

## Related study cases

- [Real estate: Open house follow-up](./real-estate-open-house.md) — The parent pattern for event-based SMS follow-up
- [Insurance broker: Quote follow-up](./insurance-broker-quote.md) — Timed follow-up pattern in another sector
- [Collections: Invoice follow-up](./collections-invoice-followup.md) — Scheduled reminder pattern for payments
