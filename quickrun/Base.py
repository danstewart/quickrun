#!/usr/bin/env python3

"""
This is the base module all other modules inherit from
It defines the basic outline runners should have and validates they are set correctly
"""

import sys
from typing import List, Dict
from dataclasses import dataclass
from quickrun.lib.ssh import SSH
import quickrun.lib.formatters as formatters


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
		self.formatter = formatters.default

		# Config
		self.store_state: bool = False

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
		self.before_all()

		# Go through all servers and commands and run them
		for server in self.servers:
			ssh = self.connect(server)
			if not ssh:
				continue

			for command in self.commands:
				self.run(ssh, command, server)

		# Call our after_all hook
		return self.after_all()

	def connect(self, server: Server):
		"""
		Run prehook, Connect to server, run post hook
		Return ssh instance
		"""
		self.before_connection(server)

		try:
			ssh = SSH(server.ip, server.user)
		except Exception as e:
			print(
				f"Following error was raised during ssh to {server}: {e}",
				file=sys.stderr,
			)
			self.on_error(e, server=server, action="Connect")
			return

		self.after_connection(server)
		return ssh

	def run(self, ssh, command: Command, server: Server):
		"""
		Call pre hook, run command, call post hook
		"""
		self.before_command(server, command)

		try:
			output = ssh.run(command.cmd, strip_cmd=True)
		except Exception as e:
			print(
				f"Following error was raised while running {command} on {server}: {e}",
				file=sys.stderr,
			)
			return self.on_error(e, server=server, command=command, action="Command")

		if "output" not in self.state:
			self.state["output"] = []

		self.state["output"].append(
			{
				"server": server.name,
				"ip": server.ip,
				"command": command.cmd.strip(),
				"output": output.strip(),
			}
		)

		self.after_command(server, command, output)

	def display(self):
		"""
		Display: Call out to the define formatter for displaying
		"""
		self.formatter(self.state)

	# == HOOKS ==#
	"""
	There are currently 7 types of hooks, and they
	run in the order that that they are defined below
	By default they all do nothing
	You are expected to override them in your run module
	eg. `self.hooks.before_all = lambda x: print("Starting...")`
	"""

	# before_all: Runs before anything is done
	def before_all(self):
		pass

	# before_connection: Runs before connecting to each server
	def before_connection(self, server):
		pass

	# after_connection: Runs after connecting to each server
	def after_connection(self, server):
		pass

	# before_command: Runs before each command is ran
	def before_command(self, server, command):
		pass

	# after_command: Runs after each command is ran
	def after_command(self, server, command, output):
		pass

	# after_all: Runs after everything is done
	def after_all(self):
		pass

	# on_error: Called when an error occurs
	def on_error(self, exception, **info):
		pass


# == HELPERS ==#
def arr(item):
	"""
	Ensure $item is a list
	"""
	if isinstance(item, list):
		return item
	return [item]
