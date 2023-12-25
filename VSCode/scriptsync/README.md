<p align="center">
    <img src="https://raw.githubusercontent.com/ibois-epfl/script-sync/main/VSCode/scriptsync/logo/scriptsync_480.png" width="140">
</p>

# script-sync

This repository contains the code and Rhino plug-in to run C# and Python (IronPython or CPython) in RhinoV8.

![]([./vid/record_vid_gif20fps.gif](https://raw.githubusercontent.com/ibois-epfl/script-sync/main/VSCode/scriptsync/vid/record_vid_gif20fps.gif))

## Features
To start `script-sync` in RhinoV8, run the command `ScriptSyncStart` in RhinoV8. This will start a server that listens to commands from VSCode.

Open a `.py` or `.cs` file in VSCode and run it in RhinoV8 by pressing `F4`.
Add a `shebang` to the first line of the file to specify the Python interpreter to use, e.g.:
* `#!python3` to interpret it with CPython
* `#!python2` to interpret it with IronPython

To close `script-sync` in RhinoV8, run the command `ScriptSyncStop` in RhinoV8.

## Requirements
The plug-in needs to be installed on RhinoV8.

## Caveats
There is no intellisense for C# and Python in VSCode.

## Release Notes

### 1.0.0

First release of script-sync: it can run C# and Python (IronPython or CPython) in RhinoV8 from VSCode. It is only tested on Windows. 
* Extension for VSCode
* Rhino plug-in with basic commands to start/stop script-sync server
* basic documentation

## References

There are a lot of plug-ins that allow to run Python in Rhino. Among them, [CodeListener](https://github.com/ccc159/CodeListener) was working until RhinoV8 and it was a source of inspiration for this project. This is a simplified version, but it can run `C#` and both `IronPython` and `CPython` in RhinoV8.

## Citation
This project is part of the research activities of the [IBOIS lab](https://www.epfl.ch/labs/ibois/) at EPFL. It was developed by [Andrea Settimi](https://github.com/9and3).


## For more information

* [GitHub repo](https://github.com/ibois-epfl/script-sync)
* [IBOIS GitHub organization](https://github.com/ibois-epfl)
* [IBOIS lab page](https://www.epfl.ch/labs/ibois/)