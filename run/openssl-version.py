#!/usr/bin/env python3

"""
Get the openssl version for all haproxy servers
"""

import sys
import click
from quickrun import Base, Command, Server
from quickrun.runners import Table
from quickrun.lib.aws_cli import find_instances

@click.command()
@click.option('--name', required=True, help='The env name to search for')
@click.option('--region', default='eu-west-2', help='The env name to search for')
def main(name, region):
	openssl = Openssl(name=name, region=region)
	openssl.main()
	openssl.display()

class Openssl(Table):
	def __init__(self, name, region='eu-west-2'):
		super().__init__()

		# Define our commands
		self.commands = [
			Command(
				name='Get openssl version',
				cmd="openssl version"
			),
		]

		# Define our servers
		servers = find_instances(name, region=region)
		servers = list(map(lambda x: Server(name=x['Name'], ip=x['PrivateIp']), servers))
		self.servers = servers


if __name__ == '__main__':
	main()

