"""Account info and configuration."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error


@click.group()
def account():
    """Account info and configuration."""
    pass


@account.command("info")
def account_info():
    """Show account information: login, plan, credits, options."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/account")
        if json_mode:
            output(result, json_mode=True)
        else:
            acct = result.get("account", {})
            click.echo(click.style("Account Information", bold=True))
            click.echo(f"  {click.style('Login', fg='cyan')}: {acct.get('login', '')}")
            click.echo(f"  {click.style('Plan', fg='cyan')}: {acct.get('plan', '')}")
            click.echo(f"  {click.style('Credits', fg='cyan')}: {acct.get('credits', '')}")
            options = acct.get("options", {})
            if options:
                click.echo(f"  {click.style('Options', fg='cyan')}:")
                for key, val in options.items():
                    click.echo(f"    {key}: {val}")
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@account.command("webhooks-set")
@click.option("--sms", default="", help="Incoming SMS webhook URL.")
@click.option("--dlr", default="", help="Delivery status webhook URL.")
@click.option("--clicks", default="", help="Link clicks webhook URL.")
@click.option("--calls", default="", help="Call events webhook URL.")
@click.option("--qualif", default="", help="Call qualifications webhook URL.")
def account_webhooks_set(sms, dlr, clicks, calls, qualif):
    """Set account webhook URLs."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/account/webhooks", {
            "webhooks": {
                "incoming_sms": sms,
                "delivery_status": dlr,
                "link_clicks": clicks,
                "call_events": calls,
                "call_qualifications": qualif,
            },
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Webhooks updated.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
