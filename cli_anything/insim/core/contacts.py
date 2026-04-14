"""Contacts commands: search, list, update, tag."""
import click
from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core.auth import require_auth
from cli_anything.insim.utils.output import (
    output,
    print_contact,
    print_error,
    print_table,
    truncate,
)


@click.group()
def contacts():
    """Manage contacts: search, list, update, tag."""
    pass


@contacts.command("list")
@click.option("--search", default="", help="Filter contacts by text.")
@click.option("--limit", default=10, type=int, help="Max results to return.")
@click.option("--cursor", default="", help="Pagination cursor.")
@click.option("--sort", default="", help="Sort field.")
@click.option("--order", default="", help="Sort order (asc/desc).")
def contacts_list(search, limit, cursor, sort, order):
    """List contacts with optional filtering and pagination."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        data = {"limit": limit}
        if search:
            data["search"] = search
        if cursor:
            data["cursor"] = cursor
        if sort:
            data["sort"] = sort
        if order:
            data["order"] = order
        result = api.post("/api/v2/contacts", data)
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("contacts", [])
            rows = [
                [
                    c.get("lastname", ""),
                    c.get("firstname", ""),
                    c.get("phone_number", ""),
                    c.get("email", ""),
                ]
                for c in items
            ]
            print_table(["Lastname", "Firstname", "Phone", "Email"], rows)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("search")
@click.argument("name")
@click.option(
    "--mode",
    type=click.Choice(["smart", "exact", "starts_with"]),
    default="smart",
    help="Search mode.",
)
@click.option("--fuzzy/--no-fuzzy", default=True, help="Enable fuzzy matching.")
@click.option("--limit", default=5, type=int, help="Max results.")
def contacts_search(name, mode, fuzzy, limit):
    """Search contacts by name."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/search", {
            "name": name,
            "mode": mode,
            "fuzzy": fuzzy,
            "limit": limit,
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("contacts", [])
            if not items:
                click.echo("No contacts found.")
                return
            for c in items:
                print_contact(c)
                click.echo()
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("find-phone")
@click.argument("phone")
def contacts_find_phone(phone):
    """Find contacts by phone number."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/find_contact", {"phone_number": phone})
        if json_mode:
            output(result, json_mode=True)
        else:
            items = result.get("contacts", [])
            if not items:
                click.echo("No contacts found.")
                return
            for c in items:
                print_contact(c)
                click.echo()
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("detail")
@click.argument("id")
def contacts_detail(id):
    """Show detailed info for a contact."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/detail", {"id_contact": id})
        output(result, json_mode=json_mode)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("switch-pro")
@click.argument("id")
@click.option("--pro/--perso", required=True, help="Set contact as PRO or PERSO.")
def contacts_switch_pro(id, pro):
    """Toggle a contact between PRO and PERSO."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/switch_pro", {
            "id_contact": id,
            "pro": pro,
        })
        output(result, json_mode=json_mode)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("delete")
@click.argument("id")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt.")
def contacts_delete(id, confirm):
    """Delete a contact by ID."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    if not confirm:
        click.confirm("Delete contact?", abort=True)
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/delete", {"id_contact": id})
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style("Contact deleted.", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("tags-add")
@click.argument("id")
@click.argument("tags", nargs=-1)
def contacts_tags_add(id, tags):
    """Add tags to a contact."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/tags", {
            "id_contact": id,
            "add": list(tags),
            "remove": [],
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Added {len(tags)} tag(s).", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("tags-remove")
@click.argument("id")
@click.argument("tags", nargs=-1)
def contacts_tags_remove(id, tags):
    """Remove tags from a contact."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/tags", {
            "id_contact": id,
            "add": [],
            "remove": list(tags),
        })
        if json_mode:
            output(result, json_mode=True)
        else:
            click.echo(click.style(f"Removed {len(tags)} tag(s).", fg="green"))
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)


@contacts.command("custom-fields")
def contacts_custom_fields():
    """List all custom fields defined for contacts."""
    ctx = click.get_current_context()
    json_mode = ctx.obj.get("json", False) if ctx.obj else False
    try:
        api = require_auth()
        result = api.post("/api/v2/contacts/custom_fields")
        output(result, json_mode=json_mode)
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        raise SystemExit(1)
