import click
import logging
from setups.instance_env import add_environment,create_instance_yaml

@click.group(name="init",help="Setup for instances and environments")
@click.pass_context
def init_lco(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Initialize Init")


@init_lco.command("setup",help="Run setup via interface")
@click.pass_context
@click.option('-f',
              '--file-path',
              'looker_file',
              type=click.Path(exists=True), # Validates that file path is valid
              help='File path for looker.ini file',
              default = 'looker.ini')
def setup(ctx,looker_file):
    logging.info("Running setup for environments")
    logging.info(f"looker.ini file path: {looker_file}")
    instances = add_environment(looker_file=looker_file)
    create_instance_yaml(instances)
    print("Instances",instances)


@init_lco.command("cli",
                    help="Skip setup steps and enter information via command line args")
@click.option('-i',
              '--instances',
              'instances',
              type=click.Tuple([str, str]),
              multiple=True,
              help = "For each instance, enter in the looker.ini section name + either 'production' or <looker_project>::<dev_branch>")
@click.pass_context
def args_setup(ctx,instances):
    create_instance_yaml(instances)
    logging.info("Saved instance + environment configuration to the configs/instance_environment_configs.yaml file")
    print("Following instances loaded via CLI:",instances)