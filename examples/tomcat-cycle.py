#!/usr/bin/env python3

import time
import click
from quickrun import Command, Server
from quickrun.lib.ssh import SSH
from quickrun.lib.aws_cli import find_instances


@click.command()
@click.option("--name", required=True, help="The env name to search for")
@click.option("--region", default="eu-west-2", help="The env name to search for")
def main(name, region):
	servers = Server.from_list(find_instances(name, region=region))

	for server in servers:
		ssh = SSH(server.ip, server.user)
		up = pulse(ssh)

		if up:
			print(f"{server.ip} is running")
		else:
			print(f"{server.ip} is down")


def pulse(ssh, max_attempts=10, sleep_time=10):
	"""
	Checks a tomcats pulse and sleeps between each failed check
	"""
	attempts = 0
	while attempts < max_attempts:
		out, status = ssh.run(
			"curl -m3 http://localhost:8080/encompass/api/v1/health/pulse",
			strip_cmd=True,
			with_exit=True,
		)

		if status == 0:
			break

		time.sleep(sleep_time)
		attempts += 1

	return attempts < max_attempts


if __name__ == "__main__":
	main()
