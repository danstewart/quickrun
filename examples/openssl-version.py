#!/usr/bin/env python3

"""
Get the openssl version for all haproxy servers
"""

import sys
import click
import quickrun.lib.formatters as formatters
from quickrun import QuickRun, Command, Server
from quickrun.lib.aws_cli import find_instances


@click.command()
@click.option("--name", required=True, help="The env name to search for")
@click.option("--region", default="eu-west-2", help="The env name to search for")
def main(name, region):
	qr = QuickRun()

	# Setup
	qr.formatter = formatters.table

	qr.commands = [
		Command(name="Get openssl version", cmd="openssl version"),
	]

	qr.servers = Server.from_list(find_instances(name, region=region))

	qr.main()
	qr.display()


if __name__ == "__main__":
	main()
