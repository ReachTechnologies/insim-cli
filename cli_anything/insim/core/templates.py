"""Message templates: create, send."""
import json as json_lib

import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_table


@click.group()
def templates():
    """Message templates: create, send."""
    pass


@templates.command("list")
def templates_list():
    """List all message templates."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/templates")
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("templates", [])
            rows = [
                [t.get("name", ""), t.get("message", "")[:60]]
                for t in items
            ]
            print_table(["Name", "Message"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@templates.command("create")
@click.option("--name", required=True, help="Template name.")
@click.option("--message", required=True, help="Template message body.")
def templates_create(name, message):
    """Create a new message template."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/templates/create", {
            "name": name,
            "message": message,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Template '{name}' created.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@templates.command("update")
@click.argument("id")
@click.option("--name", default="", help="New template name.")
@click.option("--message", default="", help="New template message body.")
def templates_update(id, name, message):
    """Update a message template."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {"template_id": id}
        if name:
            data["name"] = name
        if message:
            data["message"] = message
        result = api.post("/api/v2/templates/update", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Template updated.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@templates.command("delete")
@click.argument("id")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt.")
def templates_delete(id, confirm):
    """Delete a message template."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    if not confirm:
        click.confirm("Delete this template?", abort=True)
    try:
        api = require_auth()
        result = api.post("/api/v2/templates/delete", {
            "template_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Template deleted.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@templates.command("send")
@click.argument("id")
@click.option("--to", "phone", required=True, help="Recipient phone number.")
@click.option("--vars", "variables", default="", help="Template variables as JSON string.")
def templates_send(id, phone, variables):
    """Send a template to a recipient."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        parsed_vars = json_lib.loads(variables) if variables else {}
    except json_lib.JSONDecodeError:
        print_error("INVALID_JSON", "The --vars value must be valid JSON.")
        raise SystemExit(1)
    try:
        api = require_auth()
        result = api.post("/api/v2/templates/send", {
            "template_id": id,
            "recipients": [
                {
                    "phone_number": phone,
                    "variables": parsed_vars,
                },
            ],
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Template sent to {phone}.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
