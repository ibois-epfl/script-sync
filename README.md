<p align="center">
    <img src="VSCode\scriptsync\logo\scriptsync_480.png" width="140">
</p>

<p align="center">
    <img src="https://github.com/ibois-epfl/script-sync/actions/workflows/rhinoplugin.yml/badge.svg">
    <img src="https://github.com/ibois-epfl/script-sync/actions/workflows/vscodeext.yml/badge.svg">
</p>

# script-sync

Rhino/VSCode plug-in to run C# and Python (IronPython or CPython) scripts directly from VSCode. 

![record_vid_gif20fps](https://github.com/ibois-epfl/script-sync/assets/50238678/7ccb2aa5-e646-45cd-9657-95776d24a48a)


## Installation
Install script-sync rhino from food4rhino or the packageManager in Rhino (name: "script-sync").
Install script-syncVSCode extention from the VSCode extension marketplace (name: "script-sync")

## How to use
To start `script-sync` in RhinoV8, run the command `ScriptSyncStart` in RhinoV8. This will start a server that listens to commands from VSCode.

Open a `.py` or `.cs` file in VSCode and run it in RhinoV8 by pressing `F4`.
Add a `shebang` to the first line of the file to specify the Python interpreter to use, e.g.:
* `#! python3` to interpret it with CPython
* `#! python2` to interpret it with IronPython

To close `script-sync` in RhinoV8, run the command `ScriptSyncStop` in RhinoV8.

## Requirements
The plug-in needs to be installed on RhinoV8.

## Caveats
There is no intellisense for C# and Python in VSCode.

## Issues
For bugs open an issue on the [GitHub repo](https://github.com/ibois-epfl/script-sync/issues).

## Contribution
All contributions are welcome. Have a look at the [contribution guidelines](CONTRIBUTING.md).

## References

There are a lot of plug-ins that allow to run Python in Rhino. Among them, [CodeListener](https://github.com/ccc159/CodeListener) was working until RhinoV8 and it was a source of inspiration for this project. This is a simplified version, but it can run `C#` and both `IronPython` and `CPython` in RhinoV8.

## Citation
This project is part of the research activities of the [IBOIS lab](https://www.epfl.ch/labs/ibois/) at EPFL. It was developed by [Andrea Settimi](https://github.com/9and3).

## For more information

* [GitHub repo](https://github.com/ibois-epfl/script-sync)
* [IBOIS GitHub organization](https://github.com/ibois-epfl)
* [IBOIS lab page](https://www.epfl.ch/labs/ibois/)

# For code maintainers
Follow the instructions in [RELEASE.md](RELEASE.md) to release a new version of the package.

## Roadmap
- [x] publish yak package + auto pipeline
- [x] publish on tools website lab
- [x] add instructions for dev and contribution
- [x] write ci
- [ ] write tests
- [ ] ci action to publish automatic releases
- [ ] possibly redirect output from RhinoApp.RunScript() to vscode consoles or log file
- [ ] add intellisense for C# and Python Rhino in vscode
