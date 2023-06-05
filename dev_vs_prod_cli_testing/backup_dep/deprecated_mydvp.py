import click 
import logging

# Set Root level commands
@click.group
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

@cli.command("init",help="Instialize Multi-Instance Dev vs Production Tool")
@click.pass_context
def init_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Initialize Multiinstance Dev vs. Production")

@cli.command("run",help="Run mydvp")
@click.pass_context
def run_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    logging.info(f"Logging info configured at {ctx.obj['LOGGING']}") 
    logging.info(f"ctx is of type {ctx.__dict__}")
    print("Running mydvp")

# Set 'run' child commands

@cli.command("all",help="Run a full test, test all dashboards")
@click.pass_context
def run_all_mydvp(ctx):
    logging.info(f"Running full test, all dashboards being tested") 
    print("Running subcommand")



if __name__ == "__main__":
    cli(obj={})