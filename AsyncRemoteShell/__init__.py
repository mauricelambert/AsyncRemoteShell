#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This package implement 4 asynchronous tools to execute remote commands
#    Copyright (C) 2020  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
	This package implement 4 asynchronous tools to execute remote commands :
		- One ReverseShellClient
		- One ReverseShellServer
		- One ShellServer
		- One ShellClient
"""

__version__ = "0.0.1"

__all__ = [
	"ReverseShellServer", "ReverseShellClient", "ShellServer", "ShellClient", 
	"reverse_shell_server", "reverse_shell_client", "shell_server", "shell_client"
]

print("""
AsyncRemoteShell  Copyright (C) 2020  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
""")

from AsyncRemoteShell.ReverseShellServer import ReverseShellServer, main as reverse_shell_server
from AsyncRemoteShell.ReverseShellClient import ReverseShellClient, main as reverse_shell_client
from AsyncRemoteShell.ShellServer import ShellServer, main as shell_server
from AsyncRemoteShell.ShellClient import ShellClient, main as shell_client