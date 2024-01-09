# # async:true

import System
import Rhino
import Grasshopper as gh
import sys
import os
# import datetime
import time

# # async:true <--this go on top
# import threading

from System.Threading import Thread
from functools import partial

import rhinoscriptsyntax as rs

def update_component():
    ghenv.Component.ExpireSolution(True)

# class Thread(threading.Thread):
#     def __init__(self, thread_id, name, file_path):
#         threading.Thread.__init__(self)
#         self.thread_id = thread_id
#         self.name = name
#         self.file_path = file_path

#     def run(self):
#         print("Starting " + self.name)
#         check_file_change(self.file_path)
#         print("Exiting " + self.name)

def check_file_change(path):
    last_modified = os.path.getmtime(path)
    print("Entered file changed")
    while True:
        print("in loop")
        System.Threading.Thread.Sleep(1000)
        current_modified = os.path.getmtime(path)
        print(current_modified)
        if current_modified != last_modified:
            print("File has changed")
            last_modified = current_modified

            break
    print(">>>>>>>")


def safe_exec(code, globals, locals):
    # execute the code
    try:
        exec(code, globals, locals)
        return True
    except Exception as e:
        print(e)
        return False


class MyComponent(Grasshopper.Kernel.GH_ScriptInstance):
    # start a thread to check if the file has changed



    def RunScript(self, path, x, y):
        
        # check the file is path
        if not os.path.exists(path):
            raise Exception("File does not exist")

        # start a thread to check if the file has changed
        # if yes, recompute the solution of the component
        # if no, do nothing

        # convert path to us / instead of \
        # path = path.replace("\\", "/")


        # start a thread to check if the file has changed
        thread = Thread(partial(check_file_change, path))
        thread.Start()

        # threads = []
        # thread = Thread(1, "Thread-1", path)
        # thread.start()
        # threads.append(thread)

        




        # we need to add the path of the modules
        path_dir = path.split("\\")
        path_dir = "\\".join(path_dir[:-1])
        sys.path.insert(0, path_dir)

        with open(path, 'r') as f:
            code = f.read()
        return_code = safe_exec(code, globals(), locals())

        # # wait for all threads to complete
        # for t in threads:
        #     t.join()
        
        return

    # Solve overrides 
    def BeforeRunScript(self):
        pass

    def AfterRunScript(self):
        pass
