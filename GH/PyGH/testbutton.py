from ghpythonlib.componentbase import executingcomponent as component

import System
import System.Drawing
import System.Windows.Forms
import Rhino
import Grasshopper as gh
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import sys
import os
import time

import contextlib
import io

import abc
import socket
import threading
import queue

import rhinoscriptsyntax as rs


class Attributes_Custom(gh.Kernel.Attributes.GH_ComponentAttributes): # inherits all methods of GH_ComponentAttributes
    def Layout(self): # override inherited method Layout
        gh.Kernel.Attributes.GH_ComponentAttributes.Layout(self) # run render before changing the definition
        rec0 = gh.Kernel.GH_Convert.ToRectangle(self.Bounds) #System.Drawing.Rectangle 
        rec0.Height += 22
        rec1 = rec0
        rec1.Y = rec1.Bottom - 22
        rec1.Height = 22
        rec1.Inflate(-2, -2)
        Bounds = rec0
        self.Bounds=Bounds
        ButtonBounds = rec1
        self.ButtonBounds=ButtonBounds
    
    def Render(self,canvas, graphics, channel): # Override Render method
        gh.Kernel.Attributes.GH_ComponentAttributes.Render(self, canvas, graphics, channel) # run render before changing the definition
        if channel == gh.GUI.Canvas.GH_CanvasChannel.Objects:
            button = gh.GUI.Canvas.GH_Capsule.CreateTextCapsule(self.ButtonBounds, self.ButtonBounds, gh.GUI.Canvas.GH_Palette.Black, "Button", 2, 0)
            button.Render(graphics, self.Selected, self.Owner.Locked, False)
            button.Dispose()
    
    def RespondToMouseDown(self,sender,e):
        if e.Button == System.Windows.Forms.MouseButtons.Left:
            rec = self.ButtonBounds
            if rec.Contains(e.CanvasLocation):
                MessageBox.Show("The button was clicked", "Button", MessageBoxButtons.OK)
                return  gh.GUI.Canvas.GH_ObjectResponse.Handled
        self.sender=sender
        self.e=e
        self.RespondToMouseDown(sender, e)




class MyComponent(component):
    def __init__(self):
        super(MyComponent, self).__init__()

    def CreateAttributes(self):
        self.Attributes = Attributes_Custom(self)


    def RunScript(self, x, y):
        """Grasshopper Script"""
        a = "Hello Python 3 in Grasshopper!"
        print(a)

        
        
        return
