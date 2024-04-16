# Guide for releasing a new version of the package (for code maintainers)

---
## For Rhino plug-in
Script-sync is released as a `.yak` package via the Yak executable provided by McNeel.

### Build the Rhino plug-in
Start by building the Rhino plug-in as described in the [contribution guideline](#contribution-guideline). OR, grab the latest version of the plug-in from the artifacts of the latest successful build on the latest e.g., [CI](https://github.com/ibois-epfl/script-sync/actions/runs/7349030258).

### Create the `.yak` package
Create a folder with the following structure:
```
script_sync-1.0.2-rh8-win/
├───logo.png  <--64x64px
├───ScriptSync.rhp
├───<all necessary .dll files>
├───manifest.yml
└───misc/
    ├───LICENSE.md
    └───README.md
```
The `manifest.yml` file should look like this:
```yml
name: script-sync
version: 1.**1**.0
authors:
  - Andrea Settimi
description: Script-sync is a Rhino plug-in to run C# and Python (IronPython or CPython) in RhinoV8 and Grasshopper.
url: https://github.com/ibois-epfl/script-sync
keywords:
  - Rhino
  - Cs
  - Python
  - IronPython
  - CPython
  - VScode
  - Utility
icon: logo.png
```
Now, create the `.yak` package by running the following command in the terminal:
```terminal
yak build
```
The `.yak` package is created in the folder `script_sync-1.0.2-rh8-win.yak`.

### Publish the `.yak` package to the Yak server

To upload the package to the Yak server, run the following command in the terminal:
```terminal
yak login
yak push script_sync-1.0.2-rh8-win.yak
```
---

## For VSCode extension
Script-sync is released as a `.vsix` package via the VSCE executable provided by Microsoft.

### Build the VSCode extension
Start by building the VSCode extension as described in the [contribution guideline](#contribution-guideline). OR, grab the latest version of the extension from the artifacts of the latest successful build on the latest e.g., [CI](https://github.com/ibois-epfl/script-sync/actions/runs/7349030262).

Make sure to change the correct version number in the `package.json` file.
```json
  "version": "1.1.4",
  "engines": {
    "vscode": "^1.85.0"
  },
```

### Publish the `.vsix` package to the VSCode marketplace
To upload the package to the VSCode marketplace, run the following command in the terminal in the folder containing the `.vsix` file:
```terminal
vsce login ibois-epfl
vsce publish
```


