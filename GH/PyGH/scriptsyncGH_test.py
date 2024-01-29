from ghpythonlib.componentbase import executingcomponent as component

import System
import System.Drawing
import System.Windows.Forms
import Rhino
import Grasshopper as gh
import sys
import os
import time

import contextlib
import io

import socket
import threading

import rhinoscriptsyntax as rs

# TODO: create an abc class for threads with utility methods
# and create a class for a new TCPThread


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

        self.is_success = False

        self.vscode_server_ip = "127.0.0.1"
        self.vscode_server_port = 58260
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.thread_name = None
        self.path = None
        self.path_lock = threading.Lock()

    # TODO: this should be implmeneted in a separate thread to
    # continusly check if vscode is started, if not just raise a warning
    def connect_to_vscode_server(self):
        """ Connect to the VSCode server. """
        try:
            self.client_socket.connect((self.vscode_server_ip, self.vscode_server_port))
        except ConnectionRefusedError:
            print("script-sync::Connection refused by the vscode-server")
            return False
        except Exception as e:
            print(f"script-sync::Error connecting to the vscode-server: {str(e)}")
            return False
        self.client_socket.send("Hello vscode from GHcomponent!".encode())
        return True

    def safe_exec(self, path, globals, locals):
        """
            Execute Python3 code safely. It redirects the output of the code
            to a string buffer 'stdout' to output to the GH component param.
            
            :param path: The path of the file to execute.
            :param globals: The globals dictionary.
            :param locals: The locals dictionary.
        """
        try:
            with open(path, 'r') as f:
                code = compile(f.read(), path, 'exec')
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(code, globals, locals)
                locals["stdout"] = output.getvalue()
                sys.stdout = sys.__stdout__
            return locals
        except Exception as e:
            err_msg = f"script-sync::Error in the code: {str(e)}"
            # TODO: here we need to send back the erro mesage to vscode
            sys.stdout = sys.__stdout__
            raise Exception(err_msg)

    def RunScript(self):
        """ This method is called whenever the component has to be recalculated. """
        self.is_success = False
        
        # connect to the vscode server
        if not self.connect_to_vscode_server():
            raise Exception("script-sync::Error connecting to the vscode-server")
        
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

        # get the output variables defined in the script
        outparam = ghenv.Component.Params.Output
        outparam_names = [p.NickName for p in outparam]
        for outp in outparam_names:
            if outp in res.keys():
                self._var_output.append(res[outp])
            else:
                self._var_output.append(None)
    
        self.is_success = True
    # TODO: add a menu item to select the file to run


    def AfterRunScript(self):
        """
            This method is called as soon as the component has finished
            its calculation. It is used to load the GHComponent outputs
            with the values created in the script.
        """
        if not self.is_success:
            return
        outparam = [p for p in ghenv.Component.Params.Output]
        outparam_names = [p.NickName for p in outparam]
        
        for idx, outp in enumerate(outparam):
            ghenv.Component.Params.Output[idx].VolatileData.Clear()
            ghenv.Component.Params.Output[idx].AddVolatileData(gh.Kernel.Data.GH_Path(0), 0, self._var_output[idx])
        self._var_output.clear()