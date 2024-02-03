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

import rhinoscriptsyntax as rs

class GHThread(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, name : str):
        super().__init__(name=name, daemon=False)
        self.component_on_canvas = True  # TODO: need getter and setter
        self._component_enabled = True

    @abc.abstractmethod
    def run(self):
        """ Run the thread. """
        pass

    # FIXME: this should be integrate the Rhino.RhinoApp.InvokeOnUiThread
    def check_if_component_on_canvas(self):
        """ Check if the component is on canvas. """
        if ghenv.Component.OnPingDocument() is None:
            self.component_on_canvas = False
            return False
        return True

    def check_if_component_enabled(self):
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

    # TODO: not tested
    def add_runtime_remark(self, exception : str):
        """ Add a blank tab to the component from main thread. """
        action = System.Action(
            lambda: ghenv.Component.AddRuntimeMessage(RML.Remark, exception)
        )
        Rhino.RhinoApp.InvokeOnUiThread(action)

    @property
    def component_enabled(self):
        self.check_if_component_enabled()
        return self._component_enabled



class ClientThread(GHThread):
    def __init__(self,
                vscode_server_ip : str,
                vscode_server_port : int,
                name : str):
        super().__init__(name=name)
        self.client_socket = None
        self.vscode_server_ip = vscode_server_ip
        self.vscode_server_port = vscode_server_port
        self.client_socket = socket
        self.is_connected = False
        self.refresh_rate = 1  # seconds

    def run(self):
        """ Run the thread. """

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while self.check_if_component_on_canvas() and self.component_enabled:  # FIXME: check also when component is disabled
            try:
                if not self.is_connected:
                    self.connect_to_vscode_server()
                    self.clear_component()
                    self.expire_component_solution()

                self.client_socket.send("Hello test!".encode())

                # data = self.client_socket.recv(1024).decode()
                # if not data:
                #     break
                # self.add_runtime_remark(f"script-sync::Received from server: {data}")

                time.sleep(self.refresh_rate)
            except Exception as e:
                if e.winerror == 10054:
                    # Connection was forcibly closed by the vscode-server
                    # it means that vscode has been shut down abruptly
                    # in this case a new socket needs to be created
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.is_connected = False

        client_socket.close()
        return

    def connect_to_vscode_server(self):
        """ Connect to the VSCode server. """
        while self.check_if_component_on_canvas() and not self.is_connected:
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
                    time.sleep(self.refresh_rate)
                except ConnectionResetError:
                    self.add_runtime_warning("script-sync::Connection was forcibly closed by the vscode-server")
                    time.sleep(self.refresh_rate)
                except socket.error as e:
                    if e.winerror == 10056:
                        self.add_runtime_warning(f"script-sync::A connect request was made on an already connected socket")
                        self.is_connected = True
                        break
                    else:
                        self.add_runtime_warning(f"script-sync::Error connecting to the vscode-server: {str(e)}")
                        time.sleep(self.refresh_rate)
                except Exception as e:
                    self.add_runtime_warning(f"script-sync::Error connecting to the vscode-server: {str(e)}")
                    time.sleep(self.refresh_rate)
        if self.is_connected:
            self.client_socket.send("script-sync::Hello vscode from GHcomponent!".encode())


    # def send_to_server(self, client_socket : socket.socket) -> None:
    #     """
    #         Send data to the server.
            
    #         :param client_socket: The client socket.
    #     """
    #     while self.component_on_canvas:
    #         try:
    #             client_socket.send("Hello server!".encode())
    #             time.sleep(2)
    #         except Exception as e:
    #             print(f"script-sync::Error sending to server: {str(e)}")
    #             break

    def receive_from_server(self, client_socket : socket.socket) -> None:
        """
            Receive data from the server.
            
            :param client_socket: The client socket.
        """
        while self.component_on_canvas:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"script-sync::Received from server: {data}")
                client_socket.send("Hello server!".encode())
            except Exception as e:
                print(f"script-sync::Error receiving from server: {str(e)}")
                break

class FileChangedThread(GHThread):
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
                Rhino.RhinoApp.InvokeOnUiThread(System.Action(self.check_if_component_on_canvas))
                
                if not self.component_on_canvas:
                    print(f"script-sync::Thread {self.name} aborted")
                    break
                
                current_modified = os.path.getmtime(path)
                if current_modified != last_modified:
                    last_modified = current_modified
                    self.expire_component_solution()


class ScriptSyncCPy(component):
    def __init__(self):
        super(ScriptSyncCPy, self).__init__()
        self._var_output = []
        ghenv.Component.Message = "ScriptSyncCPy"

        self.is_success = False

        self.vscode_server_ip = "127.0.0.1"
        self.vscode_server_port = 58260
        self.stdout = None
        # self.stderr = None  # TODO: can we redirect the stderr?
        self.stdout_lock = threading.Lock()

        self.filechanged_thread_name = None
        self.path = None
        self.path_lock = threading.Lock()

        self.client_thread_name = None


    # # TODO: this should be implmeneted in a separate thread to
    # # continusly check if vscode is started, if not just raise a warning
    # def connect_to_vscode_server(self):
    #     """ Connect to the VSCode server. """
    #     try:
    #         self.client_socket.connect((self.vscode_server_ip, self.vscode_server_port))
    #     except ConnectionRefusedError:
    #         print("script-sync::Connection refused by the vscode-server")
    #         return False
    #     except Exception as e:
    #         print(f"script-sync::Error connecting to the vscode-server: {str(e)}")
    #         return False
    #     self.client_socket.send("Hello vscode from GHcomponent!".encode())
    #     return True

    # TODO: see if we need to send back the stderror or stdout is enough to grab the err messages
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
        self.client_thread_name : str = f"script-sync-client-thread::{ghenv.Component.InstanceGuid}"
        _ = [print(t.name) for t in threading.enumerate()]
        if self.client_thread_name not in [t.name for t in threading.enumerate()]:
            ClientThread(self.vscode_server_ip,
                        self.vscode_server_port,
                        self.client_thread_name).start()

        # check the file is path
        self.path = r"F:\script-sync\GH\PyGH\test\runner_script.py"  # <<<< test
        
        if not os.path.exists(self.path):
            raise Exception("script-sync::File does not exist")

        # get the guid instance of the component
        self.filechanged_thread_name : str = f"script-sync-fileChanged-thread::{ghenv.Component.InstanceGuid}"
        if self.filechanged_thread_name not in [t.name for t in threading.enumerate()]:
            FileChangedThread(self.path, self.path_lock, self.filechanged_thread_name).start()
        

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