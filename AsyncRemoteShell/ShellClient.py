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
    This file implement a asynchronous ShellClient.
"""

__all__ = ["ShellClient"]

from time import sleep
import asynchat
import asyncore
import logging

try:
    from .commons import parse_args
except ImportError:
    from commons import parse_args


class ShellClient(asynchat.async_chat):

    """
    This class implement a Shell Client.
    """

    def __init__(self, host: str, port: int):
        asynchat.async_chat.__init__(self)
        self.create_socket()
        self.connect((host, port))

        self.set_terminator(b"\x00")
        self.buffer = ""
        self.push(b"\n")

    def collect_incoming_data(self, data: bytes) -> None:

        """
        Get shell output and exit if ShellServer send exit message.
        """

        self.buffer += data.decode()

        if "\nexit\n" in self.buffer or self.buffer.startswith("exit"):
            logging.warning("Get exit message.")
            self.close_when_done()

    def found_terminator(self) -> None:

        """
        Print shell output, ask new command and send it.
        """

        command = input(self.buffer)
        while not command:
            command = input(self.buffer.split("\n")[-1])
        command += "\n"
        self.push(command.encode())
        self.buffer = ""


def main():

    """
    This function get arguments and launch ShellClient.
    """

    logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s")

    host, port = parse_args("ShellClient")

    logging.warning("ShellClient is running...")

    while True:
        try:
            shell = ShellClient(host, port)
            asyncore.loop()
            sleep(10)
        except KeyboardInterrupt:
            shell.push(b"exit\n")
            shell.close_when_done()
            break

    logging.warning("ShellClient is not running.")


if __name__ == "__main__":
    main()
