#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implement 4 asynchronous tools to execute remote commands
#    Copyright (C) 2020, 2021  Maurice Lambert

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
    This file implement basic functions for Shell and ReverseShell.
"""

__all__ = [
    "special_command",
    "execute_command",
    "launch_asynchronous_commands",
    "parse_args",
]

from asyncio import create_subprocess_shell, gather
from asyncio.subprocess import PIPE
from os import device_encoding, chdir
from time import perf_counter
from sys import argv, exit
from typing import List, Tuple
import logging


async def special_command(commande: str) -> str:

    """
    This method execute "cd" or "chdir" command and "exit" command.
    Return str or None.
    """

    if commande.startswith("cd") or commande.startswith("chdir"):
        try:
            chdir(commande.split(maxsplit=1)[1])
            return ""
        except FileNotFoundError:
            return "Error with command : <cd>"
    elif commande.lower().startswith("exit"):
        return "exit"


async def execute_command(commande: str) -> str:

    """
    This method execute command and return output.
    """

    result = await special_command(commande)
    if result is not None:
        return result

    debut = perf_counter()
    process = await create_subprocess_shell(commande, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await process.communicate()

    result = f"Temps : {perf_counter() - debut}s\nReturn code : {process.returncode}\n"
    if stdout:
        result += f"[stdout]\n{stdout.decode(device_encoding(0))}\n"
    if stderr:
        result += f"[stderr]\n{stderr.decode(device_encoding(0))}\n"
    return result


async def launch_asynchronous_commands(commandes: str) -> List[str]:

    """
    This method parse commands and launch asynchronous execution.
    Return a list of commands output.
    """

    return await gather(
        *(execute_command(commande) for commande in commandes.split("&"))
    )


def parse_args(process_name: str) -> Tuple[str, int]:

    """
    This function parse arguments.
    Return a tuple with interface and port.
    """

    port = 45678
    host = "127.0.0.1"
    error = False

    for i, arg in enumerate(argv[1:]):
        if arg.startswith("--interface=") or arg.startswith("-i="):
            host = arg.split("=")[1]

        elif arg.startswith("--port=") or arg.startswith("-p="):
            port = arg.split("=", 1)[1]

            if port.isdigit():
                port = int(port)
            else:
                logging.error("port must be an integer.")
                error = True
        else:
            error = True

    if error:
        print(
            f"USAGE : {process_name} --interface=<interface name or adress"
            ", default : ''> --port=<port number, default : 45678>"
        )
        exit(1)

    return host, port
