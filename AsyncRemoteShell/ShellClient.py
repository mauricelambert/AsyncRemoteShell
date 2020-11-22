#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module implement the ShellClient class.
"""

import asynchat
import asyncore

__all__ = ["ShellClient"]


class ShellClient(asynchat.async_chat):
    """
    This class is a client that allows you to send commands to the server.
    """

    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket()
        self.connect((host, port))

        self.set_terminator(b"\r\x00\r\x00")
        self.buffer = ""
        self.push(b"\n")

    def collect_incoming_data(self, data):
        self.buffer += data.decode()

    def found_terminator(self):
        """
        This function ask you the command to send on the server.
        """
        command = input(self.buffer)
        while not command:
            command = input(self.buffer.split("\n")[-1])
        command += "\n"
        self.push(command.encode())
        self.buffer = ""

        for c in command.split(" & "):
            if c.startswith("exit"):
                self.close_when_done()


def main():
    from sys import argv

    if len(argv) != 3:
        print("USAGE : ShellClient <ip or hostname server> <port server : int>")
        exit(1)

    try:
        port = int(argv[2])
    except ValueError:
        print("USAGE : ShellClient <ip or hostname server> <port server>")
        exit(1)

    ShellClient(argv[1], port)
    print("ShellClient is running...\nPlease wait the server response...")
    asyncore.loop()


if __name__ == "__main__":
    main()
