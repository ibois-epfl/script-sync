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
            // if (_isRunning)
            // {
            //     RhinoApp.WriteLine("Server already running");
            //     return Rhino.Commands.Result.Success;
            // }
            // _server = new TcpListener(IPAddress.Parse(_ip), _port);
            // _isRunning = false;

            // start a thread in async mode
            Thread thread = new Thread(new ThreadStart(Run));
            thread.Start();

            return Rhino.Commands.Result.Success;
        }

        public void Run()
        {
            // _server.Start();
            _isRunning = true;

            string pyFile = @"F:\ScriptSync\pyversion.py";

            while (_isRunning)
            {
                // TcpClient client = _server.AcceptTcpClient();
                // byte[] data = Encoding.ASCII.GetBytes("Hello from server");
                // client.GetStream().Write(data, 0, data.Length);
                // client.Close();

                // wait 2 seconds
                Thread.Sleep(2000);


                RhinoApp.InvokeOnUiThread(new Action(() =>
                // Eto.Forms.Application.Instance.Invoke(() =>
                {
                    RhinoApp.WriteLine("Hello from UI thread");
                    RhinoApp.RunScript("_-ScriptEditor Run \"" + pyFile + "\"", true);

                }));

            
            }
        }


    }
}
