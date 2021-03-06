#!/usr/bin/env python3

"""
Example module
"""

import sys
import click
from rich.console import Console
from quickrun import QuickRun, Command, Server
from quickrun.cli.aws import find_instances

console = Console()

@click.command()
@click.option("--name", required=True, help="The env name to search for")
@click.option("--region", default="eu-west-2", help="The env name to search for")
def main(name, region):
	get_settings = GetSettings(name=name, region=region)
	get_settings.main()


class GetSettings(QuickRun):
	def __init__(self, name, region="eu-west-2"):
		super().__init__()

		# Define our commands
		self.commands = [
			Command(
				name="Get free memory",
				cmd="free -h | head -2 | tail -1 | awk '{ print $2 }'",
			),
			Command(name="Get heap size", cmd="grep --color=none -i xmx /etc/default/tomcat"),
		]

		# Define our servers
		self.servers = Server.from_list(find_instances({ 'tag:Name': name }, contains=True, region=region))

	# == HOOKS ==#
	def before_connection(self, server):
		console.print(f"{server.name}", style="cyan underline")

	def after_command(self, server, command, output):
		console.print(f"Running: {command.cmd}")
		console.print(output, style="green")


if __name__ == "__main__":
	main()
