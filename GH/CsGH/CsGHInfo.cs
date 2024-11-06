using System;
using System.Drawing;
using Grasshopper;
using Grasshopper.Kernel;

namespace CsGH
{
  public class CsGHInfo : GH_AssemblyInfo
  {
    public override string Name => "CsGH Info";

    //Return a 24x24 pixel bitmap to represent this GHA library.
    public override Bitmap Icon => null;

    //Return a short string describing the purpose of this GHA library.
    public override string Description => "";

    public override Guid Id => new Guid("8FDABF86-6067-4496-977B-E17C6341F89E");

    //Return a string identifying you or your company.
    public override string AuthorName => "";

    //Return a string representing your preferred contact details.
    public override string AuthorContact => "";
  }
}