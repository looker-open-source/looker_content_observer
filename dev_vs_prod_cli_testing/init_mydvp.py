import click
import logging
from environments.setup import add_environment

# TODO: Groups that want to go pure CLI and not go through init cycle

@click.group(name="init",help="Setup for instances and environments")
@click.pass_context
def init_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Initialize Init")


@init_mydvp.command("setup",help="Run setup via interface")
@click.pass_context
@click.option('-f',
              '--file-path',
              'looker_file',
              help='File path for looker.ini file',
              default = 'looker.ini')
def setup(ctx,looker_file):
    logging.info("Running setup for environments")
    logging.info(f"looker.ini file path: {looker_file}")
    instances = add_environment(looker_file=looker_file)
    print("Instances",instances)


@init_mydvp.command("cli",
                    help="Skip setup steps and enter information via command line args")
@click.option('-i',
              '--instances',
              'instances',
              type=click.Tuple([str, str]),
              multiple=True,
              help = "For each instance, enter in the looker.ini section name + either 'production' or <looker_project>::<dev_branch>")
@click.pass_context
def args_setup(ctx,instances):
    print(instances)
    pass 
