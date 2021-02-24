import click

import app_api
from commands import atm, auth
from commands.transfer import do_transfer


@click.group()
def cli():
    pass


@cli.command()
def serve():
    """Run the Flask+Swagger app"""
    app_api.run_app()


@cli.command()
@click.argument('user_name', required=True, type=str)
@click.argument('pin', required=True, type=int)
def login(user_name: str, pin: int) -> None:
    """Usage: login username pin (e.g login ola 123) \n
     Returns: token for a session valid for 7 days"""
    click.echo(auth.login(user_name, pin))


@cli.command()
@click.argument('token', required=True)
def logout(token: str) -> None:
    """Usage: logout token (e.g logout R5T9sF3TO)"""
    click.echo(auth.logout(token))


@cli.command()
@click.argument('token', required=True, type=str)
def balance(token: str) -> None:
    """Usage: balance token (e.g balance R5T9sF3TO) \n
    Returns: current balance for account"""
    click.echo(atm.balance(token))


@cli.command()
@click.argument('token', required=True, type=str)
@click.argument('amount', required=True, type=int)
def deposit(token: str, amount: int) -> None:
    """Usage: deposit token amount (e.g deposit R5T9sF3TO 50)"""
    click.echo(atm.deposit(token, amount))


@cli.command()
@click.argument('token', required=True, type=str)
@click.argument('amount', required=True, type=int)
def withdraw(token: str, amount: int):
    """Usage: withdraw token amount (e.g withdraw R5T9sF3TO 50)"""
    click.echo(atm.withdraw(token, amount))


@cli.command()
@click.argument('token', required=True, type=str)
@click.argument('second_party', required=True, type=str)
@click.argument('amount', required=True, type=int)
def transfer(token: str, second_party: str, amount: int) -> None:
    """Usage: transfer token second_party amount (e.g transfer R5T9sF3TO jane 50)"""
    click.echo(do_transfer(token, second_party, amount))
