"""Calls commands: list, qualify, click-to-call."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_table


@click.group()
def calls():
    """Calls: list, qualify, click-to-call."""
    pass


@calls.command("list")
@click.option(
    "--type",
    "call_type",
    type=click.Choice(["all", "incoming", "outgoing", "missed"]),
    default="all",
    help="Filter by call type.",
)
@click.option("--phone", default="", help="Filter by phone number.")
@click.option("--limit", default=10, type=int, help="Max results.")
def calls_list(call_type, phone, limit):
    """List calls with optional filters."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {"type": call_type, "limit": limit}
        if phone:
            data["phone_number"] = phone
        result = api.post("/api/v2/calls", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("calls", [])
            rows = [
                [
                    c.get("type", ""),
                    c.get("phone_number", ""),
                    c.get("duration", ""),
                    c.get("call_time", ""),
                ]
                for c in items
            ]
            print_table(["Type", "Phone", "Duration", "Time"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@calls.command("qualify")
@click.argument("id")
@click.option("--option", "option_id", required=True, help="Qualification option ID.")
@click.option("--notes", default="", help="Additional notes.")
def calls_qualify(id, option_id, notes):
    """Qualify a call with an option and optional notes."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/calls/qualify", {
            "call_id": id,
            "option_id": option_id,
            "notes": notes,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Call qualified.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@calls.command("clictocall")
@click.argument("phone")
def calls_clictocall(phone):
    """Initiate a click-to-call to a phone number."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/clictocall", {"phone_number": phone})
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Calling {phone}...", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
