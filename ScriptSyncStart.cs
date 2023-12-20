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

            while (_isRunning)
            {
                TcpClient client = _server.AcceptTcpClient();
                // read the data from the client
                byte[] data = new byte[1024];
                client.GetStream().Read(data, 0, data.Length);
                string scriptPath = Encoding.ASCII.GetString(data);
                RhinoApp.WriteLine("Executing script: " + scriptPath);

                RhinoApp.InvokeOnUiThread(new Action(() =>
                {
                    RhinoApp.WriteLine("Hello from UI thread");
                    RhinoApp.RunScript("_-ScriptEditor Run \"" + scriptPath + "\"", true);
                }));
            }
        }
    }
}
