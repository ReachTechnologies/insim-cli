#!/usr/bin/env python3
"""inSIM CLI — Control your SMS, contacts and campaigns from the command line.

Built for AI agents and humans alike. Wraps the inSIM API v2.

Usage:
    insim login EMAIL --key ACCESS_KEY
    insim contacts search "cecile dubois"
    insim sms send "+33612345678" "Hello from CLI"
    insim campaigns create --name "Promo" --message "Hello!" --list LIST_ID
    insim  (interactive REPL mode)
"""

import sys
import os
import shlex
import click
from typing import Optional

from cli_anything.insim.core.api import InsimAPIError
from cli_anything.insim.core import auth as auth_mod
from cli_anything.insim.utils.output import output, print_error

# Import command groups
from cli_anything.insim.core.contacts import contacts
from cli_anything.insim.core.sms import sms
from cli_anything.insim.core.calls import calls
from cli_anything.insim.core.qualifications import qualifications
from cli_anything.insim.core.account import account
from cli_anything.insim.core.lists import lists
from cli_anything.insim.core.campaigns import campaigns
from cli_anything.insim.core.templates import templates
from cli_anything.insim.core.stats import stats


@click.group(invoke_without_command=True)
@click.option("--json", "json_mode", is_flag=True, default=False, help="Output in JSON format (for AI agents).")
@click.version_option("1.0.0", prog_name="insim-cli")
@click.pass_context
def cli(ctx, json_mode):
    """inSIM CLI — Control your SMS, contacts and campaigns from the command line.

    Run without arguments to start the interactive REPL.
    Add --json to any command for machine-readable output.
    """
    ctx.ensure_object(dict)
    ctx.obj["json"] = json_mode

    if ctx.invoked_subcommand is None:
        start_repl(ctx)


# ── Auth commands (top-level, not in a group) ────────────────────────

@cli.command()
@click.argument("email")
@click.option("--key", prompt="Access Key", hide_input=False, help="Your inSIM API access key.")
@click.pass_context
def login(ctx, email, key):
    """Login to your inSIM account."""
    json_mode = ctx.obj.get("json", False)
    try:
        account_info = auth_mod.login(email, key)
        if json_mode:
            output({"success": True, "account": account_info}, json_mode=True)
        else:
            click.echo(click.style("Logged in successfully!", fg="green", bold=True))
            click.echo(f"  Account: {account_info.get('login', email)}")
            click.echo(f"  Plan: {account_info.get('product', 'free')}")
            click.echo(f"  SMS Credits: {account_info.get('sms_credits', 0)}")
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        sys.exit(1)


@cli.command()
@click.pass_context
def logout(ctx):
    """Logout and remove saved credentials."""
    removed = auth_mod.remove_credentials()
    if removed:
        click.echo("Logged out. Credentials removed.")
    else:
        click.echo("No credentials found.")


@cli.command()
@click.pass_context
def whoami(ctx):
    """Show current account info."""
    json_mode = ctx.obj.get("json", False)
    try:
        info = auth_mod.whoami()
        if json_mode:
            output(info, json_mode=True)
        else:
            click.echo(click.style("Account Info", bold=True))
            click.echo(f"  Login: {info.get('login', '?')}")
            click.echo(f"  Plan: {info.get('product', 'free')}")
            click.echo(f"  SMS Credits: {info.get('sms_credits', 0)}")
            click.echo(f"  Country: {info.get('country_code', '?')}")
            click.echo(f"  Active: {info.get('active', False)}")
            devices = info.get('devices_connected', 0)
            click.echo(f"  Devices Connected: {devices}")
    except InsimAPIError as e:
        print_error(e.error_code, str(e), e.field, e.extra)
        sys.exit(1)


# ── Register command groups ──────────────────────────────────────────

cli.add_command(contacts)
cli.add_command(sms)
cli.add_command(calls)
cli.add_command(qualifications)
cli.add_command(account)
cli.add_command(lists)
cli.add_command(campaigns)
cli.add_command(templates)
cli.add_command(stats)


# ── REPL ─────────────────────────────────────────────────────────────

def start_repl(ctx):
    """Start interactive REPL mode."""
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.completion import WordCompleter
    except ImportError:
        click.echo("Install prompt-toolkit for REPL: pip install prompt-toolkit")
        sys.exit(1)

    # Show SKILL.md path
    skill_path = os.path.join(os.path.dirname(__file__), "skills", "SKILL.md")
    if os.path.exists(skill_path):
        click.echo(f"SKILL.md: {os.path.abspath(skill_path)}")

    click.echo(click.style("inSIM CLI", fg="cyan", bold=True) + " — Interactive Mode")
    click.echo("Type commands without 'insim' prefix. Type 'help' or 'exit'.\n")

    # Build completer from CLI commands
    commands = list(cli.commands.keys())
    subcommands = []
    for name, cmd in cli.commands.items():
        if hasattr(cmd, "commands"):
            for sub in cmd.commands:
                subcommands.append(f"{name} {sub}")
    all_completions = commands + subcommands + ["help", "exit", "quit"]
    completer = WordCompleter(all_completions, ignore_case=True)

    session = PromptSession(completer=completer)

    while True:
        try:
            text = session.prompt("insim> ").strip()
        except (EOFError, KeyboardInterrupt):
            click.echo("\nBye!")
            break

        if not text:
            continue
        if text in ("exit", "quit"):
            click.echo("Bye!")
            break
        if text == "help":
            ctx.invoke(cli, ["--help"])
            continue

        try:
            args = shlex.split(text)
            # Check for --json in args
            if "--json" in args:
                ctx.obj["json"] = True
                args.remove("--json")
            else:
                ctx.obj["json"] = False

            cli.main(args=args, standalone_mode=False, obj=ctx.obj)
        except SystemExit:
            pass
        except Exception as e:
            click.echo(f"Error: {e}", err=True)


def main():
    """Entry point for the CLI."""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cli(obj={})


if __name__ == "__main__":
    main()
