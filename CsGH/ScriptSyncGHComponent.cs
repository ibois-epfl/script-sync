using System;
using System.Collections.Generic;
using System.Drawing;

using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;

using RhinoCodePluginGH;
using RhinoCodePluginGH.Components;
using RhinoCodePluginGH.Parameters;


namespace ScriptSyncGH
{
  public class ScriptSyncGHComponent : BaseScriptComponent<ScriptParam, ScriptLibraryParam>
  {
    /// <summary>
    /// Each implementation of GH_Component must provide a public 
    /// constructor without any arguments.
    /// Category represents the Tab in which the component will appear, 
    /// Subcategory the panel. If you use non-existing tab or panel names, 
    /// new tabs/panels will automatically be created.
    /// </summary>
    public ScriptSyncGHComponent()
    : base("77dc9957-c958-45b0-b9d2-6d1437ee8d8a", "ScriptSyncComponent", "ScriptSyncTest", "ST", "ScriptSync component", "ScriptSync", "Script")
      // : base("ScriptSyncComponent", "SC",
      //   "Test component",
      //   "script-sync", "Default")
    {
    }

    /// <summary>
    /// Registers all the input parameters for this component.
    /// </summary>
    protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
    {
      pManager.AddParameter(CreateParameter(GH_ParameterSide.Input, pManager.ParamCount));
      pManager.AddParameter(CreateParameter(GH_ParameterSide.Input, pManager.ParamCount));

      // add a component message
      // Message = "ScriptSyncComponent";
      this.Message = "ScriptSyncComponent";
    }

    /// <summary>
    /// Registers all the output parameters for this component.
    /// </summary>
    protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
    {
      pManager.RegisterParam(CreateParameter(GH_ParameterSide.Output, pManager.ParamCount));
      UsingStandardOutputParam = true;
    }

    /// <summary>
    /// This is the method that actually does the work.
    /// </summary>
    /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
    /// to store data in output parameters.</param>
    protected override void SolveInstance(IGH_DataAccess DA)
    {
      base.SolveInstance(DA);
    }

    /// <summary>
    /// Provides an Icon for every component that will be visible in the User Interface.
    /// Icons need to be 24x24 pixels.
    /// You can add image files to your project resources and access them like this:
    /// return Resources.IconForThisComponent;
    /// </summary>
    protected override System.Drawing.Bitmap Icon => null;

    /// <summary>
    /// Each component must have a unique Guid to identify it. 
    /// It is vital this Guid doesn't change otherwise old ghx files 
    /// that use the old ID will partially fail during loading.
    /// </summary>
    public override Guid ComponentGuid => new Guid("B6DC1B5D-F487-4330-941B-3B06A38ABD09");
  }
}