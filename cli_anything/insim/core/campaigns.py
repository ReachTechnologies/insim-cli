"""SMS campaigns: create, launch, track."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_table


@click.group()
def campaigns():
    """SMS campaigns: create, launch, track."""
    pass


@campaigns.command("list")
@click.option("--limit", default=10, type=int, help="Max results to return.")
def campaigns_list(limit):
    """List SMS campaigns."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/campaigns", {
            "limit": limit,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("campaigns", [])
            rows = [
                [
                    c.get("name", ""),
                    c.get("status", ""),
                    str(c.get("sent", 0)),
                    c.get("created", ""),
                ]
                for c in items
            ]
            print_table(["Name", "Status", "Sent", "Created"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@campaigns.command("create")
@click.option("--name", required=True, help="Campaign name.")
@click.option("--message", required=True, help="SMS message body.")
@click.option("--list", "list_id", default="", help="Target list ID.")
@click.option("--contacts", default="", help="Comma-separated contact IDs.")
@click.option("--phones", default="", help="Comma-separated phone numbers.")
@click.option("--priority", default=0, type=int, help="Campaign priority.")
def campaigns_create(name, message, list_id, contacts, phones, priority):
    """Create a new SMS campaign."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        payload = {
            "name": name,
            "message": message,
            "priority": priority,
        }
        if list_id:
            payload["list_id"] = list_id
        if contacts:
            payload["contact_ids"] = [c.strip() for c in contacts.split(",") if c.strip()]
        if phones:
            payload["phone_numbers"] = [p.strip() for p in phones.split(",") if p.strip()]
        result = api.post("/api/v2/campaigns/create", payload)
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Campaign '{name}' created.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@campaigns.command("detail")
@click.argument("id")
def campaigns_detail(id):
    """Show campaign details."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/campaigns/detail", {
            "campaign_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@campaigns.command("cancel")
@click.argument("id")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt.")
def campaigns_cancel(id, confirm):
    """Cancel a campaign."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    if not confirm:
        click.confirm("Cancel this campaign?", abort=True)
    try:
        api = require_auth()
        result = api.post("/api/v2/campaigns/cancel", {
            "campaign_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Campaign cancelled.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@campaigns.command("start")
@click.argument("id")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt.")
def campaigns_start(id, confirm):
    """Launch a campaign. This will send SMS messages."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    if not confirm:
        click.confirm("Launch campaign? This will send SMS.", abort=True)
    try:
        api = require_auth()
        result = api.post("/api/v2/campaigns/start", {
            "campaign_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Campaign launched.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
