// Grasshopper Script Instance
using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;

using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

using Python.Runtime;
using System;

public class Script_Instance : GH_ScriptInstance
{
    // ...

    private void RunScript(object x, object y, out object a)
    {
        using (Py.GIL()) // acquire the Python GIL (Global Interpreter Lock)
        {
            dynamic np = Py.Import("numpy"); // import the numpy module
            dynamic sin = np.sin; // get the sin function from numpy

            double result = (double)sin(5.0); // call the sin function with an argument
            a = result; // assign the result to the output parameter
        }
    }
}