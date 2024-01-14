#! python2

import sys
import platform

import Rhino

import module_imp

Rhino.RhinoApp.WriteLine("Python Version: " + platform.python_version())
Rhino.RhinoApp.WriteLine(platform.python_implementation())
Rhino.RhinoApp.WriteLine(sys.version)
module_imp.test_module()