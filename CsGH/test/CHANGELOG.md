# notes for changes
List of features to implement in ScriptSyncGH:

- We can do that the active file in the editor is highlighted as purple in the ghcomponent AND it is the only one that prints the "out" variables in the vscode "output" tab.
OR
- the component select always the active file in the editor as the file to run, and it runs (aka recompute the component solution on F4 or another key) ----> in this case there will always be ONLE 1 component in the canvas (we need to make sure that we cannot have more).

- ALTERNATIVE: we call the script component "ScriptComponent" and pass parameters.

## resources

- "Can I invoke Python script when develo p GH component with C# ..." : https://discourse.mcneel.com/t/can-i-invoke-python-script-when-develop-gh-component-with-c-and-vsstudio/129425/5

## to notify once done

- https://discourse.mcneel.com/t/rhino-8-how-to-use-input-code-in-grasshopper-script-component/169547/6