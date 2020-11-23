from setuptools import setup, find_packages
import AsyncRemoteShell

setup(
    name = 'AsyncRemoteShell',
 
    version = AsyncRemoteShell.__version__,
    packages = find_packages(),

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = """
	This package implement 4 asynchronous tools to execute remote commands :
		- One ReverseShellClient
		- One ReverseShellServer
		- One ShellServer
		- One ShellClient
""",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/Asynchronous-Remote-Shell',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
        "Topic :: System :: Shells",
        "Topic :: System :: Networking"
    ],
 
    entry_points = {
        'console_scripts': [
            'ShellClient = AsyncRemoteShell:shell_client',
            'ShellServer = AsyncRemoteShell:shell_server',
            'ReverseShellClient = AsyncRemoteShell:reverse_shell_client',
            'ReverseShellServer = AsyncRemoteShell:reverse_shell_server',
        ],
    },
    python_requires='>=3.6',
)