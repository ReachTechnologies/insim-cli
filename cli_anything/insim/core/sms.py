"""SMS commands: send, list, read conversations."""
from datetime import datetime

import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_sms, truncate


@click.group()
def sms():
    """SMS: send, list, read conversations."""
    pass


@sms.command("list")
@click.option(
    "--direction",
    type=click.Choice(["all", "inbound", "outbound"]),
    default="all",
    help="Filter by direction.",
)
@click.option("--phone", default="", help="Filter by phone number.")
@click.option("--from", "date_from", default="", help="Start date (YYYY-MM-DD).")
@click.option("--to", "date_to", default="", help="End date (YYYY-MM-DD).")
@click.option("--limit", default=5, type=int, help="Max results.")
def sms_list(direction, phone, date_from, date_to, limit):
    """List SMS messages with optional filters."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {"direction": direction, "limit": limit}
        if phone:
            data["phone_number"] = phone
        if date_from:
            data["date_from"] = date_from
        if date_to:
            data["date_to"] = date_to
        result = api.post("/api/v2/sms", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            messages = result.get("messages", [])
            if not messages:
                click.echo("No messages found.")
                return
            for m in messages:
                print_sms(m)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@sms.command("detail")
@click.argument("id")
def sms_detail(id):
    """Show details for a specific SMS."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/sms/detail", {"sms_id": id})
        output(result, json_mode=json_mode)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@sms.command("conversation")
@click.argument("phone")
@click.option("--limit", default=20, type=int, help="Max messages to return.")
def sms_conversation(phone, limit):
    """Show the SMS conversation with a phone number."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/sms/conversation", {
            "phone_number": phone,
            "limit": limit,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            messages = result.get("messages", [])
            if not messages:
                click.echo("No messages in conversation.")
                return
            for m in messages:
                print_sms(m)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@sms.command("send")
@click.argument("phone")
@click.argument("message")
@click.option("--url", default="", help="URL to include in the SMS.")
def sms_send(phone, message, url):
    """Send an SMS to a phone number."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/sendsms", {
            "messages": [
                {
                    "phone_number": phone,
                    "message": message,
                    "url": url,
                    "priority": 1,
                    "date_to_send": datetime.now().isoformat(),
                }
            ],
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            sent_count = result.get("sent_count", 0)
            res_list = result.get("result", [])
            actually_sent = sum(1 for r in res_list if isinstance(r, dict) and r.get("sent") == 1) if isinstance(res_list, list) else sent_count
            click.echo(click.style(f"SMS sent! {actually_sent} message(s) delivered.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@sms.command("delivery-status")
@click.argument("sms_ids", nargs=-1, required=True)
def sms_delivery_status(sms_ids):
    """Check delivery status for one or more SMS by ID.

    Example: insim sms delivery-status ID1 ID2 ID3
    """
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        ids = list(sms_ids)
        data = {"sms_id": ids[0]} if len(ids) == 1 else {"sms_ids": ids}
        result = api.post("/api/v2/sms/delivery_status", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            for s in result.get("statuses", []):
                status = s.get("delivery_status", "unknown")
                colors = {"delivered": "green", "sent": "yellow", "pending": "cyan", "failed": "red", "blocked": "red", "not_found": "white"}
                color = colors.get(status, "white")
                icons = {"delivered": ">>", "sent": ">", "pending": "~", "failed": "X", "blocked": "!", "not_found": "?"}
                click.echo(f"  {click.style(icons.get(status, '?'), fg=color)} {s.get('phone_number', '')}  {click.style(status.upper(), fg=color, bold=True)}  {s.get('description', '')}")
                preview = s.get("message_preview", "")
                if preview:
                    click.echo(f"    {truncate(preview, 60)}")
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
