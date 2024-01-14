// r "RhinoCodeEditor.dll"
// r "RhinoCodePluginGH.dll"

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using Eto.Drawing;
using Eto.Forms;
using GH_IO.Serialization;
using Grasshopper;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Parameters;
using Rhino.Geometry;
using Rhino.Runtime.Code;
using Rhino.Runtime.Code.Diagnostics;
using Rhino.Runtime.Code.Execution;
using Rhino.Runtime.Code.Execution.Debugging;
using Rhino.Runtime.Code.Execution.Profiling;
using Rhino.Runtime.Code.Languages;
using Rhino.Runtime.Code.Registry;
using Rhino.Runtime.Code.Storage;
using Rhino.UI;
using RhinoCodeEditor;
using RhinoCodeEditor.Extensions;
using RhinoCodeEditor.Themes;
using RhinoCodePlatform.Rhino3D.GH;
using RhinoCodePlatform.Rhino3D.GH1.Legacy;
using RhinoCodePlatform.Rhino3D.Languages;
using RhinoCodePluginGH;
using RhinoCodePluginGH.Components;
using RhinoCodePluginGH.Controls;
using RhinoCodePluginGH.Parameters;
using RhinoCodePluginGH.Types;

using RhinoCodePluginGH.Components;
using RhinoCodePluginGH.Parameters;

a = 1;
Console.Write("C# Runtime: \n");

var scriptComponent = new ScriptComponent();

scriptComponent.Tooltip = "This is a tooltip";

Console.Write(scriptComponent);

// var scriptComp = ScriptComponent();

// // Console.Write(scriptComp);

// // use the component DeconstructPlane
// // to get the plane's origin and normal
// var func_info = Rhino.NodeInCode.Components.FindComponent("ScriptComponent");
// Console.Write(func_info);