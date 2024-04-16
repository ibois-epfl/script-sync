#! python3

"""
    This script sync the vsce version with the yak version indicated in manifest.yml
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