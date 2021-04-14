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
    This file implement a asynchronous ShellServer.
"""

__all__ = ["ShellServer"]

import asyncore
import os
import asynchat
from os import (
    getcwd,
    getlogin,
    cpu_count,
    get_exec_path,
    getenv,
)
from asyncio import run
import logging

try:
    from .commons import parse_args, launch_asynchronous_commands
except ImportError:
    from commons import parse_args, launch_asynchronous_commands


class Shell(asynchat.async_chat):

    """
    This class implement a Shell.
    """

    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self.set_terminator(b"\n")
        self.buffer = ""

    def collect_incoming_data(self, data):
        self.buffer += data.decode()

    def found_terminator(self):

        """
        This function parse commands and execute it or close connection.
        """

        if self.buffer:
            result = run(launch_asynchronous_commands(self.buffer))
            self.push("\n".join(result).encode())

            if "exit" in result:
                self.push(b"exit\n")
                logging.warning("Send exit message")
                self.close_when_done()

        else:
            self.get_banner()

        self.buffer = ""
        self.get_prompt()

    def get_banner(self):

        """
        This method add some banner informations.
        """

        path_exec = "\n\t".join(get_exec_path())
        self.push(
            f"OS name : {os.name}\nThe number of processor : {cpu_count()}"
            f"Execution path : \n\t{path_exec}".encode()
        )

    def get_prompt(self):

        """
        This method send the last line of the output to the client.
        """

        if os.name == "nt":
            self.push(f"\n{getlogin()}@{getenv('COMPUTERNAME')}-{getcwd()}>".encode())
        else:
            self.push(f"\n{getlogin()}@{getenv('COMPUTERNAME')}:{getcwd()}$".encode())

        self.push("\x00".encode())


class ShellServer(asyncore.dispatcher):

    """
    This class implement a simple asynchronous TCP server to launch Shell.
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.bind((host, port))
        self.listen(100)

    def handle_accept(self):

        """
        This method log a new connection and calls the Shell class.
        """

        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            logging.warning(f"{addr[0]}:{addr[1]} is connected...")
            Shell(sock)


def main() -> None:

    """
    This function get arguments and launch ShellServer.
    """

    logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s")

    host, port = parse_args("ShellServer")

    ShellServer(host, port)
    logging.warning(f"Server is running on tcp://{host}:{port}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logging.warning("Server is not running...")


if __name__ == "__main__":
    main()
