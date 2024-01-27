from ghpythonlib.componentbase import executingcomponent as component

import System
import Rhino
import Grasshopper as gh
import sys
import os
import time

import threading

# from System.Threading import Thread
# from functools import partial

import rhinoscriptsyntax as rs


def update_component():
    """ Fire the recalculation of the component solution. """
    # clear the output
    ghenv.Component.Params.Output[0].ClearData()
    # # expire the component
    ghenv.Component.ExpireSolution(True)

def check_file_change(path, path_lock):
    """
        Check if the file has changed on disk.
        
        :param path: The path of the file to check.
        :returns: True if the file has changed, False otherwise.
    """
    with path_lock:
        last_modified = os.path.getmtime(path)
        while True:
            System.Threading.Thread.Sleep(1000)
            
            current_modified = os.path.getmtime(path)
            if current_modified != last_modified:
                last_modified = current_modified
                action = System.Action(update_component)
                Rhino.RhinoApp.InvokeOnUiThread(action)
                break
    return


def safe_exec(path, globals, locals):
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

# define a custom Exception class
class ScriptSyncError(Exception):
    def __init__(self, msg, thread):
        self.msg = msg
        # release all the resources
        thread.Abort()

    def __str__(self):
        return self.msg


class ScriptSyncCPy(component):
    def __init__(self):
        super(ScriptSyncCPy, self).__init__()
        self._var_output = ["None"]
        ghenv.Component.Message = "ScriptSyncCPy"

        self.thread = None
        self.path = None
        self.path_lock = threading.Lock()

        # print(f'Number of scriptsync_threads: {len(threading.enumerate())}')
    
    def RunScript(self, x, y):
        """ This method is called whenever the component has to be recalculated. """
        # check the file is path
        self.path = r"F:\script-sync\GH\PyGH\test\runner_script.py"  # <<<< test
        
        if not os.path.exists(self.path):
            raise Exception("script-sync::File does not exist")

        print(f"script-sync::x value: {x}")

        # share the self.path resource among threads
        

        # # non-blocking thread
        # action = partial(check_file_change, self.path)
        # Rhino.RhinoApp.InvokeOnUiThread(action)
        # self.thread = Thread(partial(check_file_change, self.path))
        # self.thread.Start()

        thread = threading.Thread(target=check_file_change, args=(self.path, self.path_lock))
        thread.start()




        # we need to add the path of the modules
        path_dir = self.path.split("\\")
        path_dir = "\\".join(path_dir[:-1])
        sys.path.insert(0, path_dir)

        # run the script
        res = safe_exec(self.path, globals(), locals())
        if isinstance(res, Exception):
            err_msg = f"script-sync::Error in the code: {res}"
            print(err_msg)
            raise Exception(err_msg)
            # raise ScriptSyncError(err_msg, self.thread)

        # get the output variables defined in the script
        outparam = ghenv.Component.Params.Output
        outparam_names = [p.NickName for p in outparam if p.NickName != "out"]
        for k, v in res.items():
            if k in outparam_names:
                self._var_output.append(v)

        return self._var_output

    # FIXME: problem with indexing  return
    def AfterRunScript(self):
        outparam = ghenv.Component.Params.Output
        for idx, outp in enumerate(outparam):
            if outp.NickName != "out":
                ghenv.Component.Params.Output[idx].VolatileData.Clear()
                ghenv.Component.Params.Output[idx].AddVolatileData(gh.Kernel.Data.GH_Path(0), 0, self._var_output[idx])
        self._var_output = ["None"]
