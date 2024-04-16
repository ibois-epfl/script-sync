#! python3

"""
    This script collects all the files needed to create the yak package.
"""

from invoke import run
import os


# Run a command just like you would in the shell
result = run("dir", hide=True, warn=True)

# You can check if the command was successful
if result.ok:
    # print it in green
    print("\033[92mCommand succeeded\033[0m")
else:
    print("\033[91mCommand failed\033[0m")

# print(secret)
# # You can access the output of the command
# print("Command output was:")
# print(result.stdout)

############################################

path_rhldir : str = "./"

# copy the yaker directory to the build folder
result = run("cd yaker", hide=True, warn=True)
# result = run("cd", hide=False, warn=True)

# get the rhino .rhp and its dependencies
