using System;
using System.Collections.Generic;


using Rhino;
using Rhino.Commands;
using Rhino.Geometry;

CsVersion.Main();

class CsVersion
{
    static public void Main()
    {
        // print the version of C# we are using
        Console.WriteLine("C# Runtime: " + Environment.Version.ToString());
        Console.WriteLine("platform: " + Environment.OSVersion.ToString());

        // add a cube
        var rhBox = new Box(Plane.WorldXY,
            new Interval(10, 20),
            new Interval(10, 20),
            new Interval(20, 30));

        // change color attributes of rhBox
        var boxAttributes = new Rhino.DocObjects.ObjectAttributes();
        boxAttributes.ObjectColor = System.Drawing.Color.Red;
        boxAttributes.ColorSource = 
            Rhino.DocObjects.ObjectColorSource.ColorFromObject;

        // add the cube to the document
        var id = RhinoDoc.ActiveDoc.Objects.AddBox(rhBox, boxAttributes);
    }
}
