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
import sys
sys.path.append("../looker_content_observer/")
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
    ctx.obj['LOGGING'] = logging.upper()


if __name__ == "__main__":
    cli(obj={})