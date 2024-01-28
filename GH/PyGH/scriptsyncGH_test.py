from ghpythonlib.componentbase import executingcomponent as component

import System
import Rhino
import Grasshopper as gh
import sys
import os
import time

import threading

import rhinoscriptsyntax as rs


class ScriptSyncThread(threading.Thread):
    def __init__(self,
                path : str,
                path_lock : threading.Lock,
                name : str):
        super().__init__(name=name, daemon=False)
        self.path = path
        self.path_lock = path_lock
        self.component_on_canvas = True

    def run(self):
        """ Run the thread. """
        self.check_file_change(self.path, self.path_lock)

    def check_if_component_on_canvas(self):
        """ Check if the component is on canvas. """
        if ghenv.Component.OnPingDocument() is None:
            self.component_on_canvas = False

    def update_component(self):
        """ Fire the recalculation of the component solution. """
        ghenv.Component.Params.Output[0].ClearData()  # clear the output
        ghenv.Component.ExpireSolution(True)  # expire the component

    def check_file_change(self, path : str, path_lock : threading.Lock) -> None:
        """
            Check if the file has changed on disk.
            
            :param path: The path of the file to check.
            :param path_lock: The lock for the path.
        """
        with path_lock:
            last_modified = os.path.getmtime(path)
            while self.component_on_canvas:
                System.Threading.Thread.Sleep(1000)
                Rhino.RhinoApp.InvokeOnUiThread(System.Action(self.check_if_component_on_canvas))
                
                if not self.component_on_canvas:
                    print(f"script-sync::Thread {self.name} aborted")
                    break
                
                current_modified = os.path.getmtime(path)
                if current_modified != last_modified:
                    last_modified = current_modified
                    Rhino.RhinoApp.InvokeOnUiThread(System.Action(self.update_component))


class ScriptSyncCPy(component):
    def __init__(self):
        super(ScriptSyncCPy, self).__init__()
        self._var_output = []
        ghenv.Component.Message = "ScriptSyncCPy"

        self.thread_name = None
        self.path = None
        self.path_lock = threading.Lock()

        # FIXME: output cannot be set by componentizer, redirect the output of python to
        # a custom string output

    def safe_exec(self, path, globals, locals):
        """
            Execute Python3 code safely.
            
            :param path: The path of the file to execute.
            :param globals: The globals dictionary.
            :param locals: The locals dictionary.
        """
        try:
            with open(path, 'r') as f:
                code = compile(f.read(), path, 'exec')
                exec(code, globals, locals)
            return locals  # return the locals dictionary
        except Exception as e:
            err_msg = str(e)
            return e

    def RunScript(self, x, y):
        """ This method is called whenever the component has to be recalculated. """
        # check the file is path
        self.path = r"F:\script-sync\GH\PyGH\test\runner_script.py"  # <<<< test
        
        if not os.path.exists(self.path):
            raise Exception("script-sync::File does not exist")

        # get the guid instance of the component
        self.thread_name : str = f"script-sync-thread::{ghenv.Component.InstanceGuid}"
        if self.thread_name not in [t.name for t in threading.enumerate()]:
            ScriptSyncThread(self.path, self.path_lock, self.thread_name).start()
        
        # we need to add the path of the modules
        path_dir = self.path.split("\\")
        path_dir = "\\".join(path_dir[:-1])
        sys.path.insert(0, path_dir)

        # run the script
        res = self.safe_exec(self.path, globals(), locals())
        if isinstance(res, Exception):
            err_msg = f"script-sync::Error in the code: {res}"
            print(err_msg)
            raise Exception(err_msg)

        # get the output variables defined in the script
        outparam = ghenv.Component.Params.Output
        outparam_names = [p.NickName for p in outparam if p.NickName != "out"]
        for outp in outparam_names:
            if outp in res.keys():
                self._var_output.append(res[outp])
            else:
                self._var_output.append(None)

        return self._var_output

    def AfterRunScript(self):
        """
            This method is called as soon as the component has finished
            its calculation. It is used to load the GHComponent outputs
            with the values created in the script.
        """
        outparam = [p for p in ghenv.Component.Params.Output if p.NickName != "out"]
        outparam_names = [p.NickName for p in outparam]
        
        for idx, outp in enumerate(outparam):
            ghenv.Component.Params.Output[idx+1].VolatileData.Clear()
            ghenv.Component.Params.Output[idx+1].AddVolatileData(gh.Kernel.Data.GH_Path(0), 0, self._var_output[idx])
        self._var_output.clear()