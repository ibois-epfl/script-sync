using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

using System.Reflection;

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
    private string _scriptSyncPath = @"F:\script-sync\CsGH\test\cpy_version.py";

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
      base.UsingScriptInputParam = true;
      base.UsingLibraryInputParam = true;
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

    protected override void BeforeSolveInstance()
    {
      // add a panel component to input parameters

      // foreach (IGH_Param param in Params.Input)
      // {
      //   Rhino.RhinoApp.WriteLine(param.NickName);
      // }

      // create a GH_Structure with the private member _scriptSyncPath
      // Grasshopper.Kernel.Data.GH_Structure<Grasshopper.Kernel.Types.GH_String> scriptSyncPath = new Grasshopper.Kernel.Data.GH_Structure<Grasshopper.Kernel.Types.GH_String>();
      // scriptSyncPath.Append(new Grasshopper.Kernel.Types.GH_String(_scriptSyncPath));







      
      // set to script input parameter the value of the script path
      // check the "Input as Path" menu item for the script input parameter

      base.BeforeSolveInstance();

      // Params.Input[0].ClearData();
      // Params.Input[0].AddVolatileData(new Grasshopper.Kernel.Data.GH_Path(0), 0, _scriptSyncPath);

      // // print all the input parameters values
      // Rhino.RhinoApp.WriteLine(Params.Input[0].NickName);
      // Rhino.RhinoApp.WriteLine(Params.Input[0].VolatileData.ToString());
      // Rhino.RhinoApp.WriteLine(Params.Input[0].VolatileData.PathCount.ToString());
      // Rhino.RhinoApp.WriteLine(Params.Input[0].VolatileData.get_Branch(0).ToString());
      // Rhino.RhinoApp.WriteLine(Params.Input[0].VolatileData.get_Branch(0)[0].ToString());


    }

    protected override void AfterSolveInstance()
    {


      // hide the first input parameter
      // Params.UnregisterInputParameter(Params.Input[0], true);

      base.AfterSolveInstance();
    }

    /// <summary>
    /// This is the method that actually does the work.
    /// </summary>
    /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
    /// to store data in output parameters.</param>
    protected override void SolveInstance(IGH_DataAccess DA)
    {

      Rhino.RhinoApp.WriteLine(">>>>>>>>>>SolveInstance");
      string testPrint = "";
      DA.GetData(0, ref testPrint);
      Rhino.RhinoApp.WriteLine(testPrint);


      // add source to the script input parameter
      // check the "Input as Path" menu item for the script input parameter
      // DA.SetData(0, _scriptSyncPath);

      // Params.Input[0].AddSource(_scriptSyncPath);

      base.SolveInstance(DA);
    }

    protected override void AppendAdditionalComponentMenuItems(ToolStripDropDown menu)
    {
      // Call empty to avoid Shift+LeftClick menu
      // base.AppendAdditionalComponentMenuItems(menu);
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