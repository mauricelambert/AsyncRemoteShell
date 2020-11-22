# AsyncRemoteShell

## Description
This package implement 4 tools for asynchronous remote commands :
- ReverseShellClient
- ReverseShellServer
- ShellClient
- ShellServer

The ReverseShellServer open one socket, wait the ReverseShellClient connection, ask commands to the user and print the output.
The ReverseShellClient initialize the connection with the ReverseShellServer, wait the ReverseShellServer response, execute commands and send the output.

The ShellServer open one socket, wait the ShellClient connection, execute commands and send the output.
The ShellClient initialize the connection with the ShellServer, ask commands to the user and print the output.

## Requirements
This package require :
- python 3
- python3 Standard Library

## Installation
```
pip install AsyncRemoteShell
```

## Examples
With System Terminal/System Console :
- ` ReverseShellClient --interface=127.0.0.1 --port=45678 `
- ` ReverseShellServer -i=localhost -p=45678 `
- ` ShellClient 10.0.0.2 56789 `
- ` ShellServer --interface= -p=56789 `

With python 3 :
- ReverseShellClient : 
```python
from AsyncRemoteShell import ReverseShellClient
import asyncore
ReverseShellClient("10.0.0.2", 45678) # host and port is required
asyncore.loop()
```
- ReverseShellServer : 
```python
from AsyncRemoteShell import ReverseShellServer
import asyncore
ReverseShellServer("", 45678) # interface and port is required
asyncore.loop()
```
- ShellClient : 
```python 
from AsyncRemoteShell import ShellClient
import asyncore
ShellClient("10.0.0.2", 45678) # host and port is required
asyncore.loop()
```
- ShellServer : 
```python 
from AsyncRemoteShell import ShellServer
import asyncore
ShellServer("", 45678) # interface and port is required
asyncore.loop()
```

## Why Asynchronous Shell
You can install this package on Windows and execute this script :
```python
from time import perf_counter
from os import system
t1 = perf_counter(); system('powershell -c "Get-PSDrive" & netstat & systeminfo'); t2 = perf_counter()
print(f"Execution time : {t2 - t1} s")
```

After that launch this asynchronous shell, launch this command : ` powershell -c "Get-PSDrive" & netstat & systeminfo ` and compare the execution time.

## Link
[AsyncRemoteShell Github Page](https://github.com/mauricelambert/Asynchronous-Remote-Shell)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
