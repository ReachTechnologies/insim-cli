"""Contact lists: create, manage members."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import output, print_error, print_table


@click.group()
def lists():
    """Contact lists: create, manage members."""
    pass


@lists.command("list")
def lists_list():
    """List all contact lists."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists")
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("lists", [])
            rows = [
                [
                    li.get("name", ""),
                    str(li.get("contacts", 0)),
                    li.get("created", ""),
                ]
                for li in items
            ]
            print_table(["Name", "Contacts", "Created"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("create")
@click.argument("name")
@click.option("--desc", default="", help="List description.")
def lists_create(name, desc):
    """Create a new contact list."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/create", {
            "name": name,
            "description": desc,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"List '{name}' created.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("detail")
@click.argument("id")
@click.option("--limit", default=10, type=int, help="Max contacts to show.")
def lists_detail(id, limit):
    """Show list details and members."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/detail", {
            "list_id": id,
            "limit": limit,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            output(result, json_mode=False)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("update")
@click.argument("id")
@click.option("--name", default="", help="New list name.")
@click.option("--desc", default="", help="New list description.")
def lists_update(id, name, desc):
    """Update a contact list."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/update", {
            "list_id": id,
            "name": name,
            "description": desc,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("List updated.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("delete")
@click.argument("id")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt.")
def lists_delete(id, confirm):
    """Delete a contact list."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    if not confirm:
        click.confirm("Delete this list?", abort=True)
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/delete", {
            "list_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("List deleted.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("add-contacts")
@click.argument("id")
@click.argument("contacts", nargs=-1)
def lists_add_contacts(id, contacts):
    """Add contacts to a list by ID."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/contacts/add", {
            "list_id": id,
            "contact_ids": list(contacts),
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Added {len(contacts)} contact(s) to list.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("remove-contacts")
@click.argument("id")
@click.argument("contacts", nargs=-1)
def lists_remove_contacts(id, contacts):
    """Remove contacts from a list by ID."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/contacts/remove", {
            "list_id": id,
            "contact_ids": list(contacts),
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Removed {len(contacts)} contact(s) from list.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@lists.command("add-all")
@click.argument("id")
def lists_add_all(id):
    """Add all contacts to a list."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/lists/contacts/addall", {
            "list_id": id,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("All contacts added to list.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
