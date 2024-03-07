# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import logging
from setups.instance_env import add_environment,create_instance_yaml
from _lco.colorprint import ColorPrint

@click.group(name="init",help="Setup for instances and environments")
@click.pass_context
def init_lco(ctx):
    logging.basicConfig(level=getattr(logging,ctx.obj['LOGGING']))
    print(ColorPrint.yellow + "Starting init for Looker Content Observer" + ColorPrint.end)


@init_lco.command("setup",help="Use this if first time, runs a guided setup wizard")
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
    print("Looker Content Observer will be checking for differences between:")
    output_lambda = lambda instance_str: f"{instance_str[0]} on {instance_str[1]}"
    if len(instances) > 1:
        for instance in instances:
            print(output_lambda(instance))
    else: 
        print(output_lambda(instances[0]))

@init_lco.command("cli",
                    help="Skips setup wizard and allows setup via command line args")
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