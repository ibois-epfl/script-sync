using System;
using System.Collections.Generic;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

// using Eto;

namespace ScriptSync
{
    [Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)]
    public class ScriptSyncStart : Command
    {
        private TcpListener _server;
        private bool _isRunning;
        private string _ip = "127.0.0.1";
        private int _port = 13000;

        public ScriptSyncStart()
        {
            Instance = this;
        }

        public static ScriptSyncStart Instance { get; private set; }

        public override string EnglishName => "ScriptSyncStart";

        protected override Rhino.Commands.Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // start a local server
            RhinoApp.WriteLine("Starting ScriptSync..");
            if (_isRunning)
            {
                RhinoApp.WriteLine("Server already running");
                return Rhino.Commands.Result.Success;
            }
            _server = new TcpListener(IPAddress.Parse(_ip), _port);
            _isRunning = false;

            // start a thread in async mode
            Thread thread = new Thread(new ThreadStart(Run));
            thread.Start();

            return Rhino.Commands.Result.Success;
        }

        public void Run()
        {
            _server.Start();
            _isRunning = true;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                if (!IsScriptEditorRunnerFromThreadOk())
                    throw new Exception("ScriptEditorRunner is not working");
            }));

            while (_isRunning)
            {
                TcpClient client = _server.AcceptTcpClient();
                byte[] data = new byte[1024];
                client.GetStream().Read(data, 0, data.Length);
                string scriptPath = Encoding.ASCII.GetString(data);

                RhinoApp.InvokeOnUiThread(new Action(() =>
                {
                    try
                    {
                        RhinoApp.RunScript("_-ScriptEditor Run " + scriptPath, true);
                    }
                    catch (Exception e)
                    {
                        RhinoApp.WriteLine("Error: " + e.Message);
                    }
                }));
            }
        }

        private bool IsScriptEditorRunnerFromThreadOk()
        {
            string cPyScriptPath = System.IO.Path.GetFullPath(@"./tests/cpy_version.py");
            string ironPyScriptPath = System.IO.Path.GetFullPath(@"./tests/ironpy_version.py");
            string csScriptPath = System.IO.Path.GetFullPath(@"./tests/CsVersion.cs");

            bool cPyIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + cPyScriptPath, false);
            bool ironPyIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + ironPyScriptPath, false);
            bool csIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + csScriptPath, false);

            if (!cPyIsRunning || !ironPyIsRunning || !csIsRunning)
                return false;
            return true;
        }
    }
}
