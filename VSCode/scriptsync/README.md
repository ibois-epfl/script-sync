<p align="center">
    <img src="./logo/scriptsync_480.png" width="140">
</p>

# script-sync

This repository contains the code and Rhino plug-in to run C# and Python (IronPython or CPython) in RhinoV8.

<--- ADD GIF Cpython box --->
<--- ADD GIF Ironpython box --->
<--- ADD GIF C# to add box --->

## Features

Open a `.py` or `.cs` file in VSCode and run it in RhinoV8 by pressing `F4`.
Add a `shebang` to the first line of the file to specify the Python interpreter to use, e.g.:
* `#!python3` to use CPython
* `#!python2` to use CPython

## Requirements

This extension works only with RhinoV8 and it is only tested on Windows.

## Release Notes

### 1.0.0

First release of script-sync: it can run C# and Python (IronPython or CPython) in RhinoV8 from VSCode. It is only tested on Windows. 
* Extension for VSCode
* `Net` Rhino plug-in
* basic documentation

## References

There are a lot of plug-ins that allow to run Python in Rhino. Among them, [CodeListener](https://github.com/ccc159/CodeListener) was working until RhinoV8 and it was a source of inspiration for this project. This is a simplified version, but it can run `C#` and both `IronPython` and `CPython` in RhinoV8.

## Citation
This project is part of the research activities of the [IBOIS lab](https://www.epfl.ch/labs/ibois/) at EPFL. It was developed by [Andrea Settimi](https://github.com/9and3).


## For more information

* [GitHub repo](https://github.com/ibois-epfl/script-sync)
* [IBOIS GitHub organization](https://github.com/ibois-epfl)
* [IBOIS lab page](https://www.epfl.ch/labs/ibois/)