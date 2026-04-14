"""Call qualifications: options, stats."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_table


@click.group()
def qualifications():
    """Call qualifications: options, stats."""
    pass


@qualifications.command("list")
@click.option("--phone", default="", help="Filter by phone number.")
@click.option("--limit", default=10, type=int, help="Max results to return.")
def qualifications_list(phone, limit):
    """List call qualifications."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {"limit": limit}
        if phone:
            data["phone_number"] = phone
        result = api.post("/api/v2/qualifications", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@qualifications.command("options")
def qualifications_options():
    """List available qualification options."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/qualifications/options")
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("options", [])
            rows = [
                [o.get("_id", ""), o.get("label", "")]
                for o in items
            ]
            print_table(["ID", "Label"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@qualifications.command("options-create")
@click.argument("label")
def qualifications_options_create(label):
    """Create a new qualification option."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/qualifications/options/create", {
            "label": label,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Option '{label}' created.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@qualifications.command("options-update")
@click.argument("id")
@click.argument("label")
def qualifications_options_update(id, label):
    """Update a qualification option label."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/qualifications/options/update", {
            "option_id": id,
            "label": label,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Option '{id}' updated.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@qualifications.command("options-delete")
@click.argument("id")
def qualifications_options_delete(id):
    """Delete a qualification option."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/qualifications/options/delete", {
            "option_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Option '{id}' deleted.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@qualifications.command("stats")
@click.option("--from", "date_from", default="", help="Start date (YYYY-MM-DD).")
@click.option("--to", "date_to", default="", help="End date (YYYY-MM-DD).")
def qualifications_stats(date_from, date_to):
    """Show qualification statistics."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {}
        if date_from:
            data["date_from"] = date_from
        if date_to:
            data["date_to"] = date_to
        result = api.post("/api/v2/qualifications/stats", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
