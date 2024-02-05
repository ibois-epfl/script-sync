from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs


def add_button() -> bool:
    """Add a button to the canvas and wire it to the "script" param."""
    # get the "script" param by name
    script_param = [param for param in ghenv.Component.Params.Input if param.Name == "script"][0]

    button = Grasshopper.Kernel.Special.GH_ButtonObject()
    button.Name = ""
    button.NickName = ""
    button.EvaluateExpressions()
    button.CreateAttributes()

    script_pivot_X = script_param.Attributes.Pivot.X
    script_pivot_Y = script_param.Attributes.Pivot.Y
    button_pivot_X = script_pivot_X-100
    button_pivot_Y = script_pivot_Y-11
    button.Attributes.Pivot = System.Drawing.PointF(button_pivot_X,
                                                            button_pivot_Y)
    button.Attributes.ExpireLayout()

    # wire it to "script" param
    GH_doc = Grasshopper.Instances.ActiveCanvas.Document
    if not script_param.Sources:
        success = GH_doc.AddObject(docObject = button,
                                    update = False)
        script_param.AddSource(button)
        ghenv.Component.Params.OnParametersChanged()

    return True



class MyComponent(component):
    def __init__(self):
        super(MyComponent, self).__init__()
        self.button = None

    def BeforeRunScript(self):
        add_button()

    def RunScript(self, script, _path, x):

        # add_button()
        pass


        
        