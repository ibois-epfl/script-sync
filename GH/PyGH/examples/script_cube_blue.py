#! python3

import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax
import scriptcontext

def main():
    brep_box = rg.Box(Rhino.Geometry.Plane.WorldXY, Rhino.Geometry.Interval(-1, 1), Rhino.Geometry.Interval(-1, 1), Rhino.Geometry.Interval(-1, 1))
    print("runner_script_2.py::main() function called")

    return brep_box

if __name__ == '__main__':
    cube_blue = main()