from ghpythonlib.componentbase import executingcomponent as component

import System
import System.Drawing
import System.Windows.Forms
import Rhino
import Grasshopper
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

import importlib
import sys


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

class ClientThread(GHThread):
    """
    A thread to connect to the VSCode server.
    """
    def __init__(self, vscode_server_ip: str, vscode_server_port: int, name: str,
                 queue_msg: queue.Queue = None, lock_queue_msg: threading.Lock = None,
                 event_fire_msg: threading.Event = None):
        super().__init__(name=name)
        self.vscode_server_ip = vscode_server_ip
        self.vscode_server_port = vscode_server_port
        self.is_connected = False
        self.connect_refresh_rate = 1  # seconds
        self.queue_msg = queue_msg
        self.lock_queue_msg = lock_queue_msg
        self.event_fire_msg = event_fire_msg
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """ Run the thread. Send the message to the vscode server."""
        while self.component_on_canvas and self.component_enabled:
            try:
                if not self.is_connected:
                    self.connect_to_vscode_server()
                    self.clear_component()
                    self.expire_component_solution()
                    continue

                self.event_fire_msg.wait()
                self.send_message_from_queue()

            except Exception as e:
                self.add_runtime_warning(f"script-sync::Unkown error from run: {str(e)}")
                self.is_connected = False
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.close()

    def send_message_from_queue(self):
        with self.lock_queue_msg:
            if self.queue_msg and not self.queue_msg.empty():
                msg = self.queue_msg.get()
                self.queue_msg.task_done()
                self.event_fire_msg.set()
                self.event_fire_msg.clear()
                self.client_socket.send(msg)

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
                except (ConnectionRefusedError, ConnectionResetError, socket.error) as e:
                    self.handle_connection_error(e)
            finally:
                time.sleep(self.connect_refresh_rate)

    def handle_connection_error(self, e):
        error_messages = {
            ConnectionRefusedError: "script-sync::Connection refused by the vscode",
            ConnectionResetError: "script-sync::Connection was forcibly closed by the vscode",
            socket.error: f"script-sync::Error connecting to the vscode: {str(e)}"
        }
        self.add_runtime_warning(error_messages[type(e)])
        self.is_connected = False if type(e) != socket.error or e.winerror != 10056 else True


class FileChangedThread(GHThread):
    """
        A thread to check if the file has changed on disk.
    """
    def __init__(self,
                path : str,
                name : str
                ):
        super().__init__(name=name)
        self.path = path
        self.refresh_rate = 1000  # milliseconds
        self._on_file_changed = threading.Event()

    def run(self):
        """
            Check if the file has changed on disk.
        """
        last_modified = os.path.getmtime(self.path)
        while self.component_on_canvas and not self._on_file_changed.is_set():
            System.Threading.Thread.Sleep(self.refresh_rate)
            last_modified = self.is_file_modified(last_modified)
        self._on_file_changed.clear()
        return

    def stop(self):
        """ Stop the thread. """
        self._on_file_changed.set()

    def is_file_modified(self, last_modified):
        current_modified = os.path.getmtime(self.path)
        if current_modified != last_modified:
            self.expire_component_solution()
            return current_modified
        return last_modified


class ScriptSyncCPy(component):
    def __init__(self):
        super(ScriptSyncCPy, self).__init__()
        self._var_output = []

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
        if self.path is None:
            ghenv.Component.Message = "select-script"

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

    def init_script_path(self, btn : bool = False):
        """
            Check if the button is pressed and load/change path script.
            
            :param btn: A boolean of the button
        """
        # check if button is pressed
        if btn is True:
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

        # default init stauts
        if self.path is None:
            raise Exception("script-sync::File not selected")

        # fi file is in table view before
        if not os.path.exists(self.path):
            raise Exception("script-sync::File does not exist")
    
    def reload_all_modules(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]  # remove '.py' from filename
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])

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
                path_dir = os.path.dirname(path)
                sys.path.insert(0, path_dir)
                self.reload_all_modules(path_dir)

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
                msg_json = json.dumps({"script_path": path,
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
            err_json = json.dumps({"script_path": path,
                                    "guid": str(ghenv.Component.InstanceGuid),
                                    "msg": "err:" + str(e)})
            err_json = err_json.encode('utf-8')
            self.queue_msg.put(err_json)
            self.event_fire_msg.set()
            
            sys.stdout = sys.__stdout__

            err_msg = f"script-sync::Error in the code: {str(e)}"
            raise Exception(err_msg)

    def RunScript(self, btn: bool, x: float):
        """ This method is called whenever the component has to be recalculated it's the solve main instance. """

        self.is_success = False

        # set the path if button is pressed
        self.init_script_path(btn)

        # file change listener thread
        if self.filechanged_thread_name not in [t.name for t in threading.enumerate()]:
            FileChangedThread(self.path,
                              self.filechanged_thread_name
                              ).start()

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

        # add to the globals all the input parameters of the component (the locals)
        globals().update(locals())

        res = self.safe_exec(self.path, None, globals())
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
        
        # TODO: add the conversion to datatree for nested lists and tuples
        for idx, outp in enumerate(outparam):
            # detect if the output is a list
            if type(self._var_output[idx]) == list or type(self._var_output[idx]) == tuple:
                ghenv.Component.Params.Output[idx].VolatileData.Clear()
                ghenv.Component.Params.Output[idx].AddVolatileDataList(gh.Kernel.Data.GH_Path(0), self._var_output[idx])
            else:
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

        if self.filechanged_thread_name in [t.name for t in threading.enumerate()]:
            _ = [t for t in threading.enumerate() if t.name == self.filechanged_thread_name][0].stop()

    @path.deleter
    def path(self):
        """ Delete the path of the file from the table view if the object is erased. """
        ghenv.Component.OnPingDocument().ValueTable.DeleteValue(self.__path_name_table_value)
