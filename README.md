<p align="center">
    <img src="VSCode\scriptsync\logo\scriptsync_480.png" width="140">
</p>

<p align="center">
    <img src="https://github.com/ibois-epfl/script-sync/actions/workflows/rhinoplugin.yml/badge.svg">
    <img src="https://github.com/ibois-epfl/script-sync/actions/workflows/ghuserbuild.yml/badge.svg">
    <img src="https://github.com/ibois-epfl/script-sync/actions/workflows/vscodeext.yml/badge.svg">
</p>

# script-sync

**What is it?** Script-sync plug-in to run C# and Python (IronPython or CPython) scripts directly from VSCode into Rhino and Grasshopper. This project is a research utility from the [IBOIS lab](https://www.epfl.ch/labs/ibois/) at EPFL. It was developed and currently maintained by [Andrea Settimi](https://github.com/9and3).

**Why Script-sync?** Although Rhino8 has a wonderful IDE, we often miss the nice extensions and functions of a full-fledged IDE like VSCode. Script-sync allows you to run your scripts directly from VSCode, while keeping the Rhino/Grasshopper environment open. This is particularly useful if you have *AI-assisted* (e.g. GithubCoPilot) code completion.

You can execute the folloing languages from VSCode with script-sync:

|               | CPython | IronPython  | C# |
| ------------- | ------  | ----------- | -- |
| Rhino         | ✅      | ✅          | ✅|
| Grasshopper   | ✅      |             |    |



<br>

<p float="left">
  <figure>
    <img src="https://github.com/ibois-epfl/script-sync/assets/50238678/7ccb2aa5-e646-45cd-9657-95776d24a48a" width="100%" />
    <figcaption><i>Script-sync in Rhino</i></figcaption>
  </figure>

  <figure>
    <img src="https://github.com/ibois-epfl/script-sync/blob/main/GH/PyGH/assets/vid/scriptsync_gh.gif?raw=true" width="100%" />
    <figcaption><i>Script-sync in Grasshopper</i></figcaption>
  </figure>
</p>


## Installation
🦏/🦗 **`Rhino/Grasshopper`**: Install script-sync rhino from food4rhino or the packageManager in Rhino (name: "script-sync"). For Grasshopper you might want to get rid of the old version of the plugin before installing the new one. Just right-click on the old icon and click *delete*.

👩‍💻 **`VScode`**: Install script-syncVSCode extension from the VSCode extension marketplace (name: "script-sync")

## How to use
🦏 **`Rhino`**: To start `script-sync` in RhinoV8, run the command `ScriptSyncStart` in RhinoV8. This will start a server that listens to commands from VSCode.
To close `script-sync` in RhinoV8, run the command `ScriptSyncStop` in RhinoV8.

🦗 **`Grasshopper`**: To start `script-sync` in Grasshopper, add the component script-sync:

<figure align="center">
    <img src="https://github.com/ibois-epfl/script-sync/blob/main/GH/PyGH/assets/img/single_comp.png?raw=true" width="550">
    <figcaption><i>Script-sync in Grasshopper: 
        <li><code>btn</code>: click to open a file explorer and connect a script</li>
        <li><code>x</code>: classical input parameter, you can add more</li>
        <li><code>stdout</code>: all errors and print() is deviated here</li>
        <li><code>a</code>: classical output parameter, you can add more</li>
    </i></figcaption>
</figure>

👩‍💻 **`VScode`**: Open a script in VSCode and run it in RhinoV8 by pressing `F4` to run in Rhino or `shift+F4` for Grasshopper.
For Python files, add a `shebang` to the first line of the file to specify the interpreter to use, e.g.:
* `#! python3` to interpret it with CPython
* ⚠️ `#! python2` to interpret it with IronPython (only in Rhino)

## Requirements
The plug-in needs to be installed on RhinoV8, Grasshopper and VSCode

## Caveats
There is no intellisense for C# and Python in VSCode. In addi

## Issues
For bugs open an issue on the [GitHub repo](https://github.com/ibois-epfl/script-sync/issues).

## Contribution
All contributions are welcome. Have a look at the [contribution guidelines](CONTRIBUTING.md).

## References
There are a lot of plug-ins that allow to run Python in Rhino. Among them, [CodeListener](https://github.com/ccc159/CodeListener) was working until RhinoV8 and it was a source of inspiration for this project. This is a simplified version, but it can run `C#` and both `IronPython` and `CPython` in RhinoV8.

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
- [ ] (optional) add C# support for Grasshopper
