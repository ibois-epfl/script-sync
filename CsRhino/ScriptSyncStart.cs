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


namespace ScriptSync
{
    [Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)]
    public class ScriptSyncStart : Command
    {
        private TcpListener _server;
        public TcpListener Server { get { return _server; } }
        public Thread WorkerThread { get; set; }
        public bool IsRunning { get; set; }
        public string Ip = "127.0.0.1";
        public int Port = 58259;

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
            if (IsRunning)
            {
                RhinoApp.WriteLine("Server already running");
                return Rhino.Commands.Result.Success;
            }
            _server = new TcpListener(IPAddress.Parse(Ip), Port);
            IsRunning = false;

            Thread WorkerThread = new Thread(new ThreadStart(Run));
            WorkerThread.Start();

            return Rhino.Commands.Result.Success;
        }

        public void Run()
        {
            _server.Start();
            IsRunning = true;

            // FIXME: this won't work in the shipped version 
            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                if (!IsScriptEditorRunnerFromThreadOk())
                    throw new Exception("ScriptEditorRunner is not working");
            }));

            while (IsRunning)
            {
                using (TcpClient client = _server.AcceptTcpClient())
                {
                    byte[] data = new byte[1024];
                    using (NetworkStream stream = client.GetStream())
                    {
                        stream.Read(data, 0, data.Length);
                    }
                    string scriptPath = Encoding.ASCII.GetString(data);
                    RhinoApp.InvokeOnUiThread(new Action(() =>
                    {
                        RhinoApp.WriteLine("Path. " + scriptPath + "");
                    }));
                    // // stop the server
                    // if (scriptPath == "101")
                    //     goto end;

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
            // end:
            _server.Stop();
            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                RhinoApp.WriteLine("ScriptSync stopped");
            }));
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
