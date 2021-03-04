class DefaultHooks:
	def __init__(self):
		pass

	# == HOOKS ==#
	# There are currently 6 types of hooks, and they
	# run in the order that that they are defined below
	# By default they all do nothing
	# You are expected to override them in your run module
	# eg. `self.hooks.before_all = lambda x: print("Starting...")`

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

	# == Other hooks ==#

	# on_error: Called when an error occurs
	def on_error(self, exception, **info):
		pass
