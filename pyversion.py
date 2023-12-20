#! python3

import sys
import platform

import Rhino

import module_imp

Rhino.RhinoApp.WriteLine(platform.python_implementation())
Rhino.RhinoApp.WriteLine(sys.version)
print("TESTING")

module_imp.test_module()