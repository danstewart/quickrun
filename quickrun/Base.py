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

@dataclass
class Server:
	name: str  # The name/tag for this server
	ip: str  # The IP or hostname to connect to
	user: str = "ubuntu"  # The user to connect as


# A command object
@dataclass
class Command:
	name: str  # The name of the command
	cmd: str  # The command itself
	test: bool = False  # Whether this is a test
	expect_fail: bool = False  # Whether to treat non zero exit status as success

class Base:
	def __init__(self):
		self.ok = True
		self.servers: List[Server] = []
		self.commands: List[Command] = []
		self.state: Dict[str, any] = {}
		self.hooks = DefaultHooks()

		# Config
		self.store_state: bool = False
		self.no_display: bool = False

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
			ssh = self.connect(server)
			if not ssh:
				continue

			for command in self.commands:
				self.run(ssh, command, server)

		# Call our after_all hook
		return self.hooks.after_all()

	def connect(self, server: Server):
		"""
		Run prehook, Connect to server, run post hook
		Return ssh instance
		"""
		self.hooks.before_connection(server)

		try:
			ssh = SSH(server.ip, server.user)
		except Exception as e:
			print(f"Following error was raised during ssh to {server}: {e}", file=sys.stderr)
			self.hooks.on_error(e, server=server, action="Connect")
			return

		self.hooks.after_connection(server)
		return ssh

	def run(self, ssh, command: Command, server: Server):
		"""
		Call pre hook, run command, call post hook
		"""
		self.hooks.before_command(server, command)

		try:
			output = ssh.run(command.cmd, strip_cmd=True)
		except Exception as e:
			print(
				f"Following error was raised while running {command} on {server}: {e}",
				file=sys.stderr,
			)
			return self.hooks.on_error(e, server=server, command=command, action="Command")

		if 'output' not in self.state:
			self.state['output'] = []

		self.state['output'].append({
			'server': server.name,
			'ip': server.ip,
			'command': command.cmd.strip(),
			'output': output.strip(),
		})

		self.hooks.after_command(server, command, output)

	def display(self):
		if self.no_display:
			return

		for result in self.state.get('output', []):
			print(result)


# == HELPERS ==#
def arr(item):
	"""
	Ensure $item is a list
	"""
	if isinstance(item, list):
		return item
	return [item]
