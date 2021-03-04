#!/usr/bin/env python3

"""
Example module
"""

import sys
from rich.console import Console
from quickrun import Base, Command, Server
from quickrun.lib.aws_cli import find_instances

console = Console()


class GetSettings(Base):
	def __init__(self):
		super().__init__()

		# Define our hooks
		self.hooks.before_connection = self.before_connection
		self.hooks.after_command = self.after_command

		# Define our commands
		self.commands = [
			Command(
				name="Get free memory", cmd="free -h | head -2 | tail -1 | awk '{ print $2 }'"
			),
			Command(name="Get heap size", cmd="grep --color=none -i xmx /etc/default/tomcat"),
		]

		# Define our servers
		servers = find_instances("my-server-name")
		servers = list(map(lambda x: Server(name=x["Name"], ip=x["PrivateIp"]), servers))
		self.servers = servers

	# == HOOKS ==#
	def before_connection(self, server):
		console.print(f"{server.name}", style="cyan underline")

	def after_command(self, server, command, output):
		console.print(f"Running: {command.cmd}")
		console.print(output, style="green")


if __name__ == "__main__":
	get_settings = GetSettings()
	get_settings.main()
	get_settings.display()
