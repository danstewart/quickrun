#!/usr/bin/env python3

import time
import click
import quickrun

@click.command()
@click.option("--host", required=True, help="The hostname to connect to")
@click.option("--user", required=True, help="The user to log in as")
def main(host, user):
	server = quickrun.Server(name=host, host=host, user=user)

	conn = quickrun.ssh(server.host, server.user)
	up = check(conn)

	if up:
		print(f"{server.host} is running")
	else:
		print(f"{server.host} is down")


def check(conn, max_attempts=10, sleep_time=10):
	"""
	Checks web server is running
	"""
	attempts = 0
	while attempts < max_attempts:
		out, status = conn.run(
			"curl -m3 http://127.0.0.1:5001/api/ping",
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
