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
    This module implement the ReverseShellServer.
"""

import asyncore

__all__ = ["ReverseShellServer"]


class ReverseShell(asyncore.dispatcher_with_send):
    """
    This class print informations send by the client and ask the 
    command to the user.
    """

    def handle_read(self):
        """
        This method print informations send by the client and 
        ask the command to the user.
        """
        data = self.recv(65535).decode()
        command = input(data)
        while not command:
            command = input(data.split("\n")[-1])
        self.send(command.encode())


class ReverseShellServer(asyncore.dispatcher):
    """
    This class implement a simple asynchronous TCP server 
    to create the socket to communicate with the client.
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(100)

    def handle_accepted(self, sock, addr):
        """
        This method call the ReverseShell.
        """
        print(f"{addr[0]}:{addr[1]} is connected...")
        ReverseShell(sock)


def main():
    from sys import argv

    port = 45678
    host = ""
    argv_number = 0

    for arg in argv:
        if arg.startswith("--interface=") or arg.startswith("-i="):
            host = arg.split("=")[1]
            argv_number += 1
        elif arg.startswith("--port=") or arg.startswith("-p="):
            try:
                port = int(arg.split("=")[1])
            except ValueError:
                print("ERROR : port must be an integer.")
            else:
                argv_number += 1

    if len(argv) - argv_number > 1:
        print(
            "USAGE : ReverseShellServer --interface=<interface name or adress,"
            " default : ''> --port=<port number, default : 45678>"
        )

    ReverseShellServer(host, port)
    print(f"Server is running on tcp://{host}:{port}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("Server is not running...")


if __name__ == "__main__":
    main()
