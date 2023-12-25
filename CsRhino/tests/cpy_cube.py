#! python3

import sys
import System.Drawing

import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs


def main():
    # print the python version
    print(sys.version)

    # add aa simple cube to the Rhino scene
    cube = rg.Box(rg.Plane.WorldXY, 
        rg.Interval(5,15),
        rg.Interval(5,15),
        rg.Interval(10,20))
    brep = cube.ToBrep()
    color = System.Drawing.Color.Magenta
    guid = Rhino.RhinoDoc.ActiveDoc.Objects.AddBrep(brep)
    rs.ObjectColor(guid, color)


if __name__ == "__main__":
    main()