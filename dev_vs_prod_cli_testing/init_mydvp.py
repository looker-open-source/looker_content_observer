import click
import logging

@click.group(name="init",help="Setup for instances and environments")
@click.pass_context
def init_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Initialize Init")


@init_mydvp.command("environment",help="Create Profile for a new environment")
@click.pass_context
def environment(ctx):
    logging.info("Running setup for environments")
    print("Creating an environment configuration")

