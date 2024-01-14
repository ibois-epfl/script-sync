#! python3

import sys
import platform

import Rhino

import rhinoscriptsyntax as rs

import module_imp
import sub_module.submodule_imp as sub_module

print("Python Version: " + platform.python_version())
print(platform.python_implementation())
print(sys.version)

module_imp.test_module()
sub_module.test_module()

point = Rhino.Geometry.Point3d(0, 0, 0)

a = "42"
b = point
d = "0000"
c = x
print(a)
print(x)