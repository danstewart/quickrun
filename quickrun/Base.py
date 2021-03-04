#!/usr/bin/env python3

"""
This is the base module all other modules inherit from
It defines the basic outline runners should have and validates they are set correctly
"""

import sys
from typing import List, Dict
from dataclasses import dataclass
from quickrun.lib.ssh import SSH
from quickrun.hooks import DefaultHooks


class Base:
	def __init__(self):
		self.ok = True
		self.servers: List[Server] = []
		self.commands: List[Command] = []
		self.state: Dict[str, any] = {}
		self.hooks = DefaultHooks()

	# Run the commands
	def main(self):
		"""
		Main execution function
		"""
		# Ensure we have arrays
		self.servers = arr(self.servers)
		self.commands = arr(self.commands)

		# Check we actually have stuff to do
		if len(self.servers) == 0 or len(self.commands) == 0:
			print("Nothing to do")

		# Call our before_all hook
		self.hooks.before_all()

		# Go through all servers and commands and run them
		for server in self.servers:
			# Call pre hook, connect to server, call post hook
			self.hooks.before_connection(server)
			try:
				ssh = SSH(server.ip, server.user)
			except Exception as e:
				print(f"Following error was raised during ssh to {server}: {e}", file=sys.stderr)
				return self.hooks.on_error(e, server=server, action="Connect")
			self.hooks.after_connection(server)

			for command in self.commands:
				# Call pre hook, run command, call post hook
				self.hooks.before_command(server, command)
				try:
					output = ssh.run(command.cmd, strip_cmd=True)
				except Exception as e:
					print(
						f"Following error was raised while running {command} on {server}: {e}",
						file=sys.stderr,
					)
					return self.hooks.on_error(e, server=server, command=command)

				self.hooks.after_command(server, command, output)

		# Call our after_all hook
		return self.hooks.after_all()


# == HELPERS ==#
def arr(item):
	"""
	Ensure $item is a list
	"""
	if isinstance(item, list):
		return item
	return [item]
