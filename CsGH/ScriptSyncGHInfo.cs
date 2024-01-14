using System;
using System.Drawing;
using Grasshopper;
using Grasshopper.Kernel;

namespace ScriptSyncGH
{
  public class CsGHInfo : GH_AssemblyInfo
  {
    public override string Name => "ScriptSync Info";

    //Return a 24x24 pixel bitmap to represent this GHA library.
    public override Bitmap Icon => null;

    //Return a short string describing the purpose of this GHA library.
    public override string Description => "";

    public override Guid Id => new Guid("95474D08-7103-4A0D-AD8B-64A3D4D23F1D");

    //Return a string identifying you or your company.
    public override string AuthorName => "";

    //Return a string representing your preferred contact details.
    public override string AuthorContact => "";
  }
}