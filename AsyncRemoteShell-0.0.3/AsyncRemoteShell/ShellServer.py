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
    This module implement the class named ShellServer.
"""

import asyncore
import os
import asynchat
from os import (
    getcwd,
    chdir,
    getlogin,
    cpu_count,
    get_exec_path,
    getenv,
    device_encoding,
)
from asyncio import create_subprocess_shell, run, gather
from asyncio.subprocess import PIPE
from time import perf_counter

__all__ = ["ShellServer"]


class Shell(asynchat.async_chat):
    """
    This class get, parse and execute the command sent by the
    client and return the output to the client.
    """

    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self.set_terminator(b"\n")
        self.buffer = ""

    def collect_incoming_data(self, data):
        self.buffer += data.decode()

    def found_terminator(self):
        """
        This method parse the command, call the execution methods
        and and send the output to the client.
        """
        if self.buffer:
            result = run(asynch(self.buffer))
            self.push("\n".join(result).encode())

            if "exit" in result:
                self.close_when_done()
        else:
            self.get_first_buffer()
        self.buffer = ""
        self.get_buffer_end()

    def get_first_buffer(self):
        """
        This method send some informations in the first time.
        """
        path_exec = "\n\t".join(get_exec_path())
        self.push(
            f"OS name : {os.name}\nThe number of processor : {cpu_count()}"
            f"Execution path : \n\t{path_exec}".encode()
        )

    def get_buffer_end(self):
        """
        This method send the last line of the output to the client.
        """
        if os.name == "nt":
            self.push(
                f"\n{getlogin()}@{getenv('COMPUTERNAME')}-{getcwd()}>".encode()
            )
        else:
            self.push(
                f"\n{getlogin()}@{getenv('COMPUTERNAME')}:{getcwd()}$".encode()
            )
        self.push("\r\x00\r\x00".encode())


class ShellServer(asyncore.dispatcher):
    """
    The TCP server that created the socket and call the Shell class.
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.bind((host, port))
        self.listen(100)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print(f"{addr[0]}:{addr[1]} is connected...")
            Shell(sock)


async def special_command(commande):
    """
    This method execute one command with "special" execution.
    The command "cd" and "exit" are implemented here.
    """
    if commande.startswith("cd") or commande.startswith("chdir"):
        try:
            chdir(" ".join(commande.split()[1:]))
        except FileNotFoundError:
            return "Error with command : <cd>"
    elif commande.lower().startswith("exit"):
        return "exit"


async def exec_(commande):
    """
    This method execute one command and return the output.
    """
    result = await special_command(commande)
    if result:
        return result

    debut = perf_counter()
    process = await create_subprocess_shell(commande, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await process.communicate()

    result = f"Time : {perf_counter() - debut}s\nError code : {process.returncode}\n"
    if stdout:
        result += f"[stdout]\n{stdout.decode(device_encoding(0))}\n"
    if stderr:
        result += f"[stderr]\n{stderr.decode(device_encoding(0))}\n"
    return result


async def asynch(commandes):
    """
    This method parse the command and call the execution method.
    She return a list of output.
    """
    return await gather(*(exec_(commande) for commande in commandes.split(" & ")))


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
            "USAGE : ShellServer --interface=<interface name or adress, default : "
            "''> --port=<port number, default : 45678>"
        )

    ShellServer(host, port)
    print(f"Server is running on tcp://{host}:{port}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("Server is not running...")


if __name__ == "__main__":
    main()
