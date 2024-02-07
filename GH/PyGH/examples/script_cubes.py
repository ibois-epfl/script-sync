#! python3

import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax
import scriptcontext

def main():
    box_blue = None
    box_gray = None
    box_yellow = None

    box_blue = rg.Box(rg.Plane.WorldXY,
                      rg.Interval(0, 10),
                      rg.Interval(0, 10),
                      rg.Interval(0, 10))
    print(f"blue box: {box_blue}")

    box_gray = rg.Box(rg.Plane.WorldXY, 
                      rg.Interval(5,15),
                      rg.Interval(5,15),
                      rg.Interval(10,20))
    print(f"gray box: {box_gray}")

    box_yellow = rg.Box(rg.Plane.WorldXY,
                        rg.Interval(10,20),
                        rg.Interval(10,20),
                        rg.Interval(20,30))
    print(f"yellow box: {box_yellow}")

    return box_blue, box_gray, box_yellow

if __name__ == '__main__':
    cube_blue, cube_gray, cube_yellow = main()