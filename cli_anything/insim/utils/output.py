"""Output formatting: JSON for agents, human-readable for humans."""
import json
import click
from typing import Any


def output(data: Any, message: str = "", json_mode: bool = False) -> None:
    if json_mode:
        click.echo(json.dumps(data, indent=2, default=str, ensure_ascii=False))
    else:
        if message:
            click.echo(message)
        if isinstance(data, dict):
            _print_dict(data)
        elif isinstance(data, list):
            _print_list(data)
        else:
            click.echo(str(data))


def _print_dict(d: dict, indent: int = 0) -> None:
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            click.echo(f"{prefix}{click.style(k, fg='cyan')}:")
            _print_dict(v, indent + 1)
        elif isinstance(v, list):
            click.echo(f"{prefix}{click.style(k, fg='cyan')}: [{len(v)} items]")
            if v and indent < 2:
                _print_list(v, indent + 1)
        elif isinstance(v, bool):
            color = "green" if v else "red"
            click.echo(f"{prefix}{click.style(k, fg='cyan')}: {click.style(str(v), fg=color)}")
        else:
            click.echo(f"{prefix}{click.style(k, fg='cyan')}: {v}")


def _print_list(items: list, indent: int = 0) -> None:
    prefix = "  " * indent
    for i, item in enumerate(items):
        if isinstance(item, dict):
            click.echo(f"{prefix}{click.style(f'[{i}]', fg='yellow')}")
            _print_dict(item, indent + 1)
        else:
            click.echo(f"{prefix}- {item}")


def print_table(headers: list[str], rows: list[list]) -> None:
    if not rows:
        click.echo("  (empty)")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    header_line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    click.echo(click.style(header_line, bold=True))
    click.echo("  ".join("-" * w for w in widths))
    for row in rows:
        click.echo("  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))


def print_contact(c: dict) -> None:
    name = f"{c.get('firstname', '')} {c.get('lastname', '')}".strip() or "(no name)"
    phone = c.get("phone_number", "")
    email = c.get("email", "")
    pro = "PRO" if c.get("pro") else "PERSO"
    tags = ", ".join(c.get("tags", [])) or "-"
    click.echo(f"  {click.style(name, bold=True)}  {phone}  {email}")
    click.echo(f"  {pro}  Tags: {tags}")
    score = c.get("score")
    if score is not None:
        match_type = c.get("match_type", "")
        click.echo(f"  Score: {score} ({match_type})")


def print_sms(s: dict) -> None:
    direction = click.style("<<" if s.get("direction") == "inbound" else ">>", fg="green" if s.get("direction") == "inbound" else "blue")
    phone = s.get("phone_number", "")
    msg = truncate(s.get("message", ""), 80)
    click.echo(f"  {direction} {phone}: {msg}")


def truncate(text: str, max_len: int = 50) -> str:
    text = text.replace("\n", " ").strip()
    return text[:max_len] + "..." if len(text) > max_len else text


def print_error(error_code: str, message: str, field: str = "", extra: dict | None = None) -> None:
    if error_code == "LICENSE_REQUIRED":
        print_license_error(message, extra or {})
        return
    click.echo(click.style(f"Error [{error_code}]", fg="red", bold=True) + f": {message}", err=True)
    if field:
        click.echo(click.style(f"  Field: {field}", fg="yellow"), err=True)


def print_license_error(message: str, extra: dict) -> None:
    sub_type = extra.get("subscription_type", "")
    upgrade_url = extra.get("upgrade_url", "https://www.insim.app")

    click.echo("", err=True)
    if sub_type == "premium expired":
        click.echo(click.style("  Subscription Expired", fg="yellow", bold=True), err=True)
    else:
        click.echo(click.style("  Premium Required", fg="yellow", bold=True), err=True)
    click.echo("", err=True)
    click.echo(f"  {message}", err=True)
    click.echo("", err=True)
    click.echo(f"  {click.style('Upgrade now', bold=True)} -> {click.style(upgrade_url, fg='cyan', underline=True)}", err=True)
    click.echo(f"  Go to Menu > {click.style('Get Premium', fg='green')} to start.", err=True)
    click.echo("", err=True)
