import click 
import logging

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


# @run_mydvp.command("test",help="Test Command")
# def run_mydvp(level):
#     logging.basicConfig(level=getattr(logging,level))\

# cli.add_command(init_mydvp)
# cli.add_command(run_mydvp)

cli(obj={})