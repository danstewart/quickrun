#!/usr/bin/env python3

import sys
from typing import List, Dict
from dataclasses import dataclass
from quickrun.Base import Base


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
