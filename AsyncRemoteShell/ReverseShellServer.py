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
    This file implement a asynchronous ReverseShellServer.
"""

__all__ = ["ReverseShellServer"]

from typing import Tuple
import asyncore
import socket
import logging

try:
    from .commons import parse_args
except ImportError:
    from commons import parse_args


class ReverseShell(asyncore.dispatcher_with_send):

    """
    This class implement a ReverseShell.
    """

    def handle_read(self) -> None:

        """
        This function retrieves data from a connected ReverseShellClient,
        ask a new command and sends it.
        """

        data = self.recv(65535).decode()

        if "exit" in data.split("\n"):
            logging.warning("Client send exit message.")
            self.close()
        else:
            command = input(data)
            while not command:
                command = input(data.split("\n")[-1])
            self.send(command.encode())


class ReverseShellServer(asyncore.dispatcher):

    """
    This class implement a simple asynchronous TCP server to launch ReverseShell.
    """

    def __init__(self, host: str, port: int):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(100)

    def handle_accepted(self, sock: socket.socket, addr: Tuple[str, int]) -> None:

        """
        This method log a new connection and calls the ReverseShell class.
        """

        logging.warning(f"{addr[0]}:{addr[1]} is connected...")
        ReverseShell(sock)


def main() -> None:

    """
    This function get arguments and launch ReverseShellServer.
    """

    logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s")

    host, port = parse_args("ShellServer")

    ReverseShellServer(host, port)
    logging.warning(f"Server is running on tcp://{host}:{port}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        logging.warning("Server is not running.")


if __name__ == "__main__":
    main()
