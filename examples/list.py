#!/usr/bin/env python3

"""
List EC2 instances, searching by tag name
"""

import sys
import click
import json as pyjson
from quickrun.cli.aws import find_instances
from rich.console import Console as RichConsole
from rich.table import Table as RichTable


"""
Examples

Search by 'Name' tag:
	list.py --name server-name

Search by 'Environment' tag:
	list.py --tag Environment uat
"""


@click.command()
@click.option("--name", help="The env name to search for")
@click.option("--tag", nargs=2, multiple=True, help="Additional tag filters (In the format: --search key val)")
@click.option("--region", default="eu-west-2", help="The env name to search for")
@click.option("--sort", default="Name", help="The column to sort by")
@click.option("--json", is_flag=True, help="Dumps results (and tags) as json")
def main(name, tag, region, sort, json):
	# Search
	search = { f'tag:{k}': v for k,v in dict(tag).items() }
	if name:
		search['tag:Name'] = name

	servers = find_instances(search, contains=True, region=region)

	# JSON mode
	if json:
		print(pyjson.dumps(servers, indent=2))
		sys.exit(0)

	# Table mode
	table = RichTable(title=f'Instances ({region})')
	fields = ['Name', 'PrivateIp', 'PublicIp', 'InstanceId']

	for header in fields:
		table.add_column(header)

	for server in sorted(servers, key=lambda k: k[sort]):
		table.add_row(*[server.get(f) for f in fields])

	RichConsole().print(table)



if __name__ == "__main__":
	main()


