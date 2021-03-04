from quickrun import Base
from rich.console import Console as RichConsole
from rich.table import Table as RichTable

class Table(Base):
	def __init__(self):
		super().__init__()
		self.store_state = True

	def display(self):
		table = RichTable(title="Results")

		data = self.state.get('output', [])
		if len(data) > 0:
			for column in data[0].keys():
				table.add_column(column)

		for item in data:
			table.add_row(*item.values())

		RichConsole().print(table)
