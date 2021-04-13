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
        - ReverseShellClient
        - ReverseShellServer
        - ShellServer
        - ShellClient
"""

__version__ = "0.0.2"

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

from sys import argv, exit

try:
    from .ReverseShellServer import ReverseShellServer, main as reverse_shell_server
    from .ReverseShellClient import ReverseShellClient, main as reverse_shell_client
    from .ShellServer import ShellServer, main as shell_server
    from .ShellClient import ShellClient, main as shell_client
except ImportError:
    from ReverseShellServer import ReverseShellServer, main as reverse_shell_server
    from ReverseShellClient import ReverseShellClient, main as reverse_shell_client
    from ShellServer import ShellServer, main as shell_server
    from ShellClient import ShellClient, main as shell_client

def launch(function):
    del argv[1]
    function()
    exit(0)

if len(argv) > 1:
    if argv[1] == "ShellClient":
        launch(shell_client)
    elif argv[1] == "ShellServer":
        launch(shell_server)
    elif argv[1] == "ReverseShellClient":
        launch(reverse_shell_client)
    elif argv[1] == "ReverseShellServer":
        launch(reverse_shell_server)

print("USAGE: AsyncRemoteShell <Shell: ShellClient, ShellServer, ReverseShellClient, ReverseShellServer>")
exit(1)