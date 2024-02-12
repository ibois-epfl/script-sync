:: This batch file is a shortcut to the prepare the release packages of script-sync.
:: It does the following:

:: a) it takes as asrgument the number of the version
:: b) it modifies all the files where the version number is present
:: c) it builds the RhinoProject
:: d) it builds the GHPlugin
:: e) it creates the yak package
:: e) it builds the vscode extension

:: f*) it updates the vscode extension in the marketplace
:: g*) it updates the yak package in the yak manager

:: h) it put in a folder all the files needed for the release (yak+vsce)