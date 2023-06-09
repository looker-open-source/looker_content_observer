import click 
import logging
# https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

@click.group(name='run', help="Run the Multi Instance Dashboard Checker")
@click.pass_context
def run_mydvp(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print("Intializing Run")


@run_mydvp.command("all",help="Run a full test, test all dashboards")
@click.pass_context
def run_all_mydvp(ctx):
    logging.info("Setting log run")
    print("Running subcommand")

