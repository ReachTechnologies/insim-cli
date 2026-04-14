"""Statistics and analytics."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error


@click.group()
def stats():
    """Statistics and analytics."""
    pass


@stats.command("overview")
@click.option("--from", "date_from", default="", help="Start date (YYYY-MM-DD).")
@click.option("--to", "date_to", default="", help="End date (YYYY-MM-DD).")
def stats_overview(date_from, date_to):
    """Show overall statistics for the account."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/stats/overview", {
            "date_from": date_from,
            "date_to": date_to,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@stats.command("clicks")
@click.option("--limit", default=10, type=int, help="Max results to return.")
def stats_clicks(limit):
    """Show link click statistics."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/stats/clicks", {
            "limit": limit,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
