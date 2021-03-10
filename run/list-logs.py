#!/usr/bin/env python3

"""
Get the openssl version for all haproxy servers
"""

import sys
import click
from quickrun import Base, Command, Server
from quickrun.lib.aws_cli import find_instances
import quickrun.lib.formatters as formatters


@click.command()
@click.option("--name", required=True, help="The env name to search for")
@click.option("--region", default="eu-west-2", help="The env name to search for")
def main(name, region):
	scratch = Scratch(name=name, region=region)
	scratch.main()
	scratch.display()


class Scratch(Base):
	def __init__(self, name, region="eu-west-2"):
		super().__init__()

		self.formatter = formatters.fake_shell

		# Define our commands
		self.commands = [
			Command(name="List dir", cmd="sudo ls -ld /var/log/tomcat*"),
		]

		# Define our servers
		servers = find_instances(name, region=region)
		servers = list(map(lambda x: Server(name=x["Name"], ip=x["PrivateIp"]), servers))
		self.servers = servers


if __name__ == "__main__":
	main()
