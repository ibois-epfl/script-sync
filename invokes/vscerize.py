#! python3

"""
    This script generate the vsce package.
"""

from invoke import run
import os
import sys
import shutil


def main() -> None:
    # the  vsce extension project
    vsceproject_dir : str = "./VSCode/scriptsync"
    # the json settings file for the VSCE extention
    json_settings_path : str = "./VSCode/scriptsync/package.json"
    # the yak manifest from which we get the version
    manifest_path : str = "./manifest.yml"

    # update version number from the manifest file
    version : str = ""
    with open(manifest_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "version" in line:
                version = line.split(":")[1].strip()
    print(f"Script-sync yak Version: {version}")

    with open(json_settings_path, "r") as file:
        lines = file.readlines()
        new_lines = []
        for i, line in enumerate(lines):
            if "version" in line:
                new_lines.append(f'  "version": "{version}",\n')
            else:
                new_lines.append(line)
    with open(json_settings_path, "w") as file:
        file.writelines(new_lines)
    print("Updated the version number in the package.json file.")

    # check npm/vsce is installed
    res = run("npm -v", hide=True, warn=True)
    if res.failed:
        res = run("npm install -g npm", hide=False, warn=True)
        if res.failed:
            print("Failed to install npm.")
            sys.exit(1)
        print("npm installed successfully.")
    res = run("npm list -g --depth=0", hide=True, warn=True)
    if "vsce" not in res.stdout:
        print("vsce is not installed. Installing vsce...")
        res = run("npm install -g vsce", hide=False, warn=True)
        if res.failed:
            print("Failed to install vsce.")
            sys.exit(1)
        print("vsce installed successfully.")
    else:
        print("vsce is installed.")

    # build the package
    path_current : str = os.getcwd()
    os.chdir(vsceproject_dir)
    res = run("vsce package", hide=False, warn=True)
    if res.failed:
        print(f"Failed to build the package: {res.stderr}")
        sys.exit(1)
    print(f"Package built successfully in {vsceproject_dir}.")
    os.chdir(path_current)


if __name__ == "__main__":
    main()