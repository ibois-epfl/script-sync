from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs





    # ghenv.Component.Params.OnParametersChanged()


def add_button():
    button = Grasshopper.Kernel.Special.GH_ButtonObject()
    button.CreateAttributes()
    button.Attributes.Pivot = System.Drawing.PointF(100, 100)
    button.Attributes.ExpireLayout()
    GH_doc = Grasshopper.Instances.ActiveCanvas.Document
    success = GH_doc.AddObject(docObject = button, update = False)
    
    return success
    
class MyComponent(component):


    def RunScript(self, script, x, y):

        # add_button()
        # get the Pivot of the parameter "script"

        script_pivot_X = ghenv.Component.Params.Input[0].Attributes.Pivot.X
        script_pivot_Y = ghenv.Component.Params.Input[0].Attributes.Pivot.Y

        button_pivot_X = script_pivot_X-150
        button_pivot_Y = script_pivot_Y-11




        button = Grasshopper.Kernel.Special.GH_ButtonObject()
        button.ExpressionNormal = "x"
        button.ExpressionPressed = "y"
        # change the name of the button
        button.EvaluateExpressions()
        button.CreateAttributes()
        button.Attributes.Pivot = System.Drawing.PointF(button_pivot_X, button_pivot_Y)
        button.Attributes.ExpireLayout()



        # link the button to the script
        ghenv.Component.Params.Input[0].AddSource(button)
        ghenv.Component.Params.OnParametersChanged()










        


        GH_doc = Grasshopper.Instances.ActiveCanvas.Document
        success = GH_doc.AddObject(docObject = button, update = True)  # set true to avoid to add new buttons




        # wire = Grasshopper.Kernel.Special.GH_Wire()
        # wire.CreateAttributes()
        # wire.Attributes.ExpireLayout()
        # GH_doc = Grasshopper.Instances.ActiveCanvas.Document
        # success = GH_doc.AddObject(docObject = wire, update = False)

        # wire.ConnectEnds(x, button)
        # wire.Update()
        return success
        



            
        
        a='OK'
        # return a