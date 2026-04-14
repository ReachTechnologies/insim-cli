# "30 overdue invoices this month. I sent 8 reminders."

> **Persona**: David, freelance accountant — Nantes, France — Managing accounts for 15 small businesses
> **Sector**: Accounting / Collections
> **Tool**: insim-cli (command line) + monthly script
> **Setup time**: 10 minutes
> **ROI estimate**: €4,500 additional cash collected per month across his clients, ~€54,000/year

## The problem

David manages accounts receivable for 15 small businesses. Each month, around 30 invoices across his clients go past due. The standard process is to send a polite email reminder, wait a week, send a firmer email, wait another week, then pick up the phone.

The problem is that emails get buried. Open rates on invoice reminders hover around 20%. David spends hours drafting individual follow-ups, and most of them are never read. By the time he escalates to phone calls, the invoices are 30+ days overdue and the conversation is awkward. His clients lose cash flow, and David loses credibility as their accountant. At an average invoice value of €1,500, every month of delay costs real money.

## The solution with inSIM

1. **First of the month** — David exports overdue invoices from his accounting software into a CSV and imports the debtors into inSIM, tagged with the client company and invoice age (`overdue;client-dupont;30days`).
2. **Same day** — He creates a payment reminder campaign with a tracked link to an online payment page. Professional tone, clear deadline.
3. **3 days later** — He checks click stats. Anyone who clicked but did not pay gets a follow-up call. Anyone who did not click gets a second, firmer SMS.
4. **7 days later** — Final reminder SMS before formal collection proceedings.

Total time: 10 minutes per batch. Every debtor is contacted within 24 hours of the due date.

## Key commands

### Import overdue contacts from CSV

```bash
python examples/automation/import-contacts-from-csv.py overdue-april.csv --list "Overdue April 2025"
```

### Create and launch the first reminder campaign

```bash
insim --json campaigns create \
  --name "Payment Reminder - April 2025" \
  --message "Hello {firstname}, invoice #{invoice_number} of {amount} EUR is now overdue. Pay securely here: [link]. Questions? Reply to this SMS. — David, Cabinet Comptable Nantes" \
  --list "LIST_ID" \
  --url "https://cabinet-nantes.fr/pay"

insim campaigns start "CAMPAIGN_ID" --confirm
```

### Check who clicked the payment link

```bash
insim stats clicks --limit 30
```

### Send escalation reminder to non-payers

```bash
insim --json campaigns create \
  --name "Payment Final Reminder - April 2025" \
  --message "Hello {firstname}, this is a final reminder for invoice #{invoice_number} ({amount} EUR). Payment is required by April 15 to avoid collection proceedings. Pay here: [link]. — David" \
  --list "LIST_ID" \
  --url "https://cabinet-nantes.fr/pay"

insim campaigns start "CAMPAIGN_ID_2" --confirm
```

## Results

| Metric | Before inSIM | After inSIM |
|--------|-------------|-------------|
| Overdue invoices contacted | 8 of 30 (27%) | 30 of 30 (100%) |
| Time spent on reminders | 5 hours/month (emails + calls) | 30 min/month (CLI + targeted calls) |
| Payment within 7 days of reminder | 15% | 45% |
| Average days to payment (overdue) | 42 days | 18 days |

David's clients now get paid faster. The SMS open rate (95%+) means debtors actually see the reminder, and the tracked payment link removes friction. The escalation sequence is consistent and professional — no more awkward "I forgot to follow up" situations.

## Related study cases

- [Real estate: Open house follow-up](./real-estate-open-house.md) — The parent pattern for event-based SMS follow-up
- [Insurance broker: Quote follow-up](./insurance-broker-quote.md) — Timed follow-up for lead conversion
- [Travel agent: Departure reminders](./travel-agent-reminders.md) — Scheduled reminder pattern in another sector
