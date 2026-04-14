#!/usr/bin/env python3
"""Import contacts from a CSV file into inSIM.

CSV format expected:
    firstname,lastname,phone,email,tags
    Marie,Dupont,+33600000001,marie@example.com,vip;client
    Jean,Martin,+33600000002,jean@example.com,prospect

Usage:
    python import-contacts-from-csv.py contacts.csv
    python import-contacts-from-csv.py contacts.csv --list "Imported April"

Prerequisites:
    pip install insim-cli
    insim login your@email.com --key YOUR_KEY
"""

import csv
import json
import subprocess
import sys
from pathlib import Path


def run_insim(args: list[str]) -> dict:
    """Run an insim CLI command and return parsed JSON output."""
    result = subprocess.run(
        ["insim", "--json"] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  Error: {result.stderr.strip()}", file=sys.stderr)
        return {}
    return json.loads(result.stdout) if result.stdout.strip() else {}


def import_csv(csv_path: str, list_name: str | None = None) -> None:
    """Import contacts from CSV and optionally add them to a list."""
    path = Path(csv_path)
    if not path.exists():
        print(f"File not found: {csv_path}")
        sys.exit(1)

    # Read CSV
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Found {len(rows)} contacts in {csv_path}")

    # Create list if requested
    list_id = None
    if list_name:
        result = run_insim(["lists", "create", list_name])
        list_id = result.get("list", {}).get("_id")
        if list_id:
            print(f"Created list '{list_name}' ({list_id})")

    # Import each contact
    imported_ids = []
    for i, row in enumerate(rows, 1):
        phone = row.get("phone", "").strip()
        firstname = row.get("firstname", "").strip()
        lastname = row.get("lastname", "").strip()

        if not phone:
            print(f"  [{i}/{len(rows)}] Skipped — no phone number")
            continue

        # Build add command
        args = ["contacts", "add", phone]
        if firstname:
            args.extend(["--firstname", firstname])
        if lastname:
            args.extend(["--lastname", lastname])

        result = run_insim(args)
        contact_id = result.get("contact", {}).get("_id")

        if contact_id:
            imported_ids.append(contact_id)
            print(f"  [{i}/{len(rows)}] {firstname} {lastname} ({phone}) -> {contact_id}")

            # Add tags if present
            tags = row.get("tags", "").strip()
            if tags:
                tag_list = [t.strip() for t in tags.split(";") if t.strip()]
                if tag_list:
                    run_insim(["contacts", "tags-add", contact_id] + tag_list)
        else:
            print(f"  [{i}/{len(rows)}] Failed: {phone}")

    # Add to list if created
    if list_id and imported_ids:
        run_insim(["lists", "add-contacts", list_id] + imported_ids)
        print(f"\nAdded {len(imported_ids)} contacts to list '{list_name}'")

    print(f"\nDone. Imported {len(imported_ids)}/{len(rows)} contacts.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import-contacts-from-csv.py <file.csv> [--list 'List Name']")
        sys.exit(1)

    csv_file = sys.argv[1]
    target_list = None

    if "--list" in sys.argv:
        idx = sys.argv.index("--list")
        if idx + 1 < len(sys.argv):
            target_list = sys.argv[idx + 1]

    import_csv(csv_file, target_list)
