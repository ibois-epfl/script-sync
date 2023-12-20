using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

namespace ScriptSync
{
    [Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)]
    public class ScriptSyncCommand : Command
    {
        public ScriptSyncCommand()
        {
            Instance = this;
        }

        public static ScriptSyncCommand Instance { get; private set; }

        public override string EnglishName => "ScriptSyncCommand";

        protected override Rhino.Commands.Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            string pyFile = @"F:\pysync\pyversion.py";
            RhinoApp.InvokeOnUiThread(new Action(() => {
                RhinoApp.WriteLine("Result: {0}", RhinoApp.RunScript("_-RunPythonScript " + pyFile, true));
            }));
            return Rhino.Commands.Result.Success;
        }
    }
}
