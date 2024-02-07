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
import json

import rhinoscriptsyntax as rs

# TODO: modify the error messages for client with vscode-related info
#TODO: add tooltip description to parameters in metadata
# TODO: in the tcp send to vscode, we need to include first the name of the selected file

class GHThread(threading.Thread, metaclass=abc.ABCMeta):
    """
        A base class for Grasshopper threads.
    """
    def __init__(self, name : str):
        super().__init__(name=name, daemon=False)
        self._component_on_canvas = True
        self._component_enabled = True

    @abc.abstractmethod
    def run(self):
        """ Run the thread. """
        pass

    def _check_if_component_on_canvas(self):
        """ Check if the component is on canvas from thread. """
        def __check_if_component_on_canvas():
            if ghenv.Component.OnPingDocument() is None:
                self._component_on_canvas = False
                return False
            else:
                self._component_on_canvas = True
                return True
        action = System.Action(__check_if_component_on_canvas)
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def _check_if_component_enabled(self):
        """ Check if the component is enabled from thread. """
        def __check_if_component_enabled():
            if ghenv.Component.Locked:
                self._component_enabled = False
            else:
                self._component_enabled = True
        action = System.Action(__check_if_component_enabled)
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def expire_component_solution(self):
        """ Fire the recalculation of the component solution from thread. """
        def __expire_component_solution():
            ghenv.Component.Params.Output[0].ClearData()  # clear the output
            ghenv.Component.ExpireSolution(True)  # expire the component
        action = System.Action(__expire_component_solution)
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def clear_component(self):
        """ Clear the component from thread. """
        def __clear_component():
            ghenv.Component.ClearData()
        action = System.Action(__clear_component)
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def add_runtime_warning(self, exception : str):
        """ Add a warning tab to the component from main thread. """
        action = System.Action(
            lambda: ghenv.Component.AddRuntimeMessage(RML.Warning, exception)
        )
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def add_runtime_error(self, exception : str):
        """ Add an error tab to the component from main thread. """
        action = System.Action(
            lambda: ghenv.Component.AddRuntimeMessage(RML.Error, exception)
        )
        Rhino.RhinoApp.InvokeOnUiThread(action)

    def add_runtime_remark(self, exception : str):
        """ Add a blank tab to the component from main thread. """
        action = System.Action(
            lambda: ghenv.Component.AddRuntimeMessage(RML.Remark, exception)
        )
        Rhino.RhinoApp.InvokeOnUiThread(action)

    @property
    def component_enabled(self):
        self._check_if_component_enabled()
        return self._component_enabled

    @property
    def component_on_canvas(self):
        self._check_if_component_on_canvas()
        return self._component_on_canvas

# TODO: clean this class
class ClientThread(GHThread):
    """
        A thread to connect to the VSCode server.
    """
    def __init__(self,
                vscode_server_ip : str,
                vscode_server_port : int,
                name : str,
                queue_msg : queue.Queue=None,
                lock_queue_msg : threading.Lock=None,
                event_fire_msg : threading.Event=None
                ):
        super().__init__(name=name)
        self.vscode_server_ip = vscode_server_ip
        self.vscode_server_port = vscode_server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.connect_refresh_rate = 1  # seconds
        self.queue_msg = queue_msg
        self.lock_queue_msg = lock_queue_msg
        self.event_fire_msg = event_fire_msg

    def run(self):
        """ Run the thread. Send the message to the vscode server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while self.component_on_canvas and self.component_enabled:
            try:
                if not self.is_connected:
                    self.connect_to_vscode_server()
                    self.clear_component()
                    self.expire_component_solution()
                    continue

                self.event_fire_msg.wait()

                with self.lock_queue_msg:
                    if self.queue_msg is not None:
                        if not self.queue_msg.empty():
                            msg = self.queue_msg.get()
                            self.queue_msg.task_done()
                            self.event_fire_msg.set()
                            self.event_fire_msg.clear()
                            self.client_socket.send(msg)

            #FIXME: readjust this catching
            except Exception as e:
                self.add_runtime_warning(f"script-sync::Error from run: {str(e)}")
                self.is_connected = False
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.close()
        return

    def connect_to_vscode_server(self):
        """ Connect to the VSCode server. """
        while self.component_on_canvas and not self.is_connected:
            try:
                self.client_socket.send(b"")
                self.is_connected = True
            except socket.error:
                try:
                    self.client_socket.connect((self.vscode_server_ip, self.vscode_server_port))
                    self.is_connected = True
                    break
                except ConnectionRefusedError:
                    self.add_runtime_warning("script-sync::Connection refused by the vscode-server")
                    self.is_connected = False
                except ConnectionResetError:
                    self.add_runtime_warning("script-sync::Connection was forcibly closed by the vscode-server")
                    self.is_connected = False
                except socket.error as e:
                    if e.winerror == 10056:
                        self.add_runtime_warning(f"script-sync::A connect request was made on an already connected socket")
                        self.is_connected = True
                        break
                    else:
                        self.add_runtime_warning(f"script-sync::Error connecting to the vscode-server: {str(e)}")
                except Exception as e:
                    self.add_runtime_warning(f"script-sync::Error connecting to the vscode-server: {str(e)}")
            finally:
                time.sleep(self.connect_refresh_rate)
        # if self.is_connected:
        #     self.client_socket.send("script-sync:: from GHcomponent:\n\n".encode())


class FileChangedThread(GHThread):
    """
        A thread to check if the file has changed on disk.
    """
    def __init__(self,
                path : str,
                path_lock : threading.Lock,
                name : str):
        super().__init__(name=name)
        self.path = path
        self.path_lock = path_lock
        self.refresh_rate = 1000  # milliseconds

    def run(self):
        """ Run the thread. """
        self.check_file_change(self.path, self.path_lock)

    def check_file_change(self, path : str, path_lock : threading.Lock) -> None:
        """
            Check if the file has changed on disk.
            
            :param path: The path of the file to check.
            :param path_lock: The lock for the path.
        """
        with path_lock:
            last_modified = os.path.getmtime(path)
            while self.component_on_canvas:
                System.Threading.Thread.Sleep(self.refresh_rate)
                current_modified = os.path.getmtime(path)
                if current_modified != last_modified:
                    last_modified = current_modified
                    self.expire_component_solution()


class ScriptSyncCPy(component):
    def __init__(self):
        super(ScriptSyncCPy, self).__init__()
        self._var_output = []
        ghenv.Component.Message = "no-script-selected"

        self.is_success = False

        self.client_thread_name : str = f"script-sync-client-thread::{ghenv.Component.InstanceGuid}"
        self.vscode_server_ip = "127.0.0.1"
        self.vscode_server_port = 58260
        self.stdout = None
        self.queue_msg = queue.Queue()
        self.queue_msg_lock = threading.Lock()
        self.event_fire_msg = threading.Event()

        self.filechanged_thread_name : str = f"script-sync-fileChanged-thread::{ghenv.Component.InstanceGuid}"
        self.__path_name_table_value = "script-sync::" + "path::" + str(ghenv.Component.InstanceGuid)
        self.path_lock = threading.Lock()

    def RemovedFromDocument(self, doc):
        """ Remove the component from the document. """
        if self.client_thread_name in [t.name for t in threading.enumerate()]:
            client_thread = [t for t in threading.enumerate() if t.name == self.client_thread_name][0]
            client_thread.join()
        if self.filechanged_thread_name in [t.name for t in threading.enumerate()]:
            filechanged_thread = [t for t in threading.enumerate() if t.name == self.filechanged_thread_name][0]
            filechanged_thread.join()
        if self.queue_msg is not None:
            self.queue_msg.join()
        if self.queue_msg_lock is not None:
            self.queue_msg_lock.release()
        if self.event_fire_msg is not None:
            self.event_fire_msg.clear()

        # clear the path from the table view
        del self.path

    def add_button(self):
        """Add a button to the canvas and wire it to the "script" param."""
        # get the "script" param by name
        script_param = [param for param in ghenv.Component.Params.Input if param.Name == "script"][0]

        button = gh.Kernel.Special.GH_ButtonObject()
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
        GH_doc = gh.Instances.ActiveCanvas.Document
        if not script_param.Sources:
            success = GH_doc.AddObject(docObject = button,
                                        update = False)
            script_param.AddSource(button)
            ghenv.Component.Params.OnParametersChanged()

        return True

    def safe_exec(self, path, globals, locals):
        """
            Execute Python3 code safely. It redirects the output of the code
            to a string buffer 'stdout' to output to the GH component param.
            It is send to the vscode server.
            
            :param path: The path of the file to execute.
            :param globals: The globals dictionary.
            :param locals: The locals dictionary.
        """
        try:
            with open(path, 'r') as f:
                # add the path of the file to use the modules
                path_dir = self.path.split("\\")
                path_dir = "\\".join(path_dir[:-1])
                sys.path.insert(0, path_dir)

                # parse the code
                code = compile(f.read(), path, 'exec')
                output = io.StringIO()

                # empty the queue and event
                with self.queue_msg_lock:
                    while not self.queue_msg.empty():
                        self.queue_msg.get()
                        self.queue_msg.task_done()
                self.event_fire_msg.clear()

                # execute the code
                with contextlib.redirect_stdout(output):
                    exec(code, globals, locals)
                locals["stdout"] = output.getvalue()

                # send the msg to the vscode server
                msg_json = json.dumps({"script_path": self.path,
                                       "guid": str(ghenv.Component.InstanceGuid),
                                       "msg": output.getvalue()})
                msg_json = msg_json.encode('utf-8')
                self.queue_msg.put(msg_json)
                self.event_fire_msg.set()

                # pass the script variables to the GH component outputs
                outparam = ghenv.Component.Params.Output
                outparam_names = [p.NickName for p in outparam]
                for outp in outparam_names:
                    if outp in locals.keys():
                        self._var_output.append(locals[outp])
                    else:
                        self._var_output.append(None)

                sys.stdout = sys.__stdout__
            return locals

        except Exception as e:

            # send the error message to the vscode server
            err_json = json.dumps({"script_path": self.path,
                                    "guid": str(ghenv.Component.InstanceGuid),
                                    "msg": "err:" + str(e)})
            err_json = err_json.encode('utf-8')
            self.queue_msg.put(err_json)
            self.event_fire_msg.set()
            
            sys.stdout = sys.__stdout__

            err_msg = f"script-sync::Error in the code: {str(e)}"
            raise Exception(err_msg)

    def BeforeRunScript(self):
        """
            This method is called as soon as the component has been
            placed on the canvas and before the script is run.
        """
        self.add_button()

    def RunScript(self,
                  script : bool,
                  x : int):
        """ This method is called whenever the component has to be recalculated it's the solve main instance. """
        self.is_success = False

        # set the path
        if script is True:
            dialog = System.Windows.Forms.OpenFileDialog()
            dialog.Filter = "Python files (*.py)|*.py"
            dialog.Title = "Select a Python file"
            dialog.InitialDirectory = os.path.dirname("")
            dialog.FileName = ""
            dialog.Multiselect = False
            dialog.CheckFileExists = True
            dialog.CheckPathExists = True
            dialog.RestoreDirectory = True
            if dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
                self.path = dialog.FileName
        if self.path is None:
            raise Exception("script-sync::File not selected")
        if not os.path.exists(self.path):
            raise Exception("script-sync::File does not exist")

        # file change listener thread
        
        if self.filechanged_thread_name not in [t.name for t in threading.enumerate()]:
            FileChangedThread(self.path, self.path_lock, self.filechanged_thread_name).start()

        # set up the tcp client to connect to the vscode server
        _ = [print(t.name) for t in threading.enumerate()]
        if self.client_thread_name not in [t.name for t in threading.enumerate()]:
            ClientThread(self.vscode_server_ip,
                        self.vscode_server_port,
                        self.client_thread_name,
                        self.queue_msg,
                        self.queue_msg_lock,
                        self.event_fire_msg
                        ).start()

        # run the script
        res = self.safe_exec(self.path, globals(), locals())
        self.is_success = True
        return

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

    @property
    def path(self):
        """ Get the path of the file from the table view to be sticking between the sessions. """
        table_value = ghenv.Component.OnPingDocument().ValueTable.GetValue(
            self.__path_name_table_value, "not_found"
        )
        if table_value != "not_found":
            return table_value
        else:
            return None

    @path.setter
    def path(self, path : str):
        """ Set the path of the file to the table view to be sticking between the sessions. """
        ghenv.Component.OnPingDocument().ValueTable.SetValue(self.__path_name_table_value, path)

        script_name = os.path.basename(path)
        ghenv.Component.Message = f"{script_name}"

    @path.deleter
    def path(self):
        """ Delete the path of the file from the table view if the object is erased. """
        ghenv.Component.OnPingDocument().ValueTable.DeleteValue(self.__path_name_table_value)
