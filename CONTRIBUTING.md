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

### Build the Rhino plug-in
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

## For VSCode extension
To build the the VSCode extension, you need to have VSCode installed on your machine. You can download it from [here](https://code.visualstudio.com/download).
Be sure that nodejs is installed on your machine. You can download it from [here](https://nodejs.org/en/download/).
Also `vsce` needs to be installed on your machine. You can install it by running the following command in the terminal.
```terminal
npm install -g vsce
```

### Build the VSCode extension
Checkout the folder containing the VSCode extension.
```terminal
cd .\VSCode\scriptsync\
```
Do modifications to the code and build the extension. The main file is `extension.ts` and additional info or variables can be found in `package.json`.
```terminal
vsce package
```
A new `.vsix` file is created in the folder. To test it, open VSCode and install the extension from the `.vsix` file. To do so, open the extensions panel, click on the three dots on the top right corner and select `Install from VSIX...`. Select the `.vsix` file and reload VSCode. Otherwise you can right-click the `.vsix` file and select `Install..`. Reload VSCode.