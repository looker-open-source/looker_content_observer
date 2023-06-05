import click
import logging
from environments.setup import add_environment
import yaml

@click.group(name="init",help="Setup for instances and environments")
@click.pass_context
def init_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Initialize Init")


@init_mydvp.command("environment",help="Create Profile for a new environment")
@click.pass_context
@click.option('-f',
              '--file-path',
              'looker_file',
              help='File path for looker.ini file')
def environment(ctx,looker_file):
    logging.info("Running setup for environments")
    logging.info(f"looker.ini file path: {looker_file}")
    instances = add_environment(looker_file=looker_file)
    print("Instances",instances)

