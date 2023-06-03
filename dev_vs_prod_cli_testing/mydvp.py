import click 


# @click.command
# @click.option("--name",prompt="Enter your name: ",help="Nam eof user")
# def hello(name):
#     # click.echo(f"Hello {name}")
#     print(f"Hello {name}")
#     return name


@click.group
@click.option('--init',help="Startup Command Available")
def cli():
    pass 

@click.command
@click.option("--init",help="Init for the MyDvP")
def initmydvp():
    print("Initialize Multiinstance Dev vs. Production")

@click.command
def dropmydvp():
    print("Remove My DvP")


@click.group
def test():
    pass 

@click.command
def another():
    print("Initialize Multiinstance Dev vs. Production")

@click.command
def one():
    print("Remove My DvP")


cli.add_command(initmydvp)
cli.add_command(dropmydvp)

cli.add_command(another)
cli.add_command(one)
cli()
