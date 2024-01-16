# r: pytoml==0.1.21

import ghpythonlib.components as ghcomp
import rhinoscriptsyntax as rs

import pytoml as toml

import Rhino

# run the component Script from native grasshopper
print(ghcomp)

toml.loads("a = 1")
print(toml)
# run the component Script from native rhino
