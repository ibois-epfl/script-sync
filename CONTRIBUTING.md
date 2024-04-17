# Contribution guideline
All contributions are more than welcome. Follow these guidelines below and open a new pull request.

Script-sync is a Rhino plug-in and a VSCode extension. The Rhino plug-in is written in C# and the VSCode extension is written in TypeScript.
Depending on which part of the code you want to contribute to, follow the instructions below. The following sections are for Windows11, RhinoV8 and VSCode.

In either case clone the repository on your machine.

```terminal
git clone https://github.com/ibois-epfl/script-sync.git
```

## For Rhino plug-in
To build the Rhino plug-in, you need to have RhinoV8 installed on your machine. You can download it from [here](https://www.rhino3d.com/download/rhino-for-windows/8/latest).
Be sure that dotnet is installed on your machine. You can download it from [here](https://dotnet.microsoft.com/download/dotnet/5.0).

Checkout the folder containing the Rhino plug-in.
```terminal
cd .\CsRhino\
```
Do modifications to the code and build the plug-in.
```terminal
dotnet build
```
The plug-in is built in the folder `.\CsRhino\bin\`.
To test it remove all versions of the plug-in from RhinoV8 and drag-and-drop the `.rhp` file in RhinoV8. No need to redo it after each build, it will be updated if you close and reopen RhinoV8.

## Build the VSCode extension
Run the python invoke:
```terminal
invoke vscerize
```
The `.vsix` file is created in `VSCode/scriptsync/`. You can install it in VSCode by dragging-and-dropping it in the Extensions panel.

## Build the YAK package
Be sure to update the correct number version in the `manifest.yml` file in root.
Next call the python task:
```terminal
invoke yakerize
```
This will create a `.yak` file in the root folder. You can install it in RhinoV8 by dragging-and-dropping it in RhinoV8.

## Release
The `.yak` and `.vsix` will be generated and published online when a release is created on GitHub. The version number is the same as the one in the `manifest.yml` file.
