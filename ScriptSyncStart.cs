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
        private bool _isRunning;
        public bool IsRunning { get { return _isRunning; } }

        public ScriptSyncStart()
        {
            // Rhino only creates one instance of each command class defined in a
            // plug-in, so it is safe to store a refence in a static property.
            Instance = this;
        }

        ///<summary>The only instance of this command.</summary>
        public static ScriptSyncStart Instance { get; private set; }

        public override string EnglishName => "ScriptSyncStart";

        protected override Rhino.Commands.Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // start a local server
            RhinoApp.WriteLine("Starting server if not already running...");
            if (_isRunning)
            {
                RhinoApp.WriteLine("Server already running");
                return Rhino.Commands.Result.Success;
            }
            _server = new TcpListener(IPAddress.Parse("127.0.0.1", 13000));
            _isRunning = false;
            Thread thread = new Thread(new ThreadStart(Run));
            thread.Start();
            RhinoApp.WriteLine("Server started");

            string pyFile = @"F:\ScriptSync\pyversion.py";
            RhinoApp.InvokeOnUiThread(new Action(() => {
                RhinoApp.WriteLine("Result: {0}", RhinoApp.RunScript("_-ScriptEditor Run " + pyFile, true));
            }));
            return Rhino.Commands.Result.Success;
        }

        public void Run()
        {
            _server.Start();
            _isRunning = true;

            while (_isRunning)
            {
                TcpClient client = _server.AcceptTcpClient();

                // recive data
                byte[] data = new byte[1024];
                client.GetStream().Read(data, 0, data.Length);
                string text = Encoding.ASCII.GetString(data);
                RhinoApp.WriteLine("Received: {0}", text);
                

                client.Close();
            }
        }


    }
}
