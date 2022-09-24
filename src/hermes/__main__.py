"""__main__ - CLI runner"""

import click


@click.group()
def cli():
    """Outer CLI group"""
    pass


@click.command()
def initdb():
    """Sample command"""
    click.echo('Initialized the database')


@click.command()
def dropdb():
    """Sample command"""
    click.echo('Dropped the database')


cli.add_command(initdb)
cli.add_command(dropdb)
