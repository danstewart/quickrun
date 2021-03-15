#!/usr/bin/env python3

"""
Template to use for making other scripts
"""

import sys
import click
from quickrun import QuickRun, Command, Server, formatters
from quickrun.cli.aws import find_instances
from quickrun.cli.helpers import challenge


@click.command()
@click.option("--name", required=True, help="The env name to search for")
@click.option("--region", default="eu-west-2", help="The env name to search for")
def main(name, region):
	qr = QuickRun()

	# Setup
	qr.formatter = formatters.fake_shell
	qr.commands = [
		Command(name="List files", cmd="ls -ltr"),
	]

	qr.servers = Server.from_list(find_instances({ 'tag:Name': name }, region=region))

	if not challenge(expect=len(qr.servers), msg=f'Running against {len(qr.servers)} servers'):
		print('Challenge failed')
		sys.exit(1)

	qr.main()
	qr.display()


if __name__ == "__main__":
	main()
