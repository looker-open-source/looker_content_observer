#License Header

import click 
import logging
from init_lco import init_lco
from run_lco import run_lco

# Set list of commands
commands = {
    "init":init_lco, 
    "run": run_lco
}

# Set Root level commands
@click.group(
        commands = commands
)
@click.option('-l','--logging',
              help ="Set the logging level",
              type=click.Choice(['debug', 'info','critical'],
                                case_sensitive=False),
              default = 'critical')
@click.pass_context
def cli(ctx,logging):
    # Context Obj Docs: https://click.palletsprojects.com/en/8.1.x/complex/#contexts
    ctx.ensure_object(dict)
    # TODO: What does this mean / do exactly
    ctx.obj['LOGGING'] = logging.upper()


if __name__ == "__main__":
    cli(obj={})